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

    if len(contrat.mission) > 0:
        data["mission"] = contrat.mission
    else:
        data["mission"] = ''

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

    # Génération du CERFA non aplati

    nomfichier2 = creerCERFA(alternant, False)

    context={}

    context["alternant"] = alternant
    context["formation"] = formation

    contrats = Contrat.objects.filter(formation=formation, avis_raf=1, contrat_courant=True)
    alternants = [c.alternant for c in contrats]

    context["alternants"] = alternants
    context["request"] = request

    msg_plain = render_to_string('information_raf.txt', context)
    msg_html = render_to_string('information_raf.html', context)

    # Création du mail
    email = EmailMultiAlternatives(
        "Validation du dossier de %s %s.pdf" % (alternant.nom, alternant.prenom),
        msg_plain,
        'CFA Epure<no_reply@cfa-epure.com>',
        formation.courriel_raf.split(','),
    )

    # Ajout du format html (https://docs.djangoproject.com/fr/2.0/topics/email/#sending-alternative-content-types)
    email.attach_alternative(msg_html, "text/html")

    email.attach_file(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))

    email.attach_file(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier2))

    email.send(fail_silently=True)

    try:
        os.remove(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))
    except:
        pass

    try:
        os.remove(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier2))
    except:
        pass


def creerrecapinscriptions(request,formation_hash):

    formation = Formation.objects.get(hash=formation_hash)
    contrats = Contrat.objects.filter(formation=formation, contrat_courant=True)
    #alternants = [{"nom": c.alternant.nom, "prenom": c.alternant.prenom, "hash": c.alternant.hash, "avis_raf": c.avis_raf} for c in contrats]
    alternants = sorted([{"nom": c.alternant.nom, "prenom": c.alternant.prenom, "hash": c.alternant.hash, "avis_raf": c.avis_raf} for c in contrats], key=lambda a: a["nom"] or '')

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
        'CFA Epure<no_reply@cfa-epure.com>',
        formation.courriel_raf.split(','),
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

    #print(etat)
    #print(liste_etat)
    #print(extraction)
    #print(date_du)
    #print(date_au)

    if etat in [0,1,9]:
        if extraction == 9:
            contrats = Contrat.objects.filter(contrat_courant=True, avis_raf__in=liste_etat)
        elif extraction == 0:
            contrats = Contrat.objects.filter(contrat_courant=True, avis_raf__in=liste_etat, date_exportation_CFA=None)
        elif extraction == 1:
            contrats = Contrat.objects.filter(contrat_courant=True, avis_raf__in=liste_etat).exclude(date_exportation_CFA=None)
    else:
        if extraction == 9:
            contrats = Contrat.objects.filter(contrat_courant=True, avis_raf__in=liste_etat, date_validation_raf__gte=date_du, date_validation_raf__lte=date_au)
        elif extraction == 0:
            contrats = Contrat.objects.filter(contrat_courant=True, avis_raf__in=liste_etat, date_validation_raf__gte=date_du, date_validation_raf__lte=date_au,date_exportation_CFA=None)
        elif extraction == 1:
            contrats = Contrat.objects.filter(contrat_courant=True, avis_raf__in=liste_etat, date_validation_raf__gte=date_du, date_validation_raf__lte=date_au).exclude(date_exportation_CFA=None)

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
            enr.append(alternant.nom.upper())
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

            if alternant.adresse_numero:
                if alternant.adresse_voie:
                    adresse = "%s %s" % (alternant.adresse_numero, alternant.adresse_voie)
                else:
                    adresse = "%s" % (alternant.adresse_numero)
            else:
                if alternant.adresse_voie:
                    adresse = "%s" % (alternant.adresse_voie)
                else:
                    adresse = ""

            # 7 AD1 JEUNE
            # 8 AD2 JEUNE
            if len(adresse) > 38:
                enr.append(adresse[:38])
                enr.append(adresse[38:])
            else:
                enr.append(adresse)
                enr.append("")

            # 9 CP JEUNE
            enr.append(alternant.code_postal)
            # 10 VILLE JEUNE
            enr.append(alternant.ville.upper())
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
            enr.append(formation.situation_entree)
            # 20 DERNIER DIP
            enr.append(alternant.diplome_le_plus_eleve)
            # 21 METIER/CODE FORMATION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            enr.append(formation.code_formation[0:9])
            # 22 ORIGINE
            #print(alternant.situation_avant_contrat)
            #print(alternant.diplome_le_plus_eleve)
            #print(alternant.dernier_diplome_prepare)
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
                if alternant.diplome_le_plus_eleve == 31 or alternant.dernier_diplome_prepare == 31:
                    enr.append("0061")
                elif alternant.diplome_le_plus_eleve == 32 or alternant.dernier_diplome_prepare == 32:
                    enr.append("0065")
                else:
                    enr.append("0069")
            elif alternant.situation_avant_contrat == 2:
                enr.append("0999")
            elif alternant.situation_avant_contrat == 1:
                if alternant.dernier_diplome_prepare == 42:
                    enr.append("0051")
                elif alternant.dernier_diplome_prepare == 43:
                    enr.append("0053")
                else:
                    enr.append("0999")
            else:
                enr.append("0999")
            # 23 QUAL
            enr.append("D")
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
                if entreprise.adresse_voie:
                    adresse = "%s %s" % (entreprise.adresse_numero, entreprise.adresse_voie)
                else:
                    adresse = "%s" % (entreprise.adresse_numero)
            else:
                if entreprise.adresse_voie:
                    adresse = "%s" % (entreprise.adresse_voie)
                else:
                    adresse = ""

            # 34 ADR2 ENT
            if entreprise.adresse_complement:
                adresse2 = entreprise.adresse_complement
            else:
                adresse2 = ""

            if len(adresse) > 38:
                enr.append(adresse[:38])
                adresse3 = "%s %s" % (adresse[38:], adresse2)
                enr.append(adresse3[:38])
            else:
                enr.append(adresse)
                enr.append(adresse2[:38])

            # 35 CP ENT
            enr.append(entreprise.code_postal)
            # 36 VILLE ENT
            enr.append(entreprise.ville.upper())
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
        'CFA Epure<no_reply@cfa-epure.com>',
        [email_livraison],
    )

    email.attach_file(nomfichier)

    email.send(fail_silently=True)

    if etat in [2] and extraction in [0]:
        for contrat in contrats:
            contrat.date_exportation_CFA =datetime.now()
            contrat.save()

    #print(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))
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

    return True

    #if contrat.mission:
    #    if len(contrat.mission) >= 100:
    #        return True
    #    else:
    #        return False
    #else:
    #    return False


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


def contrat_ypareo_complet(contrat):

    if contrat:

        i = 0

        if contrat.date_debut_contrat:
            i += 1
        if contrat.date_fin_contrat:
            i += 1

        if i == 2:
            return True
        else:
            return False
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
        request.session["contratypareocomplet"] = False
        request.session["formationcomplet"] = False
        request.session["missioncomplet"] = False
        request.session["entreprisecomplet"] = False
        request.session["accordvalide"] = False

    else:
        request.session["contratcomplet"] = contrat_complet(contrat)
        request.session["contratypareocomplet"] = contrat_ypareo_complet(contrat)
        request.session["formationcomplet"] = formation_complet(contrat)
        request.session["missioncomplet"] = mission_complet(contrat)
        request.session["accordvalide"] = (contrat.avis_raf == 2)

        if not contrat.entreprise:
            request.session["entreprisecomplet"] = False
        else:
            request.session["entreprisecomplet"] = entreprise_complet(contrat.entreprise)

    return request

def creerexporttotal(request, email_livraison):

    # Pour récupérer tout : all()

    contrats = Contrat.objects.all()

    nomfichier = "export.csv"
    nomfichier = os.path.join(settings.PDF_OUTPUT_DIR, nomfichier)

    with open(nomfichier, "w") as f:

        c = csv.writer(f, delimiter=";")

        c.writerow(["Id",
                    "ContratCourant",
                    "MailApp",
                    "NomApp",
                    "PrénomApp",
                    "SexeApp",
                    "DateNaisApp",
                    "DéptNaisApp",
                    "CommNaisApp",
                    "AdrApp",
                    "CPApp",
                    "VilleApp",
                    "TelApp",
                    "Handicap",
                    "Nationalité",
                    "RégimeSocial",
                    "SituationAvant",
                    "DernierDiplômePréparé",
                    "DernièreAnnéeSUivie",
                    "InituléDernierDiplômePréparé",
                    "DiplômePlusElevé",
                    "SexeRep",
                    "NomRep",
                    "PrénomRep",
                    "AdrRep",
                    "CPRep",
                    "VilleRep",
                    "RaisonSociale",
                    "SIRET",
                    "Adr1Ent",
                    "Adr2Ent",
                    "CPEnt",
                    "VilleEnt",
                    "TypeEmployeur",
                    "SecteurEmployeur",
                    "EmployeurSpécifique",
                    "CodeAPE",
                    "Effectif",
                    "TéléphoneEnt",
                    "TélécopieEnt",
                    "EmailEnt",
                    "LibelléCC",
                    "CodeCC",
                    "RégimeAssuranceChômage",
                    "CivilitéMA1",
                    "NomMA1",
                    "PrénomMA1",
                    "EmailMA1",
                    "DateNaisMA1",
                    "CivilitéMA2",
                    "NomMA2",
                    "PrénomMA2",
                    "EmailMA2",
                    "DateNaisMA2",
                    "CivilitéCE",
                    "NomCE",
                    "PrénomCE",
                    "EmailCE",
                    "DateNaisCE",
                    "CodeFormation",
                    "LibelléFormation",
                    "Ville",
                    "Spécialité",
                    "CodeDiplôme",
                    "LibelléDiplôme",
                    "CodeDiplômeApprentissage",
                    "Niveau",
                    "NombreAnnées",
                    "RAF",
                    "CodeAccès",
                    "RéférentGU",
                    "ModeContractuel",
                    "TypeContratAvenant",
                    "TypeDérogation",
                    "ContratAntérieur",
                    "DateEmbauche",
                    "DateDébutContrat",
                    "DateEffetAvenant",
                    "DateFinContrat",
                    "DuréeHebdomadaireHeures",
                    "DuréeHebdomadaireMinutes",
                    "RisquesParticuliers",
                    "BrutMensuel",
                    "CaisseRetraiteComp",
                    "Nourriture",
                    "PrimePanier",
                    "Logement",
                    "An1Per1Du",
                    "An1Per1Au",
                    "An1Per1Taux",
                    "An1Per1Base",
                    "An1Per2Du",
                    "An1Per2Au",
                    "An1Per2Taux",
                    "An1Per2Base",
                    "An2Per1Du",
                    "An2Per1Au",
                    "An2Per1Taux",
                    "An2Per1Base",
                    "An2Per2Du",
                    "An2Per2Au",
                    "An2Per2Taux",
                    "An2Per2Base",
                    "An3Per1Du",
                    "An3Per1Au",
                    "An3Per1Taux",
                    "An3Per1Base",
                    "An3Per2Du",
                    "An3Per2Au",
                    "An3Per2Taux",
                    "An3Per2Base",
                    "An4Per1Du",
                    "An4Per1Au",
                    "An4Per1Taux",
                    "An4Per1Base",
                    "An4Per2Du",
                    "An4Per2Au",
                    "An4Per2Taux",
                    "An4Per2Base",
                    "DateMAJ",
                    "DateSaisieComplète",
                    "DateEnvoiRAF",
                    "DateGénérationCERFA",
                    "DateExportationCFA",
                    "AvisRAF"])

        for contrat in contrats:

            enr=[]

            try:
                alternant = contrat.alternant
            except ObjectDoesNotExist:
                alternant = None

            enr.append(contrat.id)
            enr.append(contrat.contrat_courant)

            if alternant:
                if alternant.user.email:
                    enr.append(alternant.user.email)
                else:
                    enr.append("")
                if alternant.nom:
                    enr.append(alternant.nom)
                else:
                    enr.append("")
                if alternant.prenom:
                    enr.append(alternant.prenom)
                else:
                    enr.append("")
                if alternant.sexe:
                    enr.append(alternant.sexe)
                else:
                    enr.append("")
                if alternant.date_naissance:
                    enr.append(alternant.date_naissance.strftime('%d/%m/%Y'))
                else:
                    enr.append("")
                if alternant.numero_departement_naissance:
                    enr.append(alternant.numero_departement_naissance)
                else:
                    enr.append("")
                if alternant.commune_naissance:
                    enr.append(alternant.commune_naissance)
                else:
                    enr.append("")

                if alternant.adresse_numero:
                    if alternant.adresse_voie:
                        enr.append("%s %s" % (alternant.adresse_numero, alternant.adresse_voie))
                    else:
                        enr.append("%s" % (alternant.adresse_numero))
                else:
                    if alternant.adresse_voie:
                        enr.append("%s" % (alternant.adresse_voie))
                    else:
                        enr.append("")

                if alternant.code_postal:
                    enr.append(alternant.code_postal)
                else:
                    enr.append("")

                if alternant.ville:
                    enr.append(alternant.ville)
                else:
                    enr.append("")

                if alternant.telephone:
                    enr.append(alternant.telephone)
                else:
                    enr.append("")

                enr.append(alternant.handicape)

                if alternant.nationalite:
                    enr.append(alternant.nationalite)
                else:
                    enr.append("")
                if alternant.regime_social:
                    enr.append(alternant.regime_social)
                else:
                    enr.append("")
                if alternant.situation_avant_contrat:
                    enr.append(alternant.situation_avant_contrat)
                else:
                    enr.append("")
                if alternant.dernier_diplome_prepare:
                    enr.append(alternant.dernier_diplome_prepare)
                else:
                    enr.append("")
                if alternant.derniere_annee_suivie:
                    enr.append(alternant.derniere_annee_suivie)
                else:
                    enr.append("")
                if alternant.intitule_dernier_diplome_prepare:
                    enr.append(alternant.intitule_dernier_diplome_prepare)
                else:
                    enr.append("")
                if alternant.diplome_le_plus_eleve:
                    enr.append(alternant.diplome_le_plus_eleve)
                else:
                    enr.append("")

                if alternant.civilite_representant == 1 or alternant.civilite_representant == 2:
                    enr.append(alternant.civilite_representant)
                else:
                    enr.append("")
                if alternant.nom_representant:
                    enr.append(alternant.nom_representant)
                else:
                    enr.append("")
                if alternant.prenom_representant:
                    enr.append(alternant.prenom_representant)
                else:
                    enr.append("")

                if alternant.adresse_numero_representant:
                    if alternant.adresse_voie_representant:
                        enr.append("%s %s" % (alternant.adresse_numero_representant, alternant.adresse_voie_representant))
                    else:
                        enr.append("")
                else:
                    if alternant.adresse_voie_representant:
                        enr.append(alternant.adresse_voie_representant)
                    else:
                        enr.append("")
                if alternant.code_postal_representant:
                    enr.append(alternant.code_postal_representant)
                else:
                    enr.append("")
                if alternant.ville_representant:
                    enr.append(alternant.ville_representant)
                else:
                    enr.append("")
            else:
                i = 1
                while i < 26:
                    enr.append("")
                    i+=1

            try:
                entreprise = contrat.entreprise
            except ObjectDoesNotExist:
                entreprise = None

            if entreprise:

                enr.append(entreprise.raison_sociale)
                enr.append(entreprise.numero_SIRET)
                if entreprise.adresse_numero:
                    enr.append("%s %s" % (entreprise.adresse_numero, entreprise.adresse_voie))
                else:
                    enr.append(entreprise.adresse_voie)
                if entreprise.adresse_complement:
                    enr.append(entreprise.adresse_complement)
                else:
                    enr.append("")
                enr.append(entreprise.code_postal)
                enr.append(entreprise.ville)
                enr.append(entreprise.type_employeur)
                enr.append(entreprise.secteur_employeur)
                enr.append(entreprise.employeur_specifique)
                enr.append(entreprise.code_APE)
                enr.append(entreprise.effectif_entreprise)
                enr.append(entreprise.telephone)
                if entreprise.telecopie:
                    enr.append(entreprise.telecopie)
                else:
                    enr.append("")
                if entreprise.courriel:
                    enr.append(entreprise.courriel)
                else:
                    enr.append("")
                if entreprise.libelle_convention_collective:
                    enr.append(entreprise.libelle_convention_collective)
                else:
                    enr.append("")
                if entreprise.code_convention_collective:
                    enr.append(entreprise.code_convention_collective)
                else:
                    enr.append("")
                if entreprise.adhesion_regime_assurance_chomage:
                    enr.append(entreprise.adhesion_regime_assurance_chomage)
                else:
                    enr.append("")
            else:
                i = 1
                while i < 18:
                    enr.append("")
                    i+=1

            try:
                maitreapprentissage1 = Personnel.objects.get(entreprise=entreprise,role=2)
            except ObjectDoesNotExist:
                maitreapprentissage1 = None

            if maitreapprentissage1:
                if maitreapprentissage1.civilite:
                    enr.append(maitreapprentissage1.civilite)
                else:
                    enr.append("")

                if maitreapprentissage1.nom:
                    enr.append(maitreapprentissage1.nom)
                else:
                    enr.append("")
                if maitreapprentissage1.prenom:
                    enr.append(maitreapprentissage1.prenom)
                else:
                    enr.append("")
                if maitreapprentissage1.courriel:
                    enr.append(maitreapprentissage1.courriel)
                else:
                    enr.append("")
                if maitreapprentissage1.date_naissance:
                    enr.append(maitreapprentissage1.date_naissance.strftime('%d/%m/%Y'))
                else:
                    enr.append("")
            else:
                enr.append("")
                enr.append("")
                enr.append("")
                enr.append("")
                enr.append("")

            try:
                maitreapprentissage2 = Personnel.objects.get(entreprise=entreprise, role=3)
            except ObjectDoesNotExist:
                maitreapprentissage2 = None

            if maitreapprentissage2:
                if maitreapprentissage2.civilite:
                    enr.append(maitreapprentissage2.civilite)
                else:
                    enr.append("")
                if maitreapprentissage2.nom:
                    enr.append(maitreapprentissage2.nom)
                else:
                    enr.append("")
                if maitreapprentissage2.prenom:
                    enr.append(maitreapprentissage2.prenom)
                else:
                    enr.append("")
                if maitreapprentissage2.courriel:
                    enr.append(maitreapprentissage2.courriel)
                else:
                    enr.append("")
                if maitreapprentissage2.date_naissance:
                    enr.append(maitreapprentissage2.date_naissance.strftime('%d/%m/%Y'))
                else:
                    enr.append("")
            else:
                enr.append("")
                enr.append("")
                enr.append("")
                enr.append("")
                enr.append("")

            try:
                contactentreprise = Personnel.objects.get(entreprise=entreprise, role=3)
            except ObjectDoesNotExist:
                contactentreprise = None

            if contactentreprise:
                if contactentreprise.civilite:
                    enr.append(contactentreprise.civilite)
                else:
                    enr.append("")
                if contactentreprise.nom:
                    enr.append(contactentreprise.nom)
                else:
                    enr.append("")
                if contactentreprise.prenom:
                    enr.append(contactentreprise.prenom)
                else:
                    enr.append("")
                if contactentreprise.courriel:
                    enr.append(contactentreprise.courriel)
                else:
                    enr.append("")
                if contactentreprise.date_naissance:
                    enr.append(contactentreprise.date_naissance.strftime('%d/%m/%Y'))
                else:
                    enr.append("")
            else:
                enr.append("")
                enr.append("")
                enr.append("")
                enr.append("")
                enr.append("")

            try:
                formation = contrat.formation
            except ObjectDoesNotExist:
                formation = None

            if formation:
                enr.append(formation.code_formation)
                enr.append(formation.intitule_formation)
                enr.append(formation.ville)
                enr.append(formation.specialite)
                enr.append(formation.diplome)
                enr.append(formation.intitule_diplome)
                enr.append(formation.code_diplome_apprentissage)
                enr.append(formation.niveau)
                enr.append(formation.nombre_annees)
                enr.append(formation.raf)
                enr.append(formation.code_acces)
                enr.append(formation.referent_GU)
            else:
                i = 1
                while i < 13:
                    enr.append("")
                    i+=1

            enr.append(contrat.mode_contractuel)
            enr.append(contrat.type_contrat_avenant)
            if contrat.type_derogation:
                enr.append(contrat.type_derogation)
            else:
                enr.append("")

            if contrat.numero_contrat_anterieur:
                enr.append(contrat.numero_contrat_anterieur)
            else:
                enr.append("")

            if contrat.date_embauche:
                enr.append(contrat.date_embauche.strftime('%d/%m/%Y'))
            else:
                enr.append("")

            if contrat.date_debut_contrat:
                enr.append(contrat.date_debut_contrat.strftime('%d/%m/%Y'))
            else:
                enr.append("")

            if contrat.date_effet_avenant:
                enr.append(contrat.date_effet_avenant.strftime('%d/%m/%Y'))
            else:
                enr.append("")

            if contrat.date_fin_contrat:
                enr.append(contrat.date_fin_contrat.strftime('%d/%m/%Y'))
            else:
                enr.append("")

            if contrat.duree_hebdomadaire_travail_heures:
                enr.append(contrat.duree_hebdomadaire_travail_heures)
            else:
                enr.append("")

            if contrat.duree_hebdomadaire_travail_minutes:
                enr.append(contrat.duree_hebdomadaire_travail_minutes)
            else:
                enr.append("")

            enr.append(contrat.risques_particuliers)

            if contrat.salaire_brut_mensuel:
                enr.append(contrat.salaire_brut_mensuel)
            else:
                enr.append("")

            if contrat.caisse_retraite_complementaire:
                enr.append(contrat.caisse_retraite_complementaire)
            else:
                enr.append("")

            if contrat.nourriture:
                enr.append(contrat.nourriture)
            else:
                enr.append("")

            if contrat.prime_panier:
                enr.append(contrat.prime_panier)
            else:
                enr.append("")

            if contrat.logement:
                enr.append(contrat.logement)
            else:
                enr.append("")

            if contrat.an_1_per_1_du:
                enr.append(contrat.an_1_per_1_du.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_1_per_1_au:
                enr.append(contrat.an_1_per_1_au.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_1_per_1_taux:
                enr.append(contrat.an_1_per_1_taux)
            else:
                enr.append("")
            if contrat.an_1_per_1_base:
                enr.append(contrat.an_1_per_1_base)
            else:
                enr.append("")
            if contrat.an_1_per_2_du:
                enr.append(contrat.an_1_per_2_du.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_1_per_2_au:
                enr.append(contrat.an_1_per_2_au.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_1_per_2_taux:
                enr.append(contrat.an_1_per_2_taux)
            else:
                enr.append("")
            if contrat.an_1_per_2_base:
                enr.append(contrat.an_1_per_2_base)
            else:
                enr.append("")

            if contrat.an_2_per_1_du:
                enr.append(contrat.an_2_per_1_du.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_2_per_1_au:
                enr.append(contrat.an_2_per_1_au.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_2_per_1_taux:
                enr.append(contrat.an_2_per_1_taux)
            else:
                enr.append("")
            if contrat.an_2_per_1_base:
                enr.append(contrat.an_2_per_1_base)
            else:
                enr.append("")
            if contrat.an_2_per_2_du:
                enr.append(contrat.an_2_per_2_du.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_2_per_2_au:
                enr.append(contrat.an_2_per_2_au.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_2_per_2_taux:
                enr.append(contrat.an_2_per_2_taux)
            else:
                enr.append("")
            if contrat.an_2_per_2_base:
                enr.append(contrat.an_2_per_2_base)
            else:
                enr.append("")

            if contrat.an_3_per_1_du:
                enr.append(contrat.an_3_per_1_du.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_3_per_1_au:
                enr.append(contrat.an_3_per_1_au.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_3_per_1_taux:
                enr.append(contrat.an_3_per_1_taux)
            else:
                enr.append("")
            if contrat.an_3_per_1_base:
                enr.append(contrat.an_3_per_1_base)
            else:
                enr.append("")
            if contrat.an_3_per_2_du:
                enr.append(contrat.an_3_per_2_du.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_3_per_2_au:
                enr.append(contrat.an_3_per_2_au.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_3_per_2_taux:
                enr.append(contrat.an_3_per_2_taux)
            else:
                enr.append("")
            if contrat.an_3_per_2_base:
                enr.append(contrat.an_3_per_2_base)
            else:
                enr.append("")

            if contrat.an_4_per_1_du:
                enr.append(contrat.an_4_per_1_du.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_4_per_1_au:
                enr.append(contrat.an_4_per_1_au.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_4_per_1_taux:
                enr.append(contrat.an_4_per_1_taux)
            else:
                enr.append("")
            if contrat.an_4_per_1_base:
                enr.append(contrat.an_4_per_1_base)
            else:
                enr.append("")
            if contrat.an_4_per_2_du:
                enr.append(contrat.an_4_per_2_du.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_4_per_2_au:
                enr.append(contrat.an_4_per_2_au.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.an_4_per_2_taux:
                enr.append(contrat.an_4_per_2_taux)
            else:
                enr.append("")
            if contrat.an_4_per_2_base:
                enr.append(contrat.an_4_per_2_base)
            else:
                enr.append("")

            enr.append(contrat.date_maj.strftime('%d/%m/%Y'))

            if contrat.date_saisie_complete:
                enr.append(contrat.date_saisie_complete.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.date_envoi_raf:
                enr.append(contrat.date_envoi_raf.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.date_generation_CERFA:
                enr.append(contrat.date_generation_CERFA.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            if contrat.date_exportation_CFA:
                enr.append(contrat.date_exportation_CFA.strftime('%d/%m/%Y'))
            else:
                enr.append("")
            enr.append(contrat.avis_raf)

            c.writerow(enr)

    # Création du mail
    email = EmailMultiAlternatives(
        "cactus export ypareo",
        "",
        'CFA Epure<no_reply@cfa-epure.com>',
        [email_livraison],
    )

    email.attach_file(nomfichier)

    email.send(fail_silently=True)

    #print(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))
    try:
        os.remove(os.path.join(settings.PDF_OUTPUT_DIR, nomfichier))
    except:
        pass


def creerCERFA(alternant, aplatir):

    # Recuperer les infos qui nous intéressent pour le pdf

    #print(request.user.email)
    #alternant = Alternant.objects.get(user=request.user)

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

    if contrat.type_contrat_avenant in (31, 32, 33, 34, 35, 36):
        data["avenant"] = 1
    else:
        data["contrat"] = 1

    data["mode_Contrat"] = contrat.mode_contractuel
    data["emp_siret"] = entreprise.numero_SIRET
    if entreprise.adresse_numero:
        data["emp_adr_num"] = entreprise.adresse_numero
    data["emp_adr_voie"] = entreprise.adresse_voie.upper()
    if entreprise.adresse_complement is not None:
        data["emp_adr_compl"] = entreprise.adresse_complement.upper()
    data["emp_adr_cp"] = entreprise.code_postal
    data["emp_adr_ville"] = entreprise.ville.upper()
    data["emp_tel"] = entreprise.telephone
    data["emp_fax"] = entreprise.telecopie

    data["emp_mail1"] = entreprise.courriel[0:entreprise.courriel.find('@')]
    data["emp_mail2"] = entreprise.courriel[entreprise.courriel.find('@') + 1:]
    data["emp_type"] = entreprise.type_employeur
    data["emp_specifique"] = entreprise.employeur_specifique
    data["emp_naf"] = entreprise.code_APE
    data["emp_eff"] = entreprise.effectif_entreprise

    data["emp_conv_coll"] = entreprise.libelle_convention_collective

    data["emp_idcc"] = entreprise.code_convention_collective
    data["emp_denom"] = entreprise.raison_sociale.upper()
    data["emp_adh_chomage"] = entreprise.adhesion_regime_assurance_chomage

    data["alt_nom"] = "%s %s" % (alternant.nom.upper(), alternant.prenom.upper())
    data["alt_mail1"] = alternant.user.email
    data["alt_tel"] = alternant.telephone
    data["alt_adr_ville"] = alternant.ville
    data["alt_adr_cp"] = alternant.code_postal
    data["alt_adr_num"] = alternant.adresse_numero
    if alternant.adresse_voie:
        data["alt_adr_voie"] = alternant.adresse_voie.upper()
    if alternant.ville_representant:
        data["alt_repr_adr_ville"] = alternant.ville_representant
    if alternant.code_postal_representant:
        data["alt_repr_adr_cp"] = alternant.code_postal_representant
    if alternant.adresse_voie_representant:
        data["alt_repr_adr_voie"] = alternant.adresse_voie_representant
    if alternant.adresse_numero_representant:
        data["alt_repr_adr_num"] = alternant.adresse_numero_representant
    if alternant.nom_representant:
        if alternant.prenom_representant:
            nom_prenom_representant = "%s %s" % (alternant.nom_representant, alternant.prenom_representant)
        else:
            nom_prenom_representant = "%s" % (alternant.nom_representant)
    else:
        nom_prenom_representant = "%s" % (alternant.prenom_representant)

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
        if ma_2.date_naissance:
            data["maitre2_ddn_jour"] = str(ma_2.date_naissance.day).zfill(2)
            data["maitre2_ddn_mois"] = str(ma_2.date_naissance.month).zfill(2)
            data["maitre2_ddn_annee"] = ma_2.date_naissance.year

    if contrat.attestation_maitre_apprentissage:
        data["maitre_attestation"] = 1
    data["contrat_type"] = contrat.type_contrat_avenant
    data["contrat_derog"] = contrat.type_derogation

    if contrat.numero_contrat_anterieur is not None:
        data["contrat_num_prec"] = contrat.numero_contrat_anterieur

    if contrat.date_embauche is not None:
        data["contrat_debut_jour"] = str(contrat.date_embauche.day).zfill(2)
        data["contrat_debut_mois"] = str(contrat.date_embauche.month).zfill(2)
        data["contrat_debut_annee"] = contrat.date_embauche.year

    data["execution_fin_annee"] = contrat.date_debut_contrat.year
    data["execution_fin_mois"] = str(contrat.date_debut_contrat.month).zfill(2)
    data["execution_fin_jour"] = str(contrat.date_debut_contrat.day).zfill(2)

    data["contrat_duree_hebdo_heures"] = str(contrat.duree_hebdomadaire_travail_heures)
    data["contrat_duree_hebdo_minutes"] = str(contrat.duree_hebdomadaire_travail_minutes)

    if contrat.risques_particuliers:
        data["contrat_risques_oui"] = 1
    else:
        data["contrat_risques_non"] = 1


    if contrat.an_1_per_1_taux is not None:
        taux = contrat.an_1_per_1_taux
        entier = int(taux)
        decimal = round((taux - entier) * 100)
        premieredecimale = int(decimal / 10)
        deuxiemedecimale = decimal - premieredecimale * 10
        if decimal == 0:
            data["contrat_remu_annee1_taux1"] = str(entier)
        else:
            if deuxiemedecimale == 0:
                data["contrat_remu_annee1_taux1"] = "%i.%i" % (entier, premieredecimale)
            else:
                data["contrat_remu_annee1_taux1"] = "%i.%i" % (entier, decimal)

    if contrat.an_2_per_1_taux is not None:
        taux = contrat.an_2_per_1_taux
        entier = int(taux)
        decimal = round((taux - entier) * 100)
        premieredecimale = int(decimal / 10)
        deuxiemedecimale = decimal - premieredecimale * 10
        if decimal == 0:
            data["contrat_remu_annee2_taux1"] = str(entier)
        else:
            if deuxiemedecimale == 0:
                data["contrat_remu_annee2_taux1"] = "%i.%i" % (entier, premieredecimale)
            else:
                data["contrat_remu_annee2_taux1"] = "%i.%i" % (entier, decimal)

    if contrat.an_3_per_1_taux is not None:
        taux = contrat.an_3_per_1_taux
        entier = int(taux)
        decimal = round((taux - entier) * 100)
        premieredecimale = int(decimal / 10)
        deuxiemedecimale = decimal - premieredecimale * 10
        if decimal == 0:
            data["contrat_remu_annee3_taux1"] = str(entier)
        else:
            if deuxiemedecimale == 0:
                data["contrat_remu_annee3_taux1"] = "%i.%i" % (entier, premieredecimale)
            else:
                data["contrat_remu_annee3_taux1"] = "%i.%i" % (entier, decimal)

    if contrat.an_4_per_1_taux is not None:
        taux = contrat.an_4_per_1_taux
        entier = int(taux)
        decimal = round((taux - entier) * 100)
        premieredecimale = int(decimal / 10)
        deuxiemedecimale = decimal - premieredecimale * 10
        if decimal == 0:
            data["contrat_remu_annee4_taux1"] = str(entier)
        else:
            if deuxiemedecimale == 0:
                data["contrat_remu_annee4_taux1"] = "%i.%i" % (entier, premieredecimale)
            else:
                data["contrat_remu_annee4_taux1"] = "%i.%i" % (entier, decimal)

    if contrat.an_1_per_1_du is not None:
        data["contrat_remu_annee1_du1_jour"] = str(contrat.an_1_per_1_du.day).zfill(2)
        data["contrat_remu_annee1_du1_mois"] = str(contrat.an_1_per_1_du.month).zfill(2)
        data["contrat_remu_annee1_du1_annee"] = contrat.an_1_per_1_du.year
    if contrat.an_2_per_1_du is not None:
        data["contrat_remu_annee2_du1_jour"] = str(contrat.an_2_per_1_du.day).zfill(2)
        data["contrat_remu_annee2_du1_mois"] = str(contrat.an_2_per_1_du.month).zfill(2)
        data["contrat_remu_annee2_du1_annee"] = contrat.an_2_per_1_du.year
    if contrat.an_3_per_1_du is not None:
        data["contrat_remu_annee3_du1_jour"] = str(contrat.an_3_per_1_du.day).zfill(2)
        data["contrat_remu_annee3_du1_mois"] = str(contrat.an_3_per_1_du.month).zfill(2)
        data["contrat_remu_annee3_du1_annee"] = contrat.an_3_per_1_du.year
    if contrat.an_4_per_1_du is not None:
        data["contrat_remu_annee4_du1_jour"] = str(contrat.an_4_per_1_du.day).zfill(2)
        data["contrat_remu_annee4_du1_mois"] = str(contrat.an_4_per_1_du.month).zfill(2)
        data["contrat_remu_annee4_du1_annee"] = contrat.an_4_per_1_du.year
    if contrat.an_1_per_1_au is not None:
        data["contrat_remu_annee1_au1_jour"] = str(contrat.an_1_per_1_au.day).zfill(2)
        data["contrat_remu_annee1_au1_mois"] = str(contrat.an_1_per_1_au.month).zfill(2)
        data["contrat_remu_annee1_au1_annee"] = contrat.an_1_per_1_au.year
    if contrat.an_2_per_1_au is not None:
        data["contrat_remu_annee2_au1_jour"] = str(contrat.an_2_per_1_au.day).zfill(2)
        data["contrat_remu_annee2_au1_mois"] = str(contrat.an_2_per_1_au.month).zfill(2)
        data["contrat_remu_annee2_au1_annee"] = contrat.an_2_per_1_au.year
    if contrat.an_3_per_1_au is not None:
        data["contrat_remu_annee3_au1_jour"] = str(contrat.an_3_per_1_au.day).zfill(2)
        data["contrat_remu_annee3_au1_mois"] = str(contrat.an_3_per_1_au.month).zfill(2)
        data["contrat_remu_annee3_au1_annee"] = contrat.an_3_per_1_au.year
    if contrat.an_4_per_1_au is not None:
        data["contrat_remu_annee4_au1_jour"] = str(contrat.an_4_per_1_au.day).zfill(2)
        data["contrat_remu_annee4_au1_mois"] = str(contrat.an_4_per_1_au.month).zfill(2)
        data["contrat_remu_annee4_au1_annee"] = contrat.an_4_per_1_au.year

    if contrat.an_1_per_1_base is not None:
        data["contrat_remu_annee1_ref1"] = Contrat.BASE[contrat.an_1_per_1_base - 1][1]
    if contrat.an_2_per_1_base is not None:
        data["contrat_remu_annee2_ref1"] = Contrat.BASE[contrat.an_2_per_1_base - 1][1]
    if contrat.an_3_per_1_base is not None:
        data["contrat_remu_annee3_ref1"] = Contrat.BASE[contrat.an_3_per_1_base - 1][1]
    if contrat.an_4_per_1_base is not None:
        data["contrat_remu_annee4_ref1"] = Contrat.BASE[contrat.an_4_per_1_base - 1][1]

    if contrat.an_1_per_2_taux is not None:
        taux = contrat.an_1_per_2_taux
        entier = int(taux)
        decimal = round((taux - entier) * 100)
        premieredecimale = int(decimal / 10)
        deuxiemedecimale = decimal - premieredecimale * 10
        if decimal == 0:
            data["contrat_remu_annee1_taux2"] = str(entier)
        else:
            if deuxiemedecimale == 0:
                data["contrat_remu_annee1_taux2"] = "%i.%i" % (entier, premieredecimale)
            else:
                data["contrat_remu_annee1_taux2"] = "%i.%i" % (entier, decimal)

    if contrat.an_2_per_2_taux is not None:
        taux = contrat.an_2_per_2_taux
        entier = int(taux)
        decimal = round((taux - entier) * 100)
        premieredecimale = int(decimal / 10)
        deuxiemedecimale = decimal - premieredecimale * 10
        if decimal == 0:
            data["contrat_remu_annee2_taux2"] = str(entier)
        else:
            if deuxiemedecimale == 0:
                data["contrat_remu_annee2_taux2"] = "%i.%i" % (entier, premieredecimale)
            else:
                data["contrat_remu_annee2_taux2"] = "%i.%i" % (entier, decimal)

    if contrat.an_3_per_2_taux is not None:
        taux = contrat.an_3_per_2_taux
        entier = int(taux)
        decimal = round((taux - entier) * 100)
        premieredecimale = int(decimal / 10)
        deuxiemedecimale = decimal - premieredecimale * 10
        if decimal == 0:
            data["contrat_remu_annee3_taux2"] = str(entier)
        else:
            if deuxiemedecimale == 0:
                data["contrat_remu_annee3_taux2"] = "%i.%i" % (entier, premieredecimale)
            else:
                data["contrat_remu_annee3_taux2"] = "%i.%i" % (entier, decimal)

    if contrat.an_4_per_2_taux is not None:
        taux = contrat.an_4_per_2_taux
        entier = int(taux)
        decimal = round((taux - entier) * 100)
        premieredecimale = int(decimal / 10)
        deuxiemedecimale = decimal - premieredecimale * 10
        if decimal == 0:
            data["contrat_remu_annee4_taux2"] = str(entier)
        else:
            if deuxiemedecimale == 0:
                data["contrat_remu_annee4_taux2"] = "%i.%i" % (entier, premieredecimale)
            else:
                data["contrat_remu_annee4_taux2"] = "%i.%i" % (entier, decimal)


    if contrat.an_1_per_2_du is not None:
        data["contrat_remu_annee1_du2_jour"] = str(contrat.an_1_per_2_du.day).zfill(2)
        data["contrat_remu_annee1_du2_mois"] = str(contrat.an_1_per_2_du.month).zfill(2)
        data["contrat_remu_annee1_du2_annee"] = contrat.an_1_per_2_du.year
    if contrat.an_2_per_2_du is not None:
        data["contrat_remu_annee2_du2_jour"] = str(contrat.an_2_per_2_du.day).zfill(2)
        data["contrat_remu_annee2_du2_mois"] = str(contrat.an_2_per_2_du.month).zfill(2)
        data["contrat_remu_annee2_du2_annee"] = contrat.an_2_per_2_du.year
    if contrat.an_3_per_2_du is not None:
        data["contrat_remu_annee3_du2_jour"] = str(contrat.an_3_per_2_du.day).zfill(2)
        data["contrat_remu_annee3_du2_mois"] = str(contrat.an_3_per_2_du.month).zfill(2)
        data["contrat_remu_annee3_du2_annee"] = contrat.an_3_per_2_du.year
    if contrat.an_4_per_2_du is not None:
        data["contrat_remu_annee4_du2_jour"] = str(contrat.an_4_per_2_du.day).zfill(2)
        data["contrat_remu_annee4_du2_mois"] = str(contrat.an_4_per_2_du.month).zfill(2)
        data["contrat_remu_annee4_du2_annee"] = contrat.an_4_per_2_du.year
    if contrat.an_1_per_2_au is not None:
        data["contrat_remu_annee1_au2_jour"] = str(contrat.an_1_per_2_au.day).zfill(2)
        data["contrat_remu_annee1_au2_mois"] = str(contrat.an_1_per_2_au.month).zfill(2)
        data["contrat_remu_annee1_au2_annee"] = contrat.an_1_per_2_au.year
    if contrat.an_2_per_2_au is not None:
        data["contrat_remu_annee2_au2_jour"] = str(contrat.an_2_per_2_au.day).zfill(2)
        data["contrat_remu_annee2_au2_mois"] = str(contrat.an_2_per_2_au.month).zfill(2)
        data["contrat_remu_annee2_au2_annee"] = contrat.an_2_per_2_au.year
    if contrat.an_3_per_2_au is not None:
        data["contrat_remu_annee3_au2_jour"] = str(contrat.an_3_per_2_au.day).zfill(2)
        data["contrat_remu_annee3_au2_mois"] = str(contrat.an_3_per_2_au.month).zfill(2)
        data["contrat_remu_annee3_au2_annee"] = contrat.an_3_per_2_au.year
    if contrat.an_4_per_2_au is not None:
        data["contrat_remu_annee4_au2_jour"] = str(contrat.an_4_per_2_au.day).zfill(2)
        data["contrat_remu_annee4_au2_mois"] = str(contrat.an_4_per_2_au.month).zfill(2)
        data["contrat_remu_annee4_au2_annee"] = contrat.an_4_per_2_au.year
    if contrat.an_1_per_2_base is not None:
        data["contrat_remu_annee1_ref2"] = Contrat.BASE[contrat.an_1_per_2_base - 1][1]
    if contrat.an_2_per_2_base is not None:
        data["contrat_remu_annee2_ref2"] = Contrat.BASE[contrat.an_2_per_2_base - 1][1]
    if contrat.an_3_per_2_base is not None:
        data["contrat_remu_annee3_ref2"] = Contrat.BASE[contrat.an_3_per_2_base - 1][1]
    if contrat.an_4_per_2_base is not None:
        data["contrat_remu_annee4_ref2"] = Contrat.BASE[contrat.an_4_per_2_base - 1][1]


    if contrat.salaire_brut_mensuel is not None:
        entier = int(contrat.salaire_brut_mensuel)
        decimal = round((contrat.salaire_brut_mensuel - entier) * 100)
        data["contrat_salaire1"] = entier
        data["contrat_salaire2"] = str(decimal).zfill(2)

    if contrat.nourriture is not None:
        entier = int(contrat.nourriture)
        decimal = (contrat.nourriture - entier) * 100
        data["contrat_avantg_nourr1"] = entier
        data["contrat_avantg_nourr2"] = str(int(decimal)).zfill(2)

    if contrat.logement is not None:
        entier = int(contrat.logement)
        decimal = (contrat.logement - entier) * 100
        data["contrat_avantg_logt1"] = entier
        data["contrat_avantg_logt2"] = str(int(decimal)).zfill(2)

    if contrat.prime_panier is not None:
        entier = int(contrat.prime_panier)
        decimal = (contrat.prime_panier - entier) * 100
        data["panier_avantg_logt1"] = entier
        data["panier_avantg_logt2"] = str(int(decimal)).zfill(2)

    if contrat.date_effet_avenant is not None:
        data["avenant_debut_jour"] = str(contrat.date_effet_avenant.day).zfill(2)
        data["avenant_debut_mois"] = str(contrat.date_effet_avenant.month).zfill(2)
        data["avenant_debut_annee"] = contrat.date_effet_avenant.year

    data["contrat_fin_jour"] = str(contrat.date_fin_contrat.day).zfill(2)
    data["contrat_fin_mois"] = str(contrat.date_fin_contrat.month).zfill(2)
    data["contrat_fin_annee"] = contrat.date_fin_contrat.year

    if contrat.caisse_retraite_complementaire is not None:
        data["retraite_caisse_comp"] = contrat.caisse_retraite_complementaire

    data["formation_nom"] = cfa.nom
    data["formation_uai"] = cfa.numeroUAI

    data["formation_adr_voie"] = cfa.adresse_voie
    data["formation_adr_num"] = cfa.adresse_numero
    data["formation_adr_compl"] = cfa.adresse_complement
    data["formation_adr_cp"] = cfa.code_postal
    data["formation_adr_ville"] = cfa.ville
    data["formation_inspect_pedag"] = formation.inspection_pedagogique_competente

    if contrat.fait_le is not None:
        data["signature_date_annee"] = contrat.fait_le.year
        data["signature_date_mois"] = str(contrat.fait_le.month).zfill(2)
        data["signature_date_jour"] = str(contrat.fait_le.day).zfill(2)

    if contrat.fait_a:
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
        data["formation_annee1_heure"] = formation.heures_an_1
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

    filename = "CERFA_%s_%s_%s.pdf" % (alternant.nom,
                                       alternant.prenom,
                                       datetime.now().strftime("%Y%m%d%H%M%S"))
    filename = filename.replace(' ', '_')
    filename = filename.replace("'", "_")

    nomfichier = PDFGenerator.generate_cerfa_pdf_with_datas(filename, data, flatten=aplatir)

    return nomfichier
