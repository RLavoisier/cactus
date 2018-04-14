# -*- coding: utf-8 -*-
from django.db.models import Min, Max
from django.shortcuts import render, redirect
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from saisiecontrat.forms import CreationContratForm, CreationEntrepriseForm, CreationAlternantForm, InformationContratForm, InformationMissionForm
from saisiecontrat.models import Contrat, Alternant, Entreprise, ConventionCollective, Personnel, Formation
from django.core.exceptions import ObjectDoesNotExist

def creationcontrat(request):

# EXEMPLE DE FORMULAIRE GERE SANS RECOURS AUX MODELSFORMS

    if len(request.POST) > 0:

        form=CreationContratForm(request.POST)
        if form.is_valid():

            # On reçoit des données du formulaire avec un ordre de création
            # Existe-t-il déjà un contrat (courant) pour cet alternant ?
            try:
                contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)
            except ObjectDoesNotExist:
                contrat = None

            # Si aucun contrat n'existe on crée un nouveau contrat

            if contrat is None:

                contrat=Contrat(alternant=request.user.alternant,
                                type_contrat_avenant=request.POST['type_contrat_avenant'],
                                mode_contractuel=request.POST['mode_contractuel'],
                                numero_contrat_anterieur=request.POST['numero_contrat_anterieur'],
                )
                contrat.save()

            else:
                nouveaucontrat=contrat
                nouveaucontrat.id=None
                nouveaucontrat.save()
                contrat.contrat_courant = False
                contrat.save()

            return redirect("creationalternant")
        else:
            return render(request, 'creationcontrat.html', {'form': form})
    else:
        try:
            contrat=Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)
        except ObjectDoesNotExist:
            contrat = None

            # A faire charger l'objet contrat dans le formulaire si trouvé

        if contrat is not None:
            form = CreationContratForm(initial={
                "type_contrat_avenant": contrat.type_contrat_avenant,
                "mode_contractuel": contrat.mode_contractuel,
                "numero_contrat_anterieur": contrat.numero_contrat_anterieur,
            })
        else:
            form = CreationContratForm()

        return render(request, 'creationcontrat.html', {'form': form})

def create_entreprise(request):

    if len(request.POST) > 0:

        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée
        form = CreationEntrepriseForm(request.POST)

        if form.is_valid():

            # Ici, on sauvegarde le formulaire, ce qui nous renvoie automatiquement
            # un nouvel objet entreprise

            alternant = Alternant(user=request.user)
            contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)
            entreprise = contrat.entreprise

            entreprise.raison_sociale = request.POST.get("raison_sociale")
            entreprise.numero_SIRET = request.POST.get("numero_SIRET")
            entreprise.adresse_numero = request.POST.get("adresse_numero")
            entreprise.adresse_voie = request.POST.get("adresse_voie")
            entreprise.adresse_complement = request.POST.get("adresse_complement")
            entreprise.code_postal = request.POST.get("code_postal")
            entreprise.ville = request.POST.get("ville")
            entreprise.type_employeur = request.POST.get("type_employeur")
            entreprise.employeur_specifique=request.POST.get("employeur_specifique")
            entreprise.code_APE = request.POST.get("code_APE")
            entreprise.effectif_entreprise = request.POST.get("effectif_entreprise")
            entreprise.telephone = request.POST.get("telephone")
            entreprise.telecopie = request.POST.get("telecopie")
            entreprise.courriel = request.POST.get("courriel")
            entreprise.code_convention_collective = request.POST.get("code_convention_collective")
            entreprise.adhesion_regime_assurance_chomage = request.POST.get("adhesion_regime_assurance_chomage", False)
            entreprise.secteur_employeur = int(request.POST.get("type_employeur")[1])

            if len(entreprise.code_convention_collective) > 0:
                try:
                    conventioncollective = ConventionCollective.objects.get(code=entreprise.code_convention_collective)
                except ObjectDoesNotExist:
                    conventioncollective = None

                if not conventioncollective is None:
                    entreprise.libelle_convention_collective = conventioncollective.libelle

            entreprise.save()

            try:
                personnel = Personnel.objects.get(entreprise=entreprise, role=2)
            except ObjectDoesNotExist:
                personnel = None

            if personnel is None:
                personnel = Personnel(entreprise=entreprise,
                                      civilite=request.POST.get("civilite_ma_1"),
                                      nom=request.POST.get("nom_ma_1"),
                                      prenom=request.POST.get("prenom_ma_1"),
                                      role=2)
                personnel.save()
            else:
                personnel.civilite = request.POST.get("civilite_ma_1")
                personnel.nom = request.POST.get("nom_ma_1")
                personnel.prenom = request.POST.get("prenom_ma_1")
                personnel.save()

            if request.POST.get("nom_ma_2") is None:
                try:
                    personnel = Personnel.objects.get(entreprise=entreprise, role=3)
                except ObjectDoesNotExist:
                    personnel = None

                if personnel is None:
                    personnel = Personnel(entreprise=entreprise,
                                          civilite=request.POST.get("civilite_ma_2"),
                                          nom=request.POST.get("nom_ma_2"),
                                          prenom=request.POST.get("prenom_ma_2"),
                                          role=2)
                    personnel.save()
                else:
                    personnel.civilite = request.POST.get("civilite_ma_2")
                    personnel.nom = request.POST.get("nom_ma_2")
                    personnel.prenom = request.POST.get("prenom_ma_2")
                    personnel.save()

            return render(request, "entreprise_form.html", {"form": form})
        else:
            return render(request, "entreprise_form.html", {"form": form})
    else:
        alternant = request.user.alternant
        contrat= Contrat.objects.get(alternant=alternant, contrat_courant=True)

        if contrat.entreprise is None:
            entreprise=Entreprise()
            entreprise.save()
            contrat.entreprise = entreprise
            contrat.save()
        else:
            entreprise = contrat.entreprise

        try:
            personnel = Personnel.objects.get(entreprise=entreprise, role=2)
        except ObjectDoesNotExist:
            personnel = None

        form = CreationEntrepriseForm(instance=entreprise)

        if personnel is not None:
            form.fields["civilite_ma_1"].initial = personnel.civilite
            form.fields["nom_ma_1"].initial = personnel.nom
            form.fields["prenom_ma_1"].initial = personnel.prenom


        return render(request, "entreprise_form.html", {"form": form})

def create_alternant(request):


    if len(request.POST) > 0:
        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée
        form = CreationAlternantForm(request.POST)

        if form.is_valid():

            alternant = Alternant(user=request.user)
            alternant.nom = form.cleaned_data["nom"]
            alternant.prenom = form.cleaned_data["prenom"]
            alternant.date_naissance = form.cleaned_data["date_naissance"]
            alternant.numero_departement_naissance = form.cleaned_data["numero_departement_naissance"]
            alternant.adresse_numero = form.cleaned_data["adresse_numero"]
            alternant.adresse_voie = form.cleaned_data["adresse_voie"]
            alternant.code_postal = form.cleaned_data["code_postal"]
            alternant.ville = form.cleaned_data["ville"]
            alternant.telephone = form.cleaned_data["telephone"]
            # a utiliser les données issues de form_cleaned data
            alternant.handicape = form.cleaned_data["handicape"]
            alternant.nationalite = form.cleaned_data["nationalite"]
            alternant.regime_social = form.cleaned_data["regime_social"]
            alternant.situation_avant_contrat = form.cleaned_data["situation_avant_contrat"]
            alternant.dernier_diplome_prepare = form.cleaned_data["dernier_diplome_prepare"]
            alternant.derniere_annee_suivie = form.cleaned_data["derniere_annee_suivie"]
            alternant.intitule_dernier_diplome_prepare = form.cleaned_data["intitule_dernier_diplome_prepare"]
            alternant.diplome_le_plus_eleve = form.cleaned_data["diplome_le_plus_eleve"]
            alternant.civilite_representant = form.cleaned_data["civilite_representant"]
            alternant.nom_representant = form.cleaned_data["nom_representant"]
            alternant.prenom_representant = form.cleaned_data["prenom_representant"]
            alternant.adresse_numero_representant = form.cleaned_data["adresse_numero_representant"]
            alternant.adresse_voie_representant = form.cleaned_data["adresse_voie_representant"]
            alternant.code_postal_representant = form.cleaned_data["code_postal_representant"]
            alternant.ville_representant = form.cleaned_data["ville_representant"]
            alternant.date_maj = datetime.now()
            alternant.save()

            #alternant.secteur_employeur = int(form.data.get("type_employeur")[1])
            #alternant.save()

            # Pour l'exemple, lorsque nous gererons les sessions et le contrat en cours
            # Nous pourrons venir rattacher la societé au contrat de cette manière :
            #id_contrat = request.session.get("id_contrat")
            #if id_contrat:
            #    # Récupération du contrat en base de donnée
            #    contrat = Contrat.objects.get(id=id_contrat)
            #    # Rattachement de l'entreprise
            #    contrat.entreprise = entreprise
            #    # Sauvegarde du contrat
            #    contrat.save()

            #return redirect("creationalternant")

            return render(request, "alternant_form.html", {"form": form})
        else:
            return render(request, "alternant_form.html", {"form": form})
    else:
        form = CreationAlternantForm(instance=request.user.alternant)
        return render(request, "alternant_form.html", {"form": form})

def inform_contrat(request):

    if len(request.POST) > 0:

        form = InformationContratForm(request.POST, request=request)

        if form.is_valid():

            alternant = request.user.alternant
            contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)
            formation =  Formation.objects.get(formation=contrat.formation)
            if contrat.nombre_année is None:
                nombre_annees = formation.nombre_annees
            else:
                nombre_annees = contrat.nombre_annees

            annee_debut = formation.annee_remuneration_annee_diplome + 1 - nombre_annees

            i = annee_debut

            while i <= formation.annee_remuneration_annee_diplome:

                pass

            return render(request, "contrat_form.html", {"form": form})
        else:
            return render(request, "contrat_form.html", {"form": form})
    else:

        # Il faut que la date de naissance de l'alternant soit renseignée avant l'appel à ce formulaire

        form = InformationContratForm(request=request)

        return render(request, "contrat_form.html", {"form": form})


def date_anniversaire(date_naissance, date_reference):
    return datetime(date_reference.year, date_naissance.month, date_naissance.day)


def age(date_naissance, date_reference):
    date_anniversaire = date_anniversaire(date_naissance, date_reference)
    annees=date_anniversaire.year-date_naissance.year
    if date_reference<date_anniversaire:
        annees-=1
    return annees



def inform_mission(request):

    contrat = request.user.alternant.get_contrat_courant()

    if len(request.POST) > 0:

        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée

        form = InformationMissionForm(request.POST)

        if contrat.mission != request.POST.get("mission"):

            if form.is_valid():

                alternant = Alternant(user=request.user)
                contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)
                contrat.mission = request.POST.get("mission")
                contrat.date_maj_mission=datetime.now()
                contrat.date_maj=datetime.now()
                contrat.save()

                return render(request, "mission_form.html", {"form": form})
            else:
                return render(request, "mission_form.html", {"form": form})
        else:
            return render(request, "mission_form.html", {"form": form})
    else:
        form = InformationMissionForm()
        return render(request, "mission_form.html", {"form": form})


class liste_formation(ListView):
    queryset = Formation.objects.order_by("code_formation")
    template_name = "formations_list.html"
    # variable contenant les objets pour les passer au template
    context_object_name = "formations"

    def get_context_data(self, *, object_list=None, **kwargs):
        # super fait référence à la classe mère ListView
        context = super().get_context_data(object_list=None, **kwargs)
        specialites = Formation.objects.order_by("specialite").values_list("specialite", flat=True).distinct()
        villes = Formation.objects.order_by("ville").values_list("ville", flat=True).distinct()
        diplomes = Formation.DIPLOME

        context["specialites"] = ["Toutes"] + list(specialites)
        context["villes"] = ["Toutes"] + list(villes)
        context["diplomes"] = ((0, "Tous"),) + diplomes
        context["request"] = self.request

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Application des différents filtres
        filters = {
            "specialite": self.request.GET.get("specialite"),
            "ville": self.request.GET.get("ville"),
            "diplome": self.request.GET.get("diplome"),
        }

        for attr, filter in filters.items():
            if filter and filter not in ["Toutes", 0]:
                queryset = queryset.filter(**{attr: filter})

        return queryset

class detail_formation(DetailView):
    model = Formation
    template_name = ("detail_formation.html")
    context_object_name = "formation"

    def get_object(self, queryset=None):
        alternant = self.request.user.alternant
        # self.contrat permet de récupérer le contrat ailleurs dans la class
        self.contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)
        formation = self.contrat.formation
        self.cfa = formation.cfa

        # la fonction du return est d'envoyer les infos à la page
        return formation

    # On redéfinit la fonction get de la classe DetailView
    def get(self, request, *args, **kwargs):
        # get_object redéfini au-dessus pour ramener une formation précise
        self.object = self.get_object()

        # l'objet de la redéfinition de la fonction get est de rerouter vers la page de choix dans le cas où aucune formation n'est associée au contrat
        if not self.object:
            return redirect("liste_formation")
        # pas besoin de else: le return return sort de la fonction
        context = self.get_context_data(object=self.object)
        context["nombre_annees"] = self.contrat.nombre_annees
        context["nom_cfa"] = self.cfa.nom
        context["numeroUAI"] = self.cfa.numeroUAI
        context["adresse_numero"] = self.cfa.adresse_numero
        context["adresse_voie"] = self.cfa.adresse_voie
        context["adresse_complement"] = self.cfa.adresse_complement
        context["code_postal"] = self.cfa.code_postal
        context["ville"] = self.cfa.ville

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        nombre_annee = self.request.POST.get("nombre_annees")
        alternant = Alternant(user=request.user)
        contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)
        contrat.nombre_annees = request.POST.get("nombre_années")
        contrat.save()

        return redirect("detail_formation")

class appliquer_formation(DetailView):
    model = Formation

    def get(self, request, *args, **kwargs):
        # Cette vue ne sert qu'a enregistrer la formation sélectionnée dans le contrat actuel
        self.object = self.get_object()

        contrat = self.request.user.alternant.get_contrat_courant()

        if contrat:
            contrat.formation = self.object
            contrat.save()

        return redirect("detail_formation")

