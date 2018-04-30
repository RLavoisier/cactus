import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from saisiecontrat.models import  Alternant,  Personnel, Contrat, Formation
from django.core.exceptions import ObjectDoesNotExist

from saisiecontrat.utils.pdf_generator import PDFGenerator


def generer_data_pour_pdf_mission(alternant, email, entreprise, ma_1, contrat):

    data = {}
    if alternant.adresse_numero is not None:
        data["numero"] = alternant.adresse_numero
    data["voie"] = alternant.adresse_voie
    data["codepostal"] = alternant.code_postal
    data["ville"] = alternant.ville
    data["neele"] = alternant.date_naissance.strftime('%d/%m/%Y')
    data["mail"] = email
    data["telephone"] = alternant.telephone
    data["nomprenom"] = "%s %s" % (alternant.nom, alternant.prenom)

    data["raisonsociale"] = entreprise.raison_sociale
    if entreprise.adresse_numero is not None:
        data["numero2"] = entreprise.adresse_numero
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
