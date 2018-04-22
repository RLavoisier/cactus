# coding: utf-8

import re
from copy import deepcopy

from django.db.models import Min, Max

from django.shortcuts import render, redirect
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from saisiecontrat.forms import CreationContratForm, CreationEntrepriseForm, CreationAlternantForm, InformationContratForm, InformationMissionForm
from saisiecontrat.models import Contrat, Alternant, Entreprise, ConventionCollective, Personnel, Formation, CFA
from django.core.exceptions import ObjectDoesNotExist

from saisiecontrat.utils.pdf_generator import PDFGenerator


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

            context = {}

            # Si aucun contrat n'existe on crée un nouveau contrat
            if contrat is None:

                contrat=Contrat(alternant=request.user.alternant,
                                type_contrat_avenant=request.POST['type_contrat_avenant'],
                                mode_contractuel=request.POST['mode_contractuel'],
                                numero_contrat_anterieur=request.POST['numero_contrat_anterieur'],
                                date_effet_avenant=request.POST['date_effet_avenant'],
                                )
                contrat.save()
                context["message"] = "Le contrat a bien été créé vous pouvez maintenant le compléter dans les onglets suivants."
            else:
                # copy ll'objet (si on écrit nouveaucontrat=contrat on crée juste un pointeur sur contrat)
                # Cette syntaxe python fonctionne sur tout type d'objet et  dictionnaire
                nouveaucontrat = deepcopy(contrat)

                nouveaucontrat.id=None
                nouveaucontrat.type_contrat_avenant = request.POST['type_contrat_avenant']
                nouveaucontrat.mode_contractuel = request.POST['mode_contractuel']
                nouveaucontrat.numero_contrat_anterieur = request.POST['numero_contrat_anterieur']
                if request.POST['date_effet_avenant'] is not None:
                    nouveaucontrat.date_effet_avenant = request.POST['date_effet_avenant']

                nouveaucontrat.save()

                contrat.contrat_courant = False
                contrat.save()

                context["message"] = "Un contrat a bien été créé. Les données du contrat précédent on été reprises vous pouver modifier les données dans les onglets suivants."

            form = CreationContratForm(initial={
                "type_contrat_avenant": nouveaucontrat.type_contrat_avenant,
                "mode_contractuel": nouveaucontrat.mode_contractuel,
                "numero_contrat_anterieur": nouveaucontrat.numero_contrat_anterieur,
                "date_effet_avenant": nouveaucontrat.date_effet_avenant,
            })

            context["form"] = form
            context["contrat"] = contrat
            return render(request, 'creationcontrat.html', context)

            # return redirect("creationalternant")
        else:
            return render(request, 'creationcontrat.html', {'form': form})
    else:
        context = {}
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
                "date_effet_avenant": contrat.date_effet_avenant,
            })
        else:
            form = CreationContratForm()

        context["form"] = form
        context["contrat"]=contrat

        return render(request, 'creationcontrat.html', context)

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

            entreprise.raison_sociale = form.cleaned_data["raison_sociale"]
            entreprise.numero_SIRET = form.cleaned_data["numero_SIRET"]
            entreprise.adresse_numero = form.cleaned_data["adresse_numero"]
            entreprise.adresse_voie = form.cleaned_data["adresse_voie"]
            entreprise.adresse_complement = form.cleaned_data["adresse_complement"]
            entreprise.code_postal = form.cleaned_data["code_postal"]
            entreprise.ville = form.cleaned_data["ville"]
            entreprise.type_employeur = form.cleaned_data["type_employeur"]
            entreprise.employeur_specifique=form.cleaned_data["employeur_specifique"]
            entreprise.code_APE = form.cleaned_data["code_APE"]
            entreprise.effectif_entreprise = form.cleaned_data["effectif_entreprise"]
            entreprise.telephone = form.cleaned_data["telephone"]
            entreprise.telecopie = form.cleaned_data["telecopie"]
            entreprise.courriel = form.cleaned_data["courriel"]
            entreprise.code_convention_collective = form.cleaned_data["code_convention_collective"]
            entreprise.adhesion_regime_assurance_chomage = form.cleaned_data["adhesion_regime_assurance_chomage"]
            if form.cleaned_data["type_employeur"] in (11, 12, 13, 14, 15, 16):
                entreprise.secteur_employeur = 1
            else:
                entreprise.secteur_employeur = 2

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
                                      date_naissance=request.POST.get("date_naissance_ma_1"),
                                      role=2)
                personnel.save()
            else:
                personnel.civilite = request.POST.get("civilite_ma_1")
                personnel.nom = request.POST.get("nom_ma_1")
                personnel.prenom = request.POST.get("prenom_ma_1")
                personnel.date_naissance = request.POST.get("date_naissance_ma_1")
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
                                          date_naissance=request.POST.get("date_naissance_ma_2"),
                                          role=3)
                    personnel.save()
                else:
                    personnel.civilite = request.POST.get("civilite_ma_2")
                    personnel.nom = request.POST.get("nom_ma_2")
                    personnel.prenom = request.POST.get("prenom_ma_2")
                    personnel.date_naissance = request.POST.get("date_naissance_ma_2")
                    personnel.save()

            if request.POST.get("nom_contact") is None:
                try:
                    personnel = Personnel.objects.get(entreprise=entreprise, role=4)
                except ObjectDoesNotExist:
                    personnel = None

                if personnel is None:
                    personnel = Personnel(entreprise=entreprise,
                                          civilite=request.POST.get("civilite_contact"),
                                          nom=request.POST.get("nom_contact"),
                                          prenom=request.POST.get("prenom_contact"),
                                          courriel=request.POST.get("courriel_contact"),
                                          role=4)
                    personnel.save()
                else:
                    personnel.civilite = request.POST.get("civilite_contact")
                    personnel.nom = request.POST.get("nom_contact")
                    personnel.prenom = request.POST.get("prenom_contact")
                    personnel.courriel_contact = request.POST.get("courriel_contact")
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
            form.fields["date_naissance_ma_1"].initial = personnel.date_naissance

        try:
            personnel = Personnel.objects.get(entreprise=entreprise, role=3)
        except ObjectDoesNotExist:
            personnel = None

        form = CreationEntrepriseForm(instance=entreprise)

        if personnel is not None:
            form.fields["civilite_ma_2"].initial = personnel.civilite
            form.fields["nom_ma_2"].initial = personnel.nom
            form.fields["prenom_ma_2"].initial = personnel.prenom
            form.fields["date_naissance_ma_2"].initial = personnel.date_naissance

        try:
            personnel = Personnel.objects.get(entreprise=entreprise, role=4)
        except ObjectDoesNotExist:
            personnel = None

        form = CreationEntrepriseForm(instance=entreprise)

        if personnel is not None:
            form.fields["civilite_contact"].initial = personnel.civilite
            form.fields["nom_contact"].initial = personnel.nom
            form.fields["prenom_contact"].initial = personnel.prenom
            form.fields["courriel_contact"].initial = personnel.courriel


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
            alternant.commune_naissance = form.cleaned_data["commune_naissance"]
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

            contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)

            contrat.type_derogation = form.cleaned_data["type_derogation"]
            contrat.date_embauche = form.cleaned_data["date_embauche"]
            contrat.date_debut_contrat = form.cleaned_data["date_debut_contrat"]
            contrat.date_effet_avenant = form.cleaned_data["date_effet_avenant"]
            contrat.date_fin_contrat = form.cleaned_data["date_fin_contrat"]
            contrat.duree_hebdomadaire_travail = form.cleaned_data["duree_hebdomadaire_travail"]
            contrat.risques_particuliers = form.cleaned_data["risques_particuliers"]
            contrat.caisse_retraite_complementaire = form.cleaned_data["caisse_retraite_complementaire"]
            contrat.salaire_brut_mensuel = form.cleaned_data["salaire_brut_mensuel"]
            contrat.nourriture = form.cleaned_data["nourriture"]
            contrat.logement = form.cleaned_data["logement"]
            contrat.prime_panier = form.cleaned_data["prime_panier"]
            contrat.fait_a = form.cleaned_data["fait_a"]
            contrat.fait_le = form.cleaned_data["fait_le"]

            contrat.an_1_per_1_du = form.cleaned_data["an_1_per_1_du"]
            contrat.an_1_per_1_au = form.cleaned_data["an_1_per_1_au"]
            contrat.an_1_per_1_taux = form.cleaned_data["an_1_per_1_taux"]
            contrat.an_1_per_1_base = form.cleaned_data["an_1_per_1_base"]
            contrat.an_1_per_2_du = form.cleaned_data["an_1_per_2_du"]
            contrat.an_1_per_2_au = form.cleaned_data["an_1_per_2_au"]
            contrat.an_1_per_2_taux = form.cleaned_data["an_1_per_2_taux"]
            contrat.an_1_per_2_base = form.cleaned_data["an_1_per_2_base"]

            contrat.an_2_per_1_du = form.cleaned_data["an_2_per_1_du"]
            contrat.an_2_per_1_au = form.cleaned_data["an_2_per_1_au"]
            contrat.an_2_per_1_taux = form.cleaned_data["an_2_per_1_taux"]
            contrat.an_2_per_1_base = form.cleaned_data["an_2_per_1_base"]
            contrat.an_2_per_2_du = form.cleaned_data["an_2_per_2_du"]
            contrat.an_2_per_2_au = form.cleaned_data["an_2_per_2_au"]
            contrat.an_2_per_2_taux = form.cleaned_data["an_2_per_2_taux"]
            contrat.an_2_per_2_base = form.cleaned_data["an_2_per_2_base"]

            contrat.an_3_per_1_du = form.cleaned_data["an_3_per_1_du"]
            contrat.an_3_per_1_au = form.cleaned_data["an_3_per_1_au"]
            contrat.an_3_per_1_taux = form.cleaned_data["an_3_per_1_taux"]
            contrat.an_3_per_1_base = form.cleaned_data["an_3_per_1_base"]
            contrat.an_3_per_2_du = form.cleaned_data["an_3_per_2_du"]
            contrat.an_3_per_2_au = form.cleaned_data["an_3_per_2_au"]
            contrat.an_3_per_2_taux = form.cleaned_data["an_3_per_2_taux"]
            contrat.an_3_per_2_base = form.cleaned_data["an_3_per_2_base"]

            contrat.an_4_per_1_du = form.cleaned_data["an_4_per_1_du"]
            contrat.an_4_per_1_au = form.cleaned_data["an_4_per_1_au"]
            contrat.an_4_per_1_taux = form.cleaned_data["an_4_per_1_taux"]
            contrat.an_4_per_1_base = form.cleaned_data["an_4_per_1_base"]
            contrat.an_4_per_2_du = form.cleaned_data["an_4_per_2_du"]
            contrat.an_4_per_2_au = form.cleaned_data["an_4_per_2_au"]
            contrat.an_4_per_2_taux = form.cleaned_data["an_4_per_2_taux"]
            contrat.an_4_per_2_base = form.cleaned_data["an_4_per_2_base"]

            contrat.date_maj=datetime.now()

            contrat.save()

        return render(request, "contrat_form.html", {"form": form})
    else:

        contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)

        # dans le formulaire on utilise l'objet user de la request qui n'existe pas dans le formulaire
        form = InformationContratForm(instance=contrat, request=request)
        return render(request, "contrat_form.html", {"form": form})


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
        contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)

        form = InformationMissionForm(instance=contrat)
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
        if self.contrat.nombre_annees is None:
            context["nombre_annees"] = context.get("formation").nombre_annees
        else:
            context["nombre_annees"] = self.contrat.nombre_annees
        context["nom_cfa"] = self.object.cfa.nom
        context["numeroUAI"] = self.object.cfa.numeroUAI
        context["adresse_numero"] = self.object.cfa.adresse_numero
        context["adresse_voie"] = self.object.cfa.adresse_voie
        context["adresse_complement"] = self.object.cfa.adresse_complement
        context["code_postal"] = self.object.cfa.code_postal
        context["ville"] = self.object.cfa.ville

        i=0

        if context.get("formation").diplome is not None:
            while context.get("formation").diplome != Formation.DIPLOME[i][0]:
                i+=1

        context["libelle_diplome"] = Formation.DIPLOME[i][1]

        #if context.get("formation").inspection_pedagogique_competente is not None:
        #    while context.get("formation").inspection_pedagogique_competente != Formation.INSPECTION_PEDAGOGIQUE[i][0]:
        #        i+=1

        #context["libelle_inspection_pedagogique_competente"] = Formation.INSPECTION_PEDAGOGIQUE[i][1]

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        nombre_annee = self.request.POST.get("nombre_annees")
        alternant = Alternant(user=request.user)
        contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)
        contrat.nombre_annees = nombre_annee
        contrat.save()

        return redirect("detail_formation")

class appliquer_formation(DetailView):
    model = Formation

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
            return redirect("comptes:login")

        # Cette vue ne sert qu'a enregistrer la formation sélectionnée dans le contrat actuel
        self.object = self.get_object()

        contrat = self.request.user.alternant.get_contrat_courant()

        if contrat:
            contrat.formation = self.object
            contrat.save()

        return redirect("detail_formation")


class creerCERFA(DetailView):
    model = Contrat

    def get(self, request, *args, **kwargs):
        # Recuperer les infos qui nous interesse pour le pdf


        alternant = Alternant.objects.get(user=request.user)
        contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)
        entreprise = contrat.entreprise
        formation = contrat.formation
        cfa = formation.cfa

        try:
            ma_1 = Personnel.objects.get(entreprise=entreprise, role=2)
        except ObjectDoesNotExist:
            ma_1 = None

        try:
            ma_2 = Personnel.objects.get(entreprise=entreprise, role=3)
        except ObjectDoesNotExist:
            ma_2 = None

        # Construction du dictionnaire des valeur du pdf
        data = {}
        if entreprise.secteur_employeur == 1:
            data["emp_prive"] = 1
        else:
            data["emp_public"] = 1

        if contrat.type_contrat_avenant in (31,32,33,34,35,36):
            data["avenant"] = 1
        else:
            data["contrat"] = 1

        data["mode_Contrat"] = contrat.mode_contractuel
        data["emp_siret"] = entreprise.numero_SIRET
        data["emp_adr_num"] = entreprise.adresse_numero
        data["emp_adr_voie"] = entreprise.adresse_voie.upper()
        if entreprise.adresse_complement is not None:
            data["emp_adr_compl"] = entreprise.adresse_complement.upper()
        data["emp_adr_cp"] = entreprise.code_postal
        data["emp_adr_ville"] = entreprise.ville.upper()
        data["emp_tel"] = entreprise.telephone
        data["emp_fax"] = entreprise.telecopie

        data["emp_mail1"] = entreprise.courriel[0:entreprise.courriel.find('@')]
        data["emp_mail2"] = entreprise.courriel[entreprise.courriel.find('@')+1:]
        data["emp_type"] = entreprise.type_employeur
        data["emp_specifique"] = entreprise.employeur_specifique
        data["emp_naf"] = entreprise.code_APE
        data["emp_eff"] = entreprise.effectif_entreprise

        data["emp_conv_coll"] = entreprise.libelle_convention_collective

        data["emp_idcc"] = entreprise.code_convention_collective
        data["emp_denom"] = entreprise.raison_sociale.upper()
        data["emp_adh_chomage"] = entreprise.adhesion_regime_assurance_chomage

        data["alt_nom"] = "%s %s" % (alternant.nom.upper(), alternant.prenom.upper())
        data["alt_mail1"] = request.user.email
        data["alt_tel"] = alternant.telephone
        data["alt_adr_ville"] = alternant.ville
        data["alt_adr_cp"] = alternant.code_postal
        data["alt_adr_num"] = alternant.adresse_numero
        data["alt_adr_voie"] = alternant.adresse_voie.upper()
        data["alt_repr_adr_ville"] = alternant.ville_representant
        data["alt_repr_adr_cp"] = alternant.code_postal_representant
        data["alt_repr_adr_voie"] = alternant.adresse_voie_representant
        data["alt_repr_adr_num"] = alternant.adresse_numero_representant
        nom_prenom_representant = "%s %s" % (alternant.nom_representant, alternant.prenom_representant)
        data["alt_repr_nom"] = nom_prenom_representant

        data["alt_ddn_jour"] = str(alternant.date_naissance.day).zfill(2)
        data["alt_ddn_mois"] = str(alternant.date_naissance.month).zfill(2)
        data["alt_ddn_annee"] = alternant.date_naissance.year

        data["alt_departement_naissance"] = alternant.numero_departement_naissance
        data["alt_regime"] = alternant.regime_social
        data["alt_nationnalite"] = alternant.nationalite
        data["alt_derniere_situation"] = alternant.situation_avant_contrat
        data["alt_dernier_diplome"] = alternant.dernier_diplome_prepare
        data["alt_derniere_classe"] = alternant.derniere_annee_suivie
        data["alt_dernier_diplome_intitule"] = alternant.intitule_dernier_diplome_prepare
        data["alt_diplome"] = alternant.diplome_le_plus_eleve

        if alternant.sexe == 'M':
            data["alt_sexe_m"] = 1
        else:
            data["alt_sexe_f"] = 1

        if alternant.handicape:
            data["alt_handicape_oui"] = 1
        else:
            data["alt_handicape_non"] = 1

        data["commune_naissance"] = alternant.commune_naissance

        data["maitre1_nom"] = "%s %s" % (ma_1.nom, ma_1.prenom)
        data["maitre1_ddn_jour"] = str(ma_1.date_naissance.day).zfill(2)
        data["maitre1_ddn_mois"] = str(ma_1.date_naissance.month).zfill(2)
        data["maitre1_ddn_annee"] = ma_1.date_naissance.year

        if ma_2 is not None:
            data["maitre2_nom"] = "%s %s" % (ma_2.nom, ma_2.prenom)
            data["maitre2_ddn_jour"] = str(ma_2.date_naissance.day).zfill(2)
            data["maitre2_ddn_mois"] = str(ma_2.date_naissance.month).zfill(2)
            data["maitre2_ddn_annee"] = ma_2.date_naissance.year

        if contrat.attestation_maitre_apprentissage:
            data["maitre_attestation"] = 1
        data["contrat_type"] = contrat.type_contrat_avenant
        data["contrat_derog"] = contrat.type_derogation

        if contrat.numero_contrat_anterieur is not None:
            data["contrat_num_prec"] = contrat.numero_contrat_anterieur

        data["contrat_debut_jour"] = str(contrat.date_embauche.day).zfill(2)
        data["contrat_debut_mois"] = str(contrat.date_embauche.month).zfill(2)
        data["contrat_debut_annee"] = contrat.date_embauche.year
        data["execution_fin_annee"] = contrat.date_debut_contrat.year
        data["execution_fin_mois"] = str(contrat.date_debut_contrat.month).zfill(2)
        data["execution_fin_jour"] = str(contrat.date_debut_contrat.day).zfill(2)

        data["contrat_duree_hebdo_heures"] = str(contrat.duree_hebdomadaire_travail).split(":")[1]
        data["contrat_duree_hebdo_minutes"] = str(contrat.duree_hebdomadaire_travail).split(":")[2]

        if contrat.risques_particuliers:
            data["contrat_risques_oui"] = 1
        else:
            data["contrat_risques_non"] = 1

        data["contrat_remu_annee1_taux1"] = str(contrat.an_1_per_1_taux)
        data["contrat_remu_annee2_taux1"] = str(contrat.an_2_per_1_taux)
        data["contrat_remu_annee3_taux1"] = str(contrat.an_3_per_1_taux)
        data["contrat_remu_annee4_taux1"] = str(contrat.an_4_per_1_taux)
        data["contrat_remu_annee1_du1_jour"] = str(contrat.an_1_per_1_du.day).zfill(2)
        data["contrat_remu_annee1_du1_mois"] = str(contrat.an_1_per_1_du.month).zfill(2)
        data["contrat_remu_annee1_du1_annee"] = contrat.an_1_per_1_du.year
        data["contrat_remu_annee2_du1_jour"] = str(contrat.an_2_per_1_du.day).zfill(2)
        data["contrat_remu_annee2_du1_mois"] = str(contrat.an_2_per_1_du.month).zfill(2)
        data["contrat_remu_annee2_du1_annee"] = contrat.an_2_per_1_du.year
        data["contrat_remu_annee3_du1_jour"] = str(contrat.an_3_per_1_du.day).zfill(2)
        data["contrat_remu_annee3_du1_mois"] = str(contrat.an_3_per_1_du.month).zfill(2)
        data["contrat_remu_annee3_du1_annee"] = contrat.an_3_per_1_du.year
        data["contrat_remu_annee4_du1_jour"] = str(contrat.an_4_per_1_du.day).zfill(2)
        data["contrat_remu_annee4_du1_mois"] = str(contrat.an_4_per_1_du.month).zfill(2)
        data["contrat_remu_annee4_du1_annee"] = contrat.an_4_per_1_du.year
        data["contrat_remu_annee1_au1_jour"] = str(contrat.an_1_per_1_au.day).zfill(2)
        data["contrat_remu_annee1_au1_mois"] = str(contrat.an_1_per_1_au.month).zfill(2)
        data["contrat_remu_annee1_au1_annee"] = contrat.an_1_per_1_au.year
        data["contrat_remu_annee2_au1_jour"] = str(contrat.an_2_per_1_au.day).zfill(2)
        data["contrat_remu_annee2_au1_mois"] = str(contrat.an_2_per_1_au.month).zfill(2)
        data["contrat_remu_annee2_au1_annee"] = contrat.an_2_per_1_au.year
        data["contrat_remu_annee3_au1_jour"] = str(contrat.an_3_per_1_au.day).zfill(2)
        data["contrat_remu_annee3_au1_mois"] = str(contrat.an_3_per_1_au.month).zfill(2)
        data["contrat_remu_annee3_au1_annee"] = contrat.an_3_per_1_au.year
        data["contrat_remu_annee4_au1_jour"] = str(contrat.an_4_per_1_au.day).zfill(2)
        data["contrat_remu_annee4_au1_mois"] = str(contrat.an_4_per_1_au.month).zfill(2)
        data["contrat_remu_annee4_au1_annee"] = contrat.an_4_per_1_au.year
        data["contrat_remu_annee1_ref1"] = Contrat.BASE[contrat.an_1_per_1_base - 1][1]
        data["contrat_remu_annee2_ref1"] = Contrat.BASE[contrat.an_2_per_1_base - 1][1]
        data["contrat_remu_annee3_ref1"] = Contrat.BASE[contrat.an_3_per_1_base - 1][1]
        data["contrat_remu_annee4_ref1"] = Contrat.BASE[contrat.an_4_per_1_base - 1][1]
        data["contrat_remu_annee1_taux2"] = str(contrat.an_1_per_2_taux)
        data["contrat_remu_annee2_taux2"] = str(contrat.an_2_per_2_taux)
        data["contrat_remu_annee3_taux2"] = str(contrat.an_3_per_2_taux)
        data["contrat_remu_annee4_taux2"] = str(contrat.an_4_per_2_taux)
        data["contrat_remu_annee1_du2_jour"] = str(contrat.an_1_per_2_du.day).zfill(2)
        data["contrat_remu_annee1_du2_mois"] = str(contrat.an_1_per_2_du.month).zfill(2)
        data["contrat_remu_annee1_du2_annee"] = contrat.an_1_per_2_du.year
        data["contrat_remu_annee2_du2_jour"] = str(contrat.an_2_per_2_du.day).zfill(2)
        data["contrat_remu_annee2_du2_mois"] = str(contrat.an_2_per_2_du.month).zfill(2)
        data["contrat_remu_annee2_du2_annee"] = contrat.an_2_per_2_du.year
        data["contrat_remu_annee3_du2_jour"] = str(contrat.an_3_per_2_du.day).zfill(2)
        data["contrat_remu_annee3_du2_mois"] = str(contrat.an_3_per_2_du.month).zfill(2)
        data["contrat_remu_annee3_du2_annee"] = contrat.an_3_per_2_du.year
        data["contrat_remu_annee4_du2_jour"] = str(contrat.an_4_per_2_du.day).zfill(2)
        data["contrat_remu_annee4_du2_mois"] = str(contrat.an_4_per_2_du.month).zfill(2)
        data["contrat_remu_annee4_du2_annee"] = contrat.an_4_per_2_du.year
        data["contrat_remu_annee1_au2_jour"] = str(contrat.an_1_per_2_au.day).zfill(2)
        data["contrat_remu_annee1_au2_mois"] = str(contrat.an_1_per_2_au.month).zfill(2)
        data["contrat_remu_annee1_au2_annee"] = contrat.an_1_per_2_au.year
        data["contrat_remu_annee2_au2_jour"] = str(contrat.an_2_per_2_au.day).zfill(2)
        data["contrat_remu_annee2_au2_mois"] = str(contrat.an_2_per_2_au.month).zfill(2)
        data["contrat_remu_annee2_au2_annee"] = contrat.an_2_per_2_au.year
        data["contrat_remu_annee3_au2_jour"] = str(contrat.an_3_per_2_au.day).zfill(2)
        data["contrat_remu_annee3_au2_mois"] = str(contrat.an_3_per_2_au.month).zfill(2)
        data["contrat_remu_annee3_au2_annee"] = contrat.an_3_per_2_au.year
        data["contrat_remu_annee4_au2_jour"] = str(contrat.an_4_per_2_au.day).zfill(2)
        data["contrat_remu_annee4_au2_mois"] = str(contrat.an_4_per_2_au.month).zfill(2)
        data["contrat_remu_annee4_au2_annee"] = contrat.an_4_per_2_au.year
        data["contrat_remu_annee1_ref2"] = Contrat.BASE[contrat.an_1_per_2_base - 1][1]
        data["contrat_remu_annee2_ref2"] = Contrat.BASE[contrat.an_2_per_2_base - 1][1]
        data["contrat_remu_annee3_ref2"] = Contrat.BASE[contrat.an_3_per_2_base - 1][1]
        data["contrat_remu_annee4_ref2"] = Contrat.BASE[contrat.an_4_per_2_base - 1][1]

        entier = int(contrat.salaire_brut_mensuel)
        decimal = contrat.salaire_brut_mensuel - entier
        data["contrat_salaire1"] = entier
        data["contrat_salaire2"] = str(int(decimal)).zfill(2)

        if contrat.nourriture is not None:
            entier = int(contrat.nourriture)
            decimal = (contrat.nourriture - entier)*100
            data["contrat_avantg_nourr1"] = entier
            data["contrat_avantg_nourr2"] = str(int(decimal)).zfill(2)

        if contrat.logement is not None:
            entier = int(contrat.logement)
            decimal = (contrat.logement - entier)*100
            data["contrat_avantg_logt1"] = entier
            data["contrat_avantg_logt2"] =  str(int(decimal)).zfill(2)


        if contrat.prime_panier is not None:
            entier = int(contrat.prime_panier)
            decimal = (contrat.prime_panier - entier)*100
            data["panier_avantg_logt1"] = entier
            data["panier_avantg_logt2"] =  str(int(decimal)).zfill(2)


        if contrat.date_effet_avenant is not None:
            data["avenant_debut_jour"] = str(contrat.date_effet_avenant.day).zfill(2)
            data["avenant_debut_mois"] = str(contrat.date_effet_avenant.month).zfill(2)
            data["avenant_debut_annee"] = contrat.date_effet_avenant.year

        data["contrat_fin_jour"] = str(contrat.date_fin_contrat.day).zfill(2)
        data["contrat_fin_mois"] = str(contrat.date_fin_contrat.month).zfill(2)
        data["contrat_fin_annee"] = contrat.date_fin_contrat.year
        data["retraite_caisse_comp"] = contrat.caisse_retraite_complementaire

        data["formation_nom"] = cfa.nom
        print(cfa.nom)
        data["formation_uai"] = cfa.numeroUAI

        data["formation_adr_voie"] = cfa.adresse_voie
        data["formation_adr_num"] = cfa.adresse_numero
        data["formation_adr_compl"] = cfa.adresse_complement
        data["formation_adr_cp"] = cfa.code_postal
        data["formation_adr_ville"] = cfa.ville
        data["formation_inspect_pedag"] = formation.inspection_pedagogique_competente
        data["signature_date_annee"] = contrat.fait_le.year
        data["signature_date_mois"] = str(contrat.fait_le.month).zfill(2)
        data["signature_date_jour"] = str(contrat.fait_le.day).zfill(2)
        data["signature_lieu"] = contrat.fait_a
        if contrat.attestation_pieces:
            data["signature_emp_attestation"] = 1
        data["formation_intitule"] = formation.intitule_diplome
        data["formation_diplome"] = formation.diplome
        data["formation_diplome_code"] = formation.code_diplome_apprentissage

        if contrat.date_inscription is not None:
            data["inscription_annee"] = contrat.date_inscription.year
            data["inscription_mois"] = str(contrat.date_inscription.month).zfill(2)
            data["inscription_jour"] = str(contrat.date_inscription.day).zfill(2)

        if formation.heures_an_1 is not None:
            data["formation_annee2_heure"] = formation.heures_an_1
        if formation.an_1_du is not None:
            data["formation_annee1_du_jour"] = str(formation.an_1_du.day).zfill(2)
            data["formation_annee1_du_mois"] = str(formation.an_1_du.month).zfill(2)
            data["formation_annee1_du_annee"] = formation.an_1_du.year
        if formation.an_1_au is not None:
            data["formation_annee1_au_jour"] = str(formation.an_1_au.day).zfill(2)
            data["formation_annee1_au_mois"] = str(formation.an_1_au.month).zfill(2)
            data["formation_annee1_au_annee"] = formation.an_1_au.year

        if formation.heures_an_2 is not None:
            data["formation_annee2_heure"] = formation.heures_an_2
        if formation.an_2_du is not None:
            data["formation_annee2_du_jour"] = str(formation.an_2_du.day).zfill(2)
            data["formation_annee2_du_mois"] = str(formation.an_2_du.month).zfill(2)
            data["formation_annee2_du_annee"] = formation.an_2_du.year
        if formation.an_2_au is not None:
            data["formation_annee2_au_jour"] = str(formation.an_2_au.day).zfill(2)
            data["formation_annee2_au_mois"] = str(formation.an_2_au.month).zfill(2)
            data["formation_annee2_au_annee"] = formation.an_2_au.year

        if formation.heures_an_3 is not None:
            data["formation_annee3_heure"] = formation.heures_an_3
        if formation.an_3_du is not None:
            data["formation_annee3_du_jour"] = str(formation.an_3_du.day).zfill(2)
            data["formation_annee3_du_mois"] = str(formation.an_3_du.month).zfill(2)
            data["formation_annee3_du_annee"] = formation.an_3_du.year
        if formation.an_3_au is not None:
            data["formation_annee3_au_jour"] = str(formation.an_3_au.day).zfill(2)
            data["formation_annee3_au_mois"] = str(formation.an_3_au.month).zfill(2)
            data["formation_annee3_au_annee"] = formation.an_3_au.year

        nomfichier = PDFGenerator.generate_pdf_with_datas(data, nom_template="cerfa_10103.pdf", flatten=False, cerfa_pdf=True)

        return redirect("informationmission")

class creerfichemission(DetailView):
    model = Contrat

    def get(self, request, *args, **kwargs):

        alternant = Alternant.objects.get(user=request.user)
        contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)
        entreprise = contrat.entreprise
        formation = contrat.formation
        cfa = formation.cfa

        try:
            ma_1 = Personnel.objects.get(entreprise=entreprise, role=2)
        except ObjectDoesNotExist:
            ma_1 = None

        data = {}
        data["numero"] = alternant.adresse_numero
        data["voie"] = alternant.adresse_voie
        data["codepostal"] = alternant.code_postal
        data["ville"] = alternant.ville
        data["neele"] = alternant.date_naissance
        data["mail"] = request.user.email
        data["telephone"] = alternant.telephone
        data["nomprenom"] = "%s %s" % (alternant.nom, alternant.prenom)

        data["raisonsociale"] = entreprise.raison_sociale
        data["numero2"] = entreprise.adresse_numero
        data["voie2"] = entreprise.adresse_voie
        data["complement2"] = entreprise.adresse_complement
        data["codepostal2"] = entreprise.code_postal
        data["ville2"] = entreprise.ville
        data["telephone2"] = entreprise.telephone
        data["mail2"] = entreprise.courriel
        data["siret"] = entreprise.numero_SIRET
        data["codeape"] = entreprise.code_APE

        if ma_1 is not None:
            data["maitredapprentissage"] = "%s %s" % (ma_1.nom, ma_1.prenom)

        data["mission"] = contrat.mission

        nomfichier = PDFGenerator.generate_pdf_with_datas(data, nom_template="fiche_mission.pdf", flatten=False, cerfa_pdf=False)

        return redirect("informationmission")
