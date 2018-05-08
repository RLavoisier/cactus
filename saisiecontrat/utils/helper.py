from datetime import datetime
import os
import csv

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from saisiecontrat.models import Alternant,  Personnel, Contrat, Formation
from django.core.exceptions import ObjectDoesNotExist

from saisiecontrat.utils.pdf_generator import PDFGenerator


def generer_data_pour_pdf_mission(alternant, email, entreprise, ma_1, contrat):

    data = {}

    data["formation"] = contrat.formation.intitule_formation

    if alternant.adresse_numero is not None:
        data["voie"] = "%s %s" % (alternant.adresse_numero,alternant.adresse_voie)
    else:
        data["voie"] = alternant.adresse_voie
    data["codepostal"] = alternant.code_postal
    data["ville"] = alternant.ville
    data["neele"] = alternant.date_naissance.strftime('%d/%m/%Y')
    data["mail"] = email
    data["telephone"] = alternant.telephone
    data["nomprenom"] = "%s %s" % (alternant.nom, alternant.prenom)

    data["raisonsociale"] = entreprise.raison_sociale
    if entreprise.adresse_numero is not None:
        data["voie2"] = "%s %s" % (entreprise.adresse_numero,entreprise.adresse_voie)
    else:
        data["voie2"] = entreprise.adresse_voie
    if entreprise.adresse_complement is not None:
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

    return data

def creerfichemission(request,alternant_hash):

    alternant = Alternant.objects.get(hash=alternant_hash)
    contrat = alternant.get_contrat_courant()
    entreprise = contrat.entreprise
    formation = contrat.formation

    try:
        ma_1 = Personnel.objects.get(entreprise=entreprise, role=2)
    except ObjectDoesNotExist:
        ma_1 = None

    data = generer_data_pour_pdf_mission(alternant, alternant.user.email, entreprise, ma_1, contrat)

    filename = "Fiche mission %s %s.pdf" % (alternant.nom, alternant.prenom)
    filename = filename.replace(' ', '_')
    filename = filename.replace("'", "_")

    nomfichier = PDFGenerator.generate_mission_pdf_with_datas(filename, data, flatten=True)

    context={}

    context["alternant"] = alternant
    context["formation"] = formation

    contrats = Contrat.objects.filter(formation=formation, avis_raf=1)
    alternants = [c.alternant for c in contrats]

    context["alternants"] = alternants
    context["request"] = request

    msg_plain = render_to_string('information_raf.txt', context)
    msg_html = render_to_string('information_raf.html', context)

    # Création du mail
    email = EmailMultiAlternatives(
        "Fiche mission de %s %s.pdf" % (alternant.nom, alternant.prenom),
        msg_plain,
        'cactus.test.tg@gmail.com',
        [formation.courriel_raf],
    )

    # Ajout du format html (https://docs.djangoproject.com/fr/2.0/topics/email/#sending-alternative-content-types)
    email.attach_alternative(msg_html, "text/html")

    email.attach_file(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))

    email.send(fail_silently=True)

    try:
        os.remove(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))
    except:
        pass

def creerrecapinscriptions(request,formation_hash):

    formation = Formation.objects.get(hash=formation_hash)
    contrats = Contrat.objects.filter(formation=formation)
    alternants = [{"nom": c.alternant.nom, "prenom": c.alternant.prenom, "hash": c.alternant.hash, "avis_raf": c.avis_raf} for c in contrats]

    context={}

    context["formation"] = formation
    context["alternants"] = alternants
    context["request"] = request

    msg_plain = render_to_string('recapinscriptions_raf.txt', context)
    msg_html = render_to_string('recapinscriptions_raf.html', context)

    # Création du mail
    email = EmailMultiAlternatives(
        "Récapitulatif des dossiers d'inscription",
        msg_plain,
        'cactus.test.tg@gmail.com',
        [formation.courriel_raf],
    )

    # Ajout du format html (https://docs.djangoproject.com/fr/2.0/topics/email/#sending-alternative-content-types)
    email.attach_alternative(msg_html, "text/html")

    email.send(fail_silently=True)


def creerexportypareo(request,email_livraison,aaaammjj_du,aaaammjj_au,extraction,etat):

    if etat==9:
        liste_etat = [0,1,2,3,4]
    else:
        liste_etat = [etat]

    date_du = datetime(int(aaaammjj_du[0:4]),int(aaaammjj_du[4] + aaaammjj_du[5]),int(aaaammjj_du[6] + aaaammjj_du[7]))
    date_au = datetime(int(aaaammjj_au[0:4]),int(aaaammjj_au[4] + aaaammjj_au[5]),int(aaaammjj_au[6] + aaaammjj_au[7]))

    # get comme pour le filtre
    # Attention si plusieurs objets retournés => exception : multipleobjectreturn
    # si aucun exception DoesNotExist
    # On utilise un Try

    # Pour récupérer plusieurs objets spécifier un filter
    # contrats = Contrat.objects.filter()

    # RPour récupérer tout : all()

    # Avant
    # contrats = Contrat.objects.filter(avis_raf in [1], date_exportation_CFA is None)
    # Après

    if etat in [0,1,9]:
        if extraction == 9:
            contrats = Contrat.objects.filter(avis_raf__in=liste_etat)
        elif extraction == 0:
            contrats = Contrat.objects.filter(avis_raf__in=liste_etat, date_exportation_CFA=None)
        elif extraction == 1:
            contrats = Contrat.objects.filter(avis_raf__in=liste_etat).exclude(date_exportation_CFA=None)
    else:
        if extraction == 9:
            contrats = Contrat.objects.filter(avis_raf__in=liste_etat, date_validation_raf__gte=date_du, date_validation_raf__lte=date_au)
        elif extraction == 0:
            contrats = Contrat.objects.filter(avis_raf__in=liste_etat, date_validation_raf__gte=date_du, date_validation_raf__lte=date_au,date_exportation_CFA=None)
        elif extraction == 1:
            contrats = Contrat.objects.filter(avis_raf__in=liste_etat, date_validation_raf__gte=date_du, date_validation_raf__lte=date_au).exclude(date_exportation_CFA=None)

    # contrat = Contrat() crée l'objet sans save (si save on crée un nouvel objet donnée  si id=null)

    # Create créé l'objet + save en base
    # contrat = Contrat.objects.create(contrat_courant=True)

    nomfichier = "export_%s_%s_%i_%i.csv" % (aaaammjj_du, aaaammjj_au, extraction, etat)
    nomfichier = os.path.join(settings.PDF_OUTPUT_DIR, nomfichier)

    with open(nomfichier, "w") as f:

        c = csv.writer(f, delimiter="|")

        c.writerow(["",""])

        c.writerow(["CIVILITE",
                    "NOM JEUNE",
                    "PRENOM JEUNE",
                    "CIV REP LEG",
                    "NOM REP LEG",
                    "PRENOM LEG",
                    "AD1 JEUNE",
                    "AD2 JEUNE",
                    "CP JEUNE",
                    "VILLE JEUNE",
                    "DISTANCE",
                    "TEL JEUNE",
                    "DATE DE NAISSANCE",
                    "LIEU NAIS",
                    "DEP NAIS",
                    "NATION",
                    "GROUPE",
                    "CALENDRIER",
                    "SITUATION",
                    "DERNIER DIP",
                    "METIER",
                    "ORIGINE",
                    "QUAL",
                    "NUMERO CON",
                    "DATE DEB CONTRAT",
                    "DATE FIN CONT",
                    "DATE ENRE",
                    "DUREE",
                    "ENT",
                    "CIV REP",
                    "NOM REP",
                    "PRENOM REP",
                    "ADR 1 ENT",
                    "ADR2 ENT",
                    "CP ENT",
                    "VILLE ENT",
                    "TEL ENT",
                    "FAX ENT",
                    "NAF",
                    "SIRET",
                    "NB SAL",
                    "AFF ENT",
                    "CIV MA",
                    "NOM MA",
                    "PRENOM MA",
                    "DATE RESIL",
                    "MOTIF RESIL",
                    "DATE ENTREE GRP",
                    "DATE DEP CFA",
                    "NOM ETAB",
                    "CP ETAB",
                    "VILLE ETAB",
                    "ID EXT JEUNE",
                    "ID EXT CONTRAT",
                    "ID EXT ENT",
                    "ID EXT COMMUNE",
                    "ID EXT VILLE ENT",
                    "DATE DE NAISSANCE MA",
                    "QUALIFICATION MA",
                    "TELEPHONE 1 MA",
                    "TELEPHONE 2 MA",
                    "FAX MA",
                    "EMAIL MA",
                    "DATE DEPART MA",
                    "AUTRE ADR APP ADRESSE 1",
                    "AUTRE ADR APP ADRESSE 2",
                    "AUTRE ADR APP CP",
                    "AUTRE ADR APP VILLE",
                    "AUTRE ADR APP TEL 1",
                    "AUTRE ADR APP TEL 2",
                    "EMAIL APPRENANT",
                    "INE APPRENANT",
                    "TEL 2 ENTREPRISE",
                    "EMAIL 2 ENTREPRISE",
                    "SITE WEB ENTREPRISE",
                    "DUMMY"])

        print(len(contrats))

        for contrat in contrats:

            enr=[]

            alternant=contrat.alternant
            entreprise = contrat.entreprise
            maitreapprentissage = Personnel.objects.get(entreprise=entreprise,role=2)
            formation = contrat.formation

            #1 CIVILITE
            if alternant.sexe == "F":
                enr.append("Mme")
            else:
                enr.append("Mr")
            #2 NOM JEUNE
            enr.append(alternant.nom)
            #3 PRENOM JEUNE
            enr.append(alternant.prenom)
            # 4 CIV REP LEG
            if alternant.civilite_representant == 1:
                enr.append("Mme")
            elif alternant.civilite_representant == 2:
                enr.append("Mr")
            else:
                enr.append("")
            # 5 NOM REP LEG
            if alternant.nom_representant:
                enr.append(alternant.nom_representant)
            else:
                enr.append("")
            # 6 PRENOM LEG
            if alternant.prenom_representant:
                enr.append(alternant.prenom_representant)
            else:
                enr.append("")
            # 7 AD1 JEUNE
            enr.append("%s %s" % (alternant.adresse_numero, alternant.adresse_voie))
            # 8 AD2 JEUNE
            enr.append("")
            # 9 CP JEUNE
            enr.append(alternant.code_postal)
            # 10 VILLE JEUNE
            enr.append(alternant.ville)
            # 11 DISTANCE
            enr.append("0")
            # 12 TEL JEUNE
            enr.append(alternant.telephone)
            # 13 DATE DE NAISSANCE
            enr.append(alternant.date_naissance.strftime('%d/%m/%Y'))
            # 14 LIEU NAIS
            enr.append(alternant.commune_naissance)
            # 15 DEP NAIS
            enr.append(alternant.numero_departement_naissance)
            # 16 NATION
            if alternant.nationalite == 1:
                enr.append("FRANCAISE")
            elif alternant.nationalite == 2:
                enr.append("EUROPEENNE")
            elif alternant.nationalite == 3:
                enr.append("ETRANGERE HORS EUROPE")
            # 17 GROUPE
            enr.append("")
            # 18 CALENDRIER
            enr.append("")
            # 19 SITUATION
            enr.append("")
            # 20 DERNIER DIP
            enr.append(alternant.diplome_le_plus_eleve)
            # 21 METIER/CODE FORMATION
            codeformation= formation.code_formation + "_"
            enr.append(codeformation[0:codeformation.find("_")])
            # 22 ORIGINE
            if alternant.situation_avant_contrat == 10:
                enr.append("0117")
            elif alternant.situation_avant_contrat == 9:
                enr.append("0113")
            elif alternant.situation_avant_contrat == 8:
                enr.append("0111")
            elif alternant.situation_avant_contrat == 7:
                enr.append("0110")
            elif alternant.situation_avant_contrat == 6:
                enr.append("0117")
            elif alternant.situation_avant_contrat == 5:
                enr.append("5901")
            elif alternant.situation_avant_contrat == 4:
                enr.append("0999")
            elif alternant.situation_avant_contrat == 3:
                enr.append("0069")
                #if alternant.derniere_annee_suivie == 11 or alternant.derniere_annee_suivie == 12:
                #   annee = 1
                #elif alternant.derniere_annee_suivie == 21 or alternant.derniere_annee_suivie == 22:
                #    annee = 2
                #elif alternant.derniere_annee_suivie == 31 or alternant.derniere_annee_suivie == 32:
                #    annee = 3
                #elif alternant.derniere_annee_suivie == 1:
                #    if alternant.dernier_diplome_prepare == 39:
                #        annee = 2
                #    elif alternant.dernier_diplome_prepare == 32:
                #        annee = 2
                #    elif alternant.dernier_diplome_prepare == 31:
                #        annee = 2
                #    elif alternant.dernier_diplome_prepare == 29:
                #        annee = 3
                #    elif alternant.dernier_diplome_prepare == 24:
                #        annee = 3
                #    elif alternant.dernier_diplome_prepare == 23:
                #        annee = 1
                #    elif alternant.dernier_diplome_prepare == 22:
                #        annee = 2
                #    elif alternant.dernier_diplome_prepare == 21:
                #        annee = 2
                #    elif alternant.dernier_diplome_prepare == 19:
                #        annee = 2
                #    elif alternant.dernier_diplome_prepare == 12:
                #        annee = 2
                #    elif alternant.dernier_diplome_prepare == 11:
                #        annee = 2
                #enr.append("%s%s" % (alternant.dernier_diplome_prepare, annee))
            elif alternant.situation_avant_contrat == 2:
                enr.append("0999")
            elif alternant.situation_avant_contrat == 1:
                enr.append("%s%s" % (alternant.dernier_diplome_prepare, "1"))
            # 23 QUAL
            enr.append("DP")
            # 24 NUMERO CON --------------------------------------------------------------------------------A VOIR
            enr.append("")
            # 25 DATE DEB CONTRAT
            enr.append(contrat.date_debut_contrat.strftime('%d/%m/%Y'))
            # 26 DATE FIN CONT
            enr.append(contrat.date_fin_contrat.strftime('%d/%m/%Y'))
            # 27 DATE ENRE
            enr.append(datetime.now().strftime('%d/%m/%Y'))
            # 28 DUREE
            if contrat.nombre_annees is None:
                duree_an = formation.nombre_annees
            else:
                duree_an = contrat.nombre_annees
            enr.append(duree_an * 12)
            # 29 ENT
            enr.append(entreprise.raison_sociale)
            # 30 CIV REP
            enr.append("")
            # 31 NOM REP
            enr.append("")
            # 32 PRENOM REP
            enr.append("")
            # 33 ADR 1 ENT
            if entreprise.adresse_numero:
                enr.append("%s %s" % (entreprise.adresse_numero, entreprise.adresse_voie))
            else:
                enr.append(entreprise.adresse_voie)
            # 34 ADR2 ENT
            if entreprise.adresse_complement:
                enr.append(entreprise.adresse_complement)
            else:
                enr.append("")
            # 35 CP ENT
            enr.append(entreprise.code_postal)
            # 36 VILLE ENT
            enr.append(entreprise.ville)
            # 37 TEL ENT
            enr.append(entreprise.telephone)
            # 38 FAX ENT
            if entreprise.telecopie:
                enr.append(entreprise.telecopie)
            else:
                enr.append("")
            # 39 NAF
            enr.append(entreprise.code_APE)
            # 40 SIRET
            enr.append(entreprise.numero_SIRET)
            # 41 NB SAL
            enr.append(entreprise.effectif_entreprise)
            # 42 AFF ENT--------------------------------------------------------------------------------A VOIR
            enr.append("")
            # 43 CIV MA
            if alternant.civilite_representant == 1:
                enr.append("Mme")
            elif alternant.civilite_representant == 2:
                enr.append("Mr")
            else:
                enr.append("")
            # 44 NOM MA
            enr.append(maitreapprentissage.nom)
            # 45 PRENOM MA
            enr.append(maitreapprentissage.prenom)
            # 46 DATE RESIL
            enr.append("")
            # 47 MOTIF RESIL
            enr.append("")
            # 48 DATE ENTREE GRP--------------------------------------------------------------------------------A VOIR
            enr.append("")
            # 49 DATE DEP CFA
            enr.append("")
            # 50 NOM ETAB
            enr.append("")
            # 51 CP ETAB
            enr.append("")
            # 52 VILLE ETAB
            enr.append("")
            # 53 ID EXT JEUNE
            enr.append("")
            # 54 ID EXT CONTRAT
            enr.append("")
            # 55 ID EXT ENT
            enr.append("")
            # 56 ID EXT COMMUNE
            enr.append("")
            # 57 ID EXT VILLE ENT
            enr.append("")
            # 58 DATE DE NAISSANCE MA
            enr.append(maitreapprentissage.date_naissance.strftime('%d/%m/%Y'))
            # 59 QUALIFICATION MA
            enr.append("")
            # 60 TELEPHONE 1 MA
            enr.append("")
            # 61 TELEPHONE 2 MA
            enr.append("")
            # 62 FAX MA
            enr.append("")
            # 63 EMAIL MA
            enr.append("")
            # 64 DATE DEPART MA
            enr.append("")
            # 65 AUTRE ADR APP ADRESSE 1
            enr.append("")
            # 66 AUTRE ADR APP ADRESSE 2
            enr.append("")
            # 67 AUTRE ADR APP CP
            enr.append("")
            # 68 AUTRE ADR APP VILLE
            enr.append("")
            # 69 AUTRE ADR APP TEL 1
            enr.append("")
            # 70 AUTRE ADR APP TEL 2
            enr.append("")
            # 71 EMAIL APPRENANT
            enr.append(alternant.user.email)
            # 72 INE APPRENANT
            enr.append("")
            # 73 TEL 2 ENTREPRISE
            enr.append("")
            # 74 EMAIL 2 ENTREPRISE
            enr.append("")
            # 75 SITE WEB ENTREPRISE
            enr.append("")
            # 76 DUMMY
            enr.append("")

            c.writerow(enr)

    # Création du mail
    email = EmailMultiAlternatives(
        "cactus export ypareo",
        "",
        'cactus.test.tg@gmail.com',
        [email_livraison],
    )

    email.attach_file(nomfichier)

    email.send(fail_silently=True)

    if etat in [2] and extraction in [0]:
        for contrat in contrats:
            contrat.date_exportation_CFA =datetime.now()
            contrat.save()

    print(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))
    try:
        os.remove(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))
    except:
        pass

def alternant_complet(alternant):

    if alternant:

        i = 0

        if alternant.nom:
            i += 1
        if alternant.prenom:
            i += 1
        if alternant.adresse_voie:
            i += 1
        if alternant.code_postal:
            i += 1
        if alternant.ville:
            i += 1
        if alternant.telephone:
            i += 1
        if alternant.date_naissance:
            i += 1
        if alternant.sexe:
            i += 1
        if alternant.numero_departement_naissance:
            i += 1
        if alternant.commune_naissance:
            i += 1
        if alternant.regime_social:
            i += 1
        if alternant.nationalite:
            i += 1
        if alternant.situation_avant_contrat:
            i += 1
        if alternant.diplome_le_plus_eleve:
            i += 1
        if alternant.dernier_diplome_prepare:
            i += 1
        if alternant.intitule_dernier_diplome_prepare:
            i += 1
        if alternant.derniere_annee_suivie:
            i += 1
        return i == 17
    else:
        return False


def entreprise_complet(entreprise):

    if entreprise:

        i = 0

        if entreprise.raison_sociale:
            i += 1
        if entreprise.adresse_voie:
            i += 1
        if entreprise.code_postal:
            i += 1
        if entreprise.ville:
            i += 1
        if entreprise.telephone:
            i += 1
        if entreprise.numero_SIRET:
            i += 1
        if entreprise.code_APE:
            i += 1
        if entreprise.effectif_entreprise:
            i += 1
        if entreprise.type_employeur:
            i += 1
        if entreprise.courriel:
            i += 1
        if entreprise.code_convention_collective:
            i += 1
        if entreprise.libelle_convention_collective:
            i += 1

        try:
            personnel = Personnel.objects.get(entreprise=entreprise, role=2)
        except ObjectDoesNotExist:
            personnel = None

        if personnel:
            if personnel.nom:
                i += 1
            if personnel.prenom:
                i += 1
            if personnel.date_naissance:
                i += 1

        return i == 15
    else:
        return False


def formation_complet(contrat):

    if contrat.formation:
        return True
    else:
        return False


def mission_complet(contrat):

    if contrat.mission:
        if len(contrat.mission) >= 100:
            return True
        else:
            return False
    else:
        return False


def contrat_complet(contrat):


    if contrat:


        i = 0

        if contrat.date_debut_contrat:
            i += 1
        if contrat.date_fin_contrat:
            i += 1
        if contrat.date_embauche:
            i += 1
        if contrat.salaire_brut_mensuel:
            i += 1
        if contrat.caisse_retraite_complementaire:
            i += 1
        if contrat.duree_hebdomadaire_travail_heures:
            i += 1

        if i < 6:
            return False
        else:
            if contrat.formation:
                if contrat.nombre_annees:

                    nombre_annees = contrat.nombre_annees
                else:
                    nombre_annees = contrat.formation.nombre_annees
            else:
                return False

            j=0

            if contrat.an_1_per_1_du:
                j+=1
            if contrat.an_2_per_1_du:
                j+=1
            if contrat.an_3_per_1_du:
                j+=1
            if contrat.an_4_per_1_du:
                j+=1

            if j < nombre_annees:
                return False

            if contrat.an_1_per_1_du or contrat.an_1_per_1_au:
                if not contrat.an_1_per_1_base:
                    return False

            if contrat.an_1_per_2_du or contrat.an_1_per_2_au:
                if not contrat.an_1_per_2_base:
                    return False

            if contrat.an_2_per_1_du or contrat.an_2_per_1_au:
                if not contrat.an_2_per_1_base:
                    return False

            if contrat.an_2_per_2_du or contrat.an_2_per_2_au:
                if not contrat.an_2_per_2_base:
                    return False

            if contrat.an_3_per_1_du or contrat.an_3_per_1_au:
                if not contrat.an_3_per_1_base:
                    return False

            if contrat.an_3_per_2_du or contrat.an_3_per_2_au:
                if not contrat.an_3_per_2_base:
                    return False

            if contrat.an_4_per_1_du or contrat.an_4_per_1_au:
                if not contrat.an_4_per_1_base:
                    return False

            if contrat.an_4_per_2_du or contrat.an_4_per_2_au:
                if not contrat.an_4_per_2_base:
                    return False

            return True
    else:
        return False

def informe_saisie_complete(request):

    alternant = request.user.alternant
    request.session["alternantcomplet"] = alternant_complet(alternant)

    try:
        contrat = alternant.get_contrat_courant()
    except ObjectDoesNotExist:
        contrat = None

    if not contrat:
        request.session["contratcomplet"] = False
        request.session["formationcomplet"] = False
        request.session["missioncomplet"] = False
        request.session["entreprisecomplet"] = False
    else:
        request.session["contratcomplet"] = contrat_complet(contrat)
        request.session["formationcomplet"] = formation_complet(contrat)
        request.session["missioncomplet"] = mission_complet(contrat)

        if not contrat.entreprise:
            request.session["entreprisecomplet"] = False
        else:
            request.session["entreprisecomplet"] = entreprise_complet(contrat.entreprise)

    return request