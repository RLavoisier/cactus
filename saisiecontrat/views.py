# coding: utf-8
from copy import deepcopy

import os
from wsgiref.util import FileWrapper

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse

from django.shortcuts import render, redirect
from datetime import datetime

from django.template.loader import render_to_string
from django.urls import reverse

from django.views.generic import ListView, DetailView

from django.conf import settings
from saisiecontrat.forms import CreationContratForm, CreationEntrepriseForm, CreationAlternantForm, InformationContratForm, InformationMissionForm, ValidationMissionForm
from saisiecontrat.models import Contrat, Alternant, Entreprise, ConventionCollective, Personnel, Formation, CFA, SMIC
from django.core.exceptions import ObjectDoesNotExist

from saisiecontrat.utils.helper import creerfichemission, creerrecapinscriptions, creerexportypareo, \
    informe_saisie_complete, entreprise_complet, alternant_complet, contrat_complet, mission_complet, formation_complet, \
    creerexporttotal, contrat_ypareo_complet, creerCERFA
from saisiecontrat.utils.pdf_generator import PDFGenerator
from raven.contrib.django.raven_compat.models import client as sentry_client


def creationcontrat(request):


    if not request.user.is_authenticated:
        # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
        return redirect("comptes:login")

    # EXEMPLE DE FORMULAIRE GERE SANS RECOURS AUX MODELSFORMS

    context = {}
    context["nomonglet"] = "Accueil"

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
                                type_contrat_avenant=form.cleaned_data['type_contrat_avenant'],
                                mode_contractuel=form.cleaned_data['mode_contractuel'],
                                numero_contrat_anterieur=form.cleaned_data['numero_contrat_anterieur'],
                                date_effet_avenant=form.cleaned_data['date_effet_avenant'],
                                )
                contrat.save()

                contrat_a_afficher = contrat
                informe_saisie_complete(request)

                messages.add_message(request, messages.SUCCESS, "Le contrat a bien été créé vous pouvez maintenant le compléter dans les onglets suivants.")

            else:
                # copy l'objet (si on écrit nouveaucontrat=contrat on crée juste un pointeur sur contrat)
                # Cette syntaxe python fonctionne sur tout type d'objet et  dictionnaire
                nouveaucontrat = deepcopy(contrat)

                nouveaucontrat.id=None
                nouveaucontrat.type_contrat_avenant = request.POST['type_contrat_avenant']
                nouveaucontrat.mode_contractuel = request.POST['mode_contractuel']
                nouveaucontrat.numero_contrat_anterieur = request.POST['numero_contrat_anterieur']
                if form.cleaned_data['date_effet_avenant']:
                    nouveaucontrat.date_effet_avenant = form.cleaned_data['date_effet_avenant']

                nouveaucontrat.save()

                contrat.contrat_courant = False
                contrat.save()

                contrat_a_afficher = nouveaucontrat

                informe_saisie_complete(request)

                messages.add_message(request, messages.SUCCESS,
                                     "Un contrat a bien été créé. Les données du contrat précédent on été reprises vous pouver modifier les données dans les onglets suivants.")

            form = CreationContratForm(initial={
                "type_contrat_avenant": contrat_a_afficher.type_contrat_avenant,
                "mode_contractuel": contrat_a_afficher.mode_contractuel,
                "numero_contrat_anterieur": contrat_a_afficher.numero_contrat_anterieur,
                "date_effet_avenant": contrat_a_afficher.date_effet_avenant,
            })

            context["form"] = form
            context["contrat"] = contrat
            informe_saisie_complete(request)

            return render(request, 'creationcontrat.html', context)
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
                "date_effet_avenant": contrat.date_effet_avenant,
            })
        else:
            form = CreationContratForm()

        context["form"] = form
        context["contrat"]=contrat

        informe_saisie_complete(request)

        return render(request, 'creationcontrat.html', context)

def create_entreprise(request):

    if not request.user.is_authenticated:
        # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
        return redirect("comptes:login")

    context = {}
    context["nomonglet"] = "Votre employeur"

    if len(request.POST) > 0:

        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée
        form = CreationEntrepriseForm(request.POST)

        alternant = request.user.alternant
        contrat = alternant.contrat_courant
        entreprise = contrat.entreprise

        if form.is_valid():

            # Ici, on sauvegarde le formulaire, ce qui nous renvoie automatiquement
            # un nouvel objet entreprise


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
            entreprise.libelle_convention_collective = form.cleaned_data["libelle_convention_collective"]
            entreprise.code_convention_collective = form.cleaned_data["code_convention_collective"]
            entreprise.adhesion_regime_assurance_chomage = form.cleaned_data["adhesion_regime_assurance_chomage"]
            if form.cleaned_data["type_employeur"] in (11, 12, 13, 14, 15, 16):
                entreprise.secteur_employeur = 1
            else:
                entreprise.secteur_employeur = 2

            if not entreprise.libelle_convention_collective:
                if entreprise.code_convention_collective:
                    try:
                        conventioncollective = ConventionCollective.objects.get(code=entreprise.code_convention_collective)
                    except ObjectDoesNotExist:
                        conventioncollective = None

                    if conventioncollective:
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
                                      date_naissance=form.cleaned_data["date_naissance_ma_1"],
                                      role=2)
                personnel.save()
            else:
                personnel.civilite = request.POST.get("civilite_ma_1")
                personnel.nom = request.POST.get("nom_ma_1")
                personnel.prenom = request.POST.get("prenom_ma_1")
                personnel.date_naissance = form.cleaned_data["date_naissance_ma_1"]
                personnel.save()

            if not request.POST.get("nom_ma_2") is None:
                try:
                    personnel = Personnel.objects.get(entreprise=entreprise, role=3)
                except ObjectDoesNotExist:
                    personnel = None

                if personnel is None:
                    personnel = Personnel(entreprise=entreprise,
                                          civilite=request.POST.get("civilite_ma_2"),
                                          nom=request.POST.get("nom_ma_2"),
                                          prenom=request.POST.get("prenom_ma_2"),
                                          date_naissance=form.cleaned_data["date_naissance_ma_2"],
                                          role=3)
                    personnel.save()
                else:
                    personnel.civilite = request.POST.get("civilite_ma_2")
                    personnel.nom = request.POST.get("nom_ma_2")
                    personnel.prenom = request.POST.get("prenom_ma_2")
                    personnel.date_naissance = form.cleaned_data["date_naissance_ma_2"]
                    personnel.save()

            if not request.POST.get("nom_contact") is None:
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
                    personnel.courriel = request.POST.get("courriel_contact")
                    personnel.save()

            messages.add_message(request, messages.SUCCESS, "Les données de l'employeur ont été enregistrées.")

            request.session["entreprisecomplet"]=entreprise_complet(entreprise)
            request.session["accordvalide"] = (contrat.avis_raf == 2)

            # le redirect affiche la page comme sur un GET celà revient à envoyer l'exécution à la ligne du else:*
            # diu test if len(request.POST) > 0: (comme si on demandait l'affichait l'affichage
            return redirect(reverse("creationentreprise"))
        else:
            context["form"] = form
            context["contrat"] = contrat
            request.session["entreprisecomplet"]=False

            return render(request, "entreprise_form.html", context)
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

        if personnel is not None:
            form.fields["civilite_ma_2"].initial = personnel.civilite
            form.fields["nom_ma_2"].initial = personnel.nom
            form.fields["prenom_ma_2"].initial = personnel.prenom
            form.fields["date_naissance_ma_2"].initial = personnel.date_naissance

        try:
            personnel = Personnel.objects.get(entreprise=entreprise, role=4)
        except ObjectDoesNotExist:
            personnel = None

        if personnel is not None:
            form.fields["civilite_contact"].initial = personnel.civilite
            form.fields["nom_contact"].initial = personnel.nom
            form.fields["prenom_contact"].initial = personnel.prenom
            form.fields["courriel_contact"].initial = personnel.courriel


        context["form"] = form
        context["contrat"] = contrat
        return render(request, "entreprise_form.html", context)

        #return render(request, "entreprise_form.html", {"form": form})

def create_alternant(request):

    if not request.user.is_authenticated:
        # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
        return redirect("comptes:login")

    context={}
    context["nomonglet"] = "Vous"

    if len(request.POST) > 0:
        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée

        form = CreationAlternantForm(request.POST)

        if form.is_valid():

            alternant = request.user.alternant
            contrat = alternant.contrat_courant

            alternant.nom = form.cleaned_data["nom"]
            alternant.prenom = form.cleaned_data["prenom"]
            alternant.sexe = form.cleaned_data["sexe"]
            alternant.date_naissance = form.cleaned_data["date_naissance"]
            alternant.commune_naissance = form.cleaned_data["commune_naissance"]
            alternant.numero_departement_naissance = form.cleaned_data["numero_departement_naissance"]
            alternant.adresse_numero = form.cleaned_data["adresse_numero"]
            alternant.adresse_voie = form.cleaned_data["adresse_voie"]
            alternant.code_postal = form.cleaned_data["code_postal"]
            alternant.ville = form.cleaned_data["ville"]
            alternant.telephone = form.cleaned_data["telephone"]
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

            context["form"] = form
            context["contrat"] = contrat
            context["nationalite"] = alternant.nationalite

            messages.add_message(request, messages.SUCCESS, "Vos données ont bien été enregistrées.")

            if alternant.handicape:
                messages.add_message(request, messages.INFO, "Vous avez coché la case travailleur handicapé, n'hésitez pas à contacter Céline Grimaud (celine.grimaud@cfa-epure.com), la référente handicap du CFA Epure.")

            request.session["alternantcomplet"]=alternant_complet(alternant)
            request.session["accordvalide"] = (contrat.avis_raf == 2)

            return render(request, "alternant_form.html", context)
        else:

            alternant = request.user.alternant
            contrat = alternant.contrat_courant

            context["form"] = form
            context["contrat"] = contrat
            request.session["alternantcomplet"]=False

            return render(request, "alternant_form.html", context)

    else:

        form = CreationAlternantForm(instance=request.user.alternant)

        context["form"] = form
        contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)
        context["contrat"] = contrat

        return render(request, "alternant_form.html", context)

def inform_contrat(request):

    if not request.user.is_authenticated:
        # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
        return redirect("comptes:login")

    context = {}
    context["nomonglet"] = "Les données de votre contrat"

    if len(request.POST) > 0:

        form = InformationContratForm(request.POST, request=request)

        if form.is_valid():

            contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)

            contrat.type_derogation = form.cleaned_data["type_derogation"]
            contrat.date_embauche = form.cleaned_data["date_embauche"]
            contrat.date_debut_contrat = form.cleaned_data["date_debut_contrat"]
            contrat.date_effet_avenant = form.cleaned_data["date_effet_avenant"]
            contrat.date_fin_contrat = form.cleaned_data["date_fin_contrat"]
            contrat.duree_hebdomadaire_travail_heures = form.cleaned_data["duree_hebdomadaire_travail_heures"]
            contrat.duree_hebdomadaire_travail_minutes = form.cleaned_data["duree_hebdomadaire_travail_minutes"]
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

            context["form"] = form
            context["contrat"] = contrat

            messages.add_message(request, messages.SUCCESS, "Les données de votre contrat ont bien été enregistrées.")
            request.session["contratcomplet"] = contrat_complet(contrat)
            request.session["contratypareocomplet"] = contrat_ypareo_complet(contrat)
            request.session["accordvalide"] = (contrat.avis_raf == 2)

            return render(request, "contrat_form.html", context)
        else:
            context["form"] = form
            contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)
            context["contrat"] = contrat

            request.session["contratcomplet"]=False
            request.session["contratypareocomplet"] = False

            return render(request, "contrat_form.html", context)
    else:

        contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)

        if not contrat.date_debut_contrat:
            messages.add_message(request, messages.INFO,
                                "Les seules données obligatoire pour valider cet écran sont les dates de début et de fin de contrat. "
                                "Commencez par informer le type de dérogation (si nécessaire) ainsi que les dates de début "
                                "et de fin de contrat. Cette saisie permettra le pré-remplissage du tableau de rémunération. "
                                "Nous vous rappelons que les pourcentages ainsi que la rémunération mensuelle sont des minima ; modifiez-les au besoin. "
                                "Suivant la convention collective, la base de calcul de la rémunération peut être le SMIC (valeur par défaut) ou le Salaire Minimum Conventionnel (SMC). Attention ! la base peut changer en cours de contrat.")

        # dans le formulaire on utilise l'objet user de la request qui n'existe pas dans le formulaire
        form = InformationContratForm(instance=contrat, request=request)

        context["form"] = form
        context["contrat"] = contrat

        request.session["contratcomplet"] = contrat_complet(contrat)
        request.session["accordvalide"] = (contrat.avis_raf == 2)

        return render(request, "contrat_form.html", context)


def cerfa(request):

    if not request.user.is_authenticated:
        # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
        return redirect("comptes:login")

    context = {}
    context["nomonglet"] = "Votre CERFA"


    contrat = request.user.alternant.get_contrat_courant()

    context["contrat"] = contrat

    return render(request, "cerfa_form.html", context)


def inform_mission(request):

    if not request.user.is_authenticated:
        # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
        return redirect("comptes:login")

    context={}
    context["nomonglet"] = "Votre mission/Validation"

    contrat = request.user.alternant.get_contrat_courant()

    if len(request.POST) > 0:

        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée

        form = InformationMissionForm(request.POST)

        if contrat.mission != request.POST.get("mission"):
            #if form.is_valid():
            alternant = request.user.alternant
            contrat = alternant.contrat_courant
            contrat.mission = request.POST.get("mission")
            contrat.avis_raf=0
            contrat.date_maj_mission=datetime.now()
            contrat.date_maj=datetime.now()
            contrat.save()
            #context["boutonenvoiactif"] = (len(contrat.mission) >= 100)
            context["boutonenvoiactif"] = True
            messages.add_message(request, messages.SUCCESS, "La mission a bien été enregistrée.")
            request.session["missioncomplet"] = mission_complet(contrat)
            request.session["accordvalide"] = (contrat.avis_raf == 2)
            #else:
            #    context["boutonenvoiactf"] = False
            #    request.session["missioncomplet"] = False
        else:
            context["boutonenvoiactif"] = True
            #context["boutonenvoiactif"] = (len(contrat.mission) >= 100)
    else:
        contrat = Contrat.objects.get(alternant=request.user.alternant, contrat_courant=True)
        form = InformationMissionForm(instance=contrat)
        #context["boutonenvoiactif"] = (len(contrat.mission) >= 100)
        context["boutonenvoiactif"] = True
        request.session["missioncomplet"] = mission_complet(contrat)
        request.session["accordvalide"] = (contrat.avis_raf == 2)

    context["form"] = form
    context["contrat"] = contrat

    i=0
    while contrat.avis_raf != Contrat.AVIS_RAF[i][0]:
        i += 1

    context["libelle_avis_raf"] = Contrat.AVIS_RAF[i][1]

    return render(request, "mission_form.html", context)


class liste_formation(LoginRequiredMixin, ListView):

    queryset = Formation.objects.order_by("code_formation")
    template_name = "formations_list.html"
    # variable contenant les objets pour les passer au template
    context_object_name = "formations"

    def get(self, request, *args, **kwargs):
        # Si une formation est déjà choisie on redirige l'utilisateur
        if request.user.alternant.contrat_courant.formation:
            return redirect("detail_formation")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        # super fait référence à la classe mère ListView
        context = super().get_context_data(object_list=None, **kwargs)
        specialites = Formation.objects.order_by("specialite").values_list("specialite", flat=True).distinct()
        villes = Formation.objects.order_by("ville").values_list("ville", flat=True).distinct()

        # Selection des diplômes dispo en base
        diplomes_base = Formation.objects.order_by("diplome").values_list("diplome", flat=True).distinct()
        diplomes = tuple(t for t in Formation.DIPLOME
                    if t[0] in diplomes_base)

        context["specialites"] = ["Toutes"] + list(specialites)
        context["villes"] = ["Toutes"] + list(villes)
        context["diplomes"] = ((0, "Tous"),) + diplomes
        context["request"] = self.request

        alternant = self.request.user.alternant
        contrat = alternant.contrat_courant
        context["contrat"] = contrat
        context["nomonglet"] = "Votre formation"

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
            if filter and filter not in ["Toutes", "0"]:
                queryset = queryset.filter(**{attr: filter})

        return queryset

class detail_formation(LoginRequiredMixin, DetailView):
    model = Formation
    template_name = ("detail_formation.html")
    context_object_name = "formation"

    def get_object(self, queryset=None):
        alternant = self.request.user.alternant

        # self.contrat permet de récupérer le contrat ailleurs dans la class
        self.contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)

        if not self.contrat.formation:
            if alternant.code_acces:
                try:
                    f = Formation.objects.get(code_acces=alternant.code_acces)
                    self.contrat.formation = f
                    self.contrat.save()
                except ObjectDoesNotExist:
                    sentry_client.captureException()

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

        i=0
        if context.get("formation").inspection_pedagogique_competente is not None:
            while context.get("formation").inspection_pedagogique_competente != Formation.INSPECTION_PEDAGOGIQUE[i][0]:
                i+=1

        context["libelle_inspection_pedagogique_competente"] = Formation.INSPECTION_PEDAGOGIQUE[i][1]

        alternant = request.user.alternant
        contrat = alternant.contrat_courant
        context["contrat"] = contrat
        context["nomonglet"] = "Votre formation"

        request.session["formationcomplet"] = formation_complet(contrat)
        request.session["accordvalide"] = (contrat.avis_raf == 2)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        nombre_annee = self.request.POST.get("nombre_annees")
        alternant = request.user.alternant
        contrat = alternant.contrat_courant
        contrat.nombre_annees = nombre_annee
        contrat.save()

        messages.add_message(request, messages.SUCCESS, "Vos données ont bien été enregistrées.")

        request.session["formationcomplet"] = formation_complet(contrat)
        request.session["accordvalide"] = (contrat.avis_raf == 2)

        return redirect("detail_formation")


class appliquer_formation(LoginRequiredMixin, DetailView):

    model = Formation

    def get(self, request, *args, **kwargs):

        # Cette vue ne sert qu'a enregistrer la formation sélectionnée dans le contrat actuel
        self.object = self.get_object()

        contrat = self.request.user.alternant.get_contrat_courant()

        if contrat:
            contrat.formation = self.object

            contrat.date_debut_contrat = None
            contrat.date_fin_contrat = None

            contrat.duree_hebdomadaire_travail_heures = None
            contrat.duree_hebdomadaire_travail_minutes = None

            contrat.salaire_minimum_conventionnel = None
            contrat.salaire_brut_mensuel = None
            contrat.caisse_retraite_complementaire = None
            contrat.nourriture = None
            contrat.logement = None
            contrat.prime_panier = None
            contrat.an_1_per_1_du = None
            contrat.an_1_per_1_au = None
            contrat.an_1_per_1_taux = None
            contrat.an_1_per_1_base = 1
            contrat.an_1_per_2_du = None
            contrat.an_1_per_2_au = None
            contrat.an_1_per_2_taux = None
            contrat.an_1_per_2_base = 1
            contrat.an_2_per_1_du = None
            contrat.an_2_per_1_au = None
            contrat.an_2_per_1_taux = None
            contrat.an_2_per_1_base = 1
            contrat.an_2_per_2_du = None
            contrat.an_2_per_2_au = None
            contrat.an_2_per_2_taux = None
            contrat.an_2_per_2_base = 1
            contrat.an_3_per_1_du = None
            contrat.an_3_per_1_au = None
            contrat.an_3_per_1_taux = None
            contrat.an_3_per_1_base = 1
            contrat.an_3_per_2_du = None
            contrat.an_3_per_2_au = None
            contrat.an_3_per_2_taux = None
            contrat.an_3_per_2_base = 1
            contrat.an_4_per_1_du = None
            contrat.an_4_per_1_au = None
            contrat.an_4_per_1_taux = None
            contrat.an_4_per_1_base = 1
            contrat.an_4_per_2_du = None
            contrat.an_4_per_2_au = None
            contrat.an_4_per_2_taux = None
            contrat.an_4_per_2_base = 1
            contrat.date_saisie_complete = None
            contrat.nombre_annees = None
            contrat.avis_raf = 0
            contrat.date_validation_raf = None

            contrat.save()

        request.session["contratcomplet"] = contrat_complet(contrat)
        request.session["contratypareocomplet"] = contrat_ypareo_complet(contrat)
        request.session["formationcomplet"] = formation_complet(contrat)
        request.session["accordvalide"] = (contrat.avis_raf == 2)

        return redirect("detail_formation")


class telechargerCERFA(LoginRequiredMixin, DetailView):

    model = Contrat

    def get(self, request, *args, **kwargs):


        nomfichier = creerCERFA(request.user.alternant, True)

        filepath = os.path.join(settings.PDF_OUTPUT_DIR, nomfichier)

        with open(filepath, "rb") as file:
            response = HttpResponse(FileWrapper(file), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s' % nomfichier

        os.remove(filepath)

        return response

def envoyermailvalidationraf(request):

# Cette vue est appelée depuis l'écran mission

    alternant = request.user.alternant
    contrat = alternant.get_contrat_courant()

    if request.session["contratypareocomplet"] and request.session["alternantcomplet"] and request.session["entreprisecomplet"] and request.session["formationcomplet"]:

        #if len(contrat.mission) > 100:
        contrat.avis_raf = 1
        contrat.motif = None
        contrat.date_envoi_raf = datetime.now()
        contrat.save()

        creerfichemission(request, alternant.hash)

        messages.add_message(request, messages.SUCCESS, "Un mail a été envoyé au responsable de formation pour qu'il valide votre dossier.")
        #else:

        #    messages.add_message(request, messages.INFO, "La mission doit être renseignée et comporter au moins 100 caractères.")

        return redirect("informationmission")

    else:
        # On pourrait aussi compléter la form pour éviter d'afficher le bouton si les données ne sont pas complètes

        form = InformationMissionForm(instance=contrat)
        context = {}
        context["nomonglet"] = "Votre mission/Validation"
        context["boutonenvoiactif"] = True
        request.session["missioncomplet"] = mission_complet(contrat)
        request.session["accordvalide"] = (contrat.avis_raf == 2)
        context["form"] = form
        context["contrat"] = contrat

        i = 0
        while contrat.avis_raf != Contrat.AVIS_RAF[i][0]:
            i += 1

        context["libelle_avis_raf"] = Contrat.AVIS_RAF[i][1]

        messages.add_message(request, messages.ERROR,"Veuillez compléter les données des onglets avant de faire la demande de validation.")

        return render(request, "mission_form.html", context)


def choisirautreformation(request):

# Cette vue est appelée depuis l'écran mission


    alternant = request.user.alternant
    contrat = alternant.get_contrat_courant()
    # print (contrat.formation.code_formation)
    contrat.formation = None
    contrat.save()

    request.session["formationcomplet"] = formation_complet(contrat)
    request.session["accordvalide"] = (contrat.avis_raf == 2)

    return redirect("liste_formation")


def envoyerficheraf(request, alternant_hash):

    creerfichemission(request,alternant_hash)

    messages.add_message(request, messages.SUCCESS, "Un mail a été généré avec la fiche mission demandée. S'il n'apparaît pas dans votre boîte de réception, vérifiez le dossier des éléments indésirables.")

    return render(request, "message.html")

def validationmission(request, alternant_hash):

    alternant=Alternant.objects.get(hash=alternant_hash)
    contrat = alternant.contrat_courant

    if len(request.POST) > 0:

        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée

        form = ValidationMissionForm(request.POST)

        if form.is_valid():
            if contrat.avis_raf == 2 or contrat.avis_raf == 3 or contrat.avis_raf == 4:
                messages.add_message(request, messages.INFO, "Un avis a déjà été enregistré sur cette mission.")
            else:
                contrat.motif = form.cleaned_data["motif"]
                contrat.avis_raf = form.cleaned_data["validation"]
                contrat.date_validation_raf=datetime.now()
                contrat.save()

                i = 0
                while str(contrat.avis_raf) != str(Contrat.AVIS_RAF[i][0]):
                    i += 1

                libelle_avis_raf = Contrat.AVIS_RAF[i][1]

                context = {}
                context["libelle_avis_raf"] = libelle_avis_raf
                context["contrat"] = contrat
                formation = contrat.formation
                context["formation"] = formation
                context["request"] = request

                msg_plain = render_to_string('informationmission_alternant.txt', context)
                msg_html = render_to_string('informationmission_alternant.html', context)

                # Création du mail
                email = EmailMultiAlternatives(
                    libelle_avis_raf,
                    msg_plain,
                    'cactus.test.tg@gmail.com',
                    [alternant.user.email],
                )

                # Ajout du format html (https://docs.djangoproject.com/fr/2.0/topics/email/#sending-alternative-content-types)
                email.attach_alternative(msg_html, "text/html")

                email.send(fail_silently=True)

                messages.add_message(request, messages.SUCCESS, "Votre avis a bien été enregistré.")

    else:
        form = ValidationMissionForm(instance=contrat)

    context={}
    context["form"] = form
    context["contrat"] = contrat
    context["nom_alternant"]=contrat.alternant.nom
    context["prenom_alternant"]=contrat.alternant.prenom
    context["telephone_alternant"]=contrat.alternant.telephone
    context["courriel_alternant"]=contrat.alternant.user.email
    context["nom_formation"]=contrat.formation.intitule_formation
    context["raison_sociale_entreprise"]=contrat.entreprise.raison_sociale
    context["ville_entreprise"]=contrat.entreprise.ville
    context["numero_SIRET_entreprise"]=contrat.entreprise.numero_SIRET
    context["telephone_entreprise"]=contrat.entreprise.telephone
    context["courriel_entreprise"]=contrat.entreprise.courriel

    context["mission"]=contrat.mission

    return render(request, "validation_mission_form.html", context)


def recapinscriptions(request, formation_hash):

    creerrecapinscriptions(request,formation_hash)

    messages.add_message(request, messages.SUCCESS, "Un mail a été généré avec la liste actualisée des inscriptions. S'il n'apparaît pas dans votre boîte de réception, vérifiez le dossier des éléments indésirables.")

    return render(request, "message.html")

def exportypareo(request, cfa_hash,email_livraison, aaaammjj_du, aaaammjj_au, extraction, etat):

    try:
        CFA.objects.get(hash=cfa_hash)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR,"L'URL est erronée.")
        return render(request, "message.html")

    creerexportypareo(request, email_livraison, aaaammjj_du, aaaammjj_au, extraction, etat)

    messages.add_message(request, messages.SUCCESS, "Un mail a été généré avec le fichier csv joint. S'il n'apparaît pas dans votre boîte de réception, vérifiez le dossier des éléments indésirables.")

    return render(request, "message.html")

def exporttotal(request, cfa_hash,email_livraison):

    try:
        CFA.objects.get(hash=cfa_hash)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR,"L'URL est erronée.")
        return render(request, "message.html")

    creerexporttotal(request, email_livraison)

    messages.add_message(request, messages.SUCCESS, "Un mail a été généré avec le fichier csv joint. S'il n'apparaît pas dans votre boîte de réception, vérifiez le dossier des éléments indésirables.")

    return render(request, "message.html")
