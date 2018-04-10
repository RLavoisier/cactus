# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from datetime import datetime

from django.views.generic import ListView

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

            # Si aucun contrat n'existe on cré un nouveau contrat

            if contrat is not None:

                contrat=Contrat(alternant=request.user.alternant,
                                type_contrat_avenant=request.POST['type_contrat_avenant'],
                                mode_contractuel=request.POST['mode_contractuel'],
                                numero_contrat_anterieur=request.POST['numero_contrat_anterieur'],
                )
                contrat.save()

            else:
                nouveaucontrat=contrat
                contrat.contrat_courant = False
                contrat.save()
                nouveaucontrat.save()

            return render(request, 'creationcontrat.html', {'form': form})
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
            form = CreationContratForm(instance=contrat)

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
            entreprise.adresse_1 = request.POST.get("adresse_1")
            entreprise.adresse_2 = request.POST.get("adresse_2")
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
            entreprise.adhesion_regime_assurance_chomage = request.POST.get("adhesion_regime_assurance_chomage")

            entreprise.secteur_employeur = int(request.POST.get("type_employeur")[1])

            if not request.POST.get("code_convention_collective") is None:
                try:
                    conventioncollective = ConventionCollective.objects.get(code=entreprise.code_convention_collective)
                except ObjectDoesNotExist:
                    conventioncollective = None

                if not conventioncollective is None:
                    entreprise.libelle_convention_collective = ConventionCollective.libelle

            entreprise.save()

            try:
                personnel = Personnel.objects.get(id=entreprise.id, role=1)
            except ObjectDoesNotExist:
                personnel = None

            if personnel is None:
                personnel = Personnel(entreprise=entreprise,
                                      civilite_dirigeant=request.POST.get("civilite_dirigeant"),
                                      nom_dirigeant = request.POST.get("nom_dirigeant"),
                                      prenom_dirigeant = request.POST.get("prenom_dirigeant"),
                                      role=1)
                personnel.save()
            else:
                personnel.civilite_dirigeant = request.POST.get("civilite_dirigeant")
                personnel.nom_dirigeant = request.POST.get("nom_dirigeant")
                personnel.prenom_dirigeant = request.POST.get("prenom_dirigeant")
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

        form = CreationEntrepriseForm(instance=entreprise)
        return render(request, "entreprise_form.html", {"form": form})

def create_alternant(request):


    if request.method == "POST":
        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée
        form = CreationAlternantForm(request.POST)

        if form.is_valid():

            alternant = Alternant(user=request.user)
            alternant.nom = request.POST['nom']
            alternant.prenom = request.POST['prenom']
            alternant.date_naissance = request.POST['date_naissance']
            alternant.numero_departement_naissance = request.POST['numero_departement_naissance']
            alternant.adresse_1 = request.POST['adresse_1']
            alternant.adresse_2 = request.POST['adresse_2']
            alternant.code_postal = request.POST['code_postal']
            alternant.ville = request.POST['ville']
            alternant.telephone = request.POST['telephone']
            #alternant.handicape = request.POST['handicape']
            alternant.nationalite = request.POST['nationalite']
            alternant.regime_social = request.POST['regime_social']
            alternant.situation_avant_contrat = request.POST['situation_avant_contrat']
            alternant.dernier_diplome_prepare = request.POST['dernier_diplome_prepare']
            alternant.derniere_annee_suivie = request.POST['derniere_annee_suivie']
            alternant.intitule_dernier_diplome_prepare = request.POST['intitule_dernier_diplome_prepare']
            alternant.diplome_le_plus_eleve = request.POST['diplome_le_plus_eleve']
            alternant.nom_representant = request.POST['nom_representant']
            alternant.prenom_representant = request.POST['prenom_representant']
            alternant.adresse_1_representant = request.POST['adresse_1_representant']
            alternant.adresse_2_representant = request.POST['adresse_2_representant']
            alternant.code_postal_representant = request.POST['code_postal_representant']
            alternant.ville_representant = request.POST['ville_representant']
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

        form = InformationContratForm(request.POST)

        if form.is_valid():

            # Ici, on sauvegarde le formulaire, ce qui nous renvoie automatiquement
            # un nouvel objet contrat

            contrat = form.save()


            return render(request, "contrat_form.html", {"form": form})
        else:
            return render(request, "contrat_form.html", {"form": form})
    else:

        # Il faut que la date de naissance de l'alternant soit renseignée avant l'appel à ce formulaire

        form = InformationContratForm()

        return render(request, "contrat_form.html", {"form": form})

def inform_mission(request):

    if request.method == "POST":
        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée

        form = InformationMissionForm(request.POST)

        if form.has_changed():

            if form.is_valid():

                # Ici, on sauvegarde le formulaire, ce qui nous renvoie automatiauement
                # un nouvel objet entreprise

                contrat = form.save()


                return render(request, "mission_form.html", {"form": form})
            else:
                return render(request, "mission_form.html", {"form": form})
    else:

        form = InformationMissionForm()
        return render(request, "mission_form.html", {"form": form})


class liste_formation(ListView):
    queryset = Formation.objects.order_by("specialite")
    template_name = "formations_list.html"
    context_object_name = "formations"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        specialites = Formation.objects.order_by("specialite").values_list("specialite", flat=True).distinct()
        context["specialites"] = ["Toutes"] + list(specialites)
        context["request"] = self.request

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        specialite_filter = self.request.GET.get("specialite")

        if specialite_filter and specialite_filter != "Toutes":
            queryset = queryset.filter(specialite=self.request.GET.get("specialite"))

        return queryset