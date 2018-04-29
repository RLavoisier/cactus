
from django.core.mail import send_mail
from django.template.loader import render_to_string
from saisiecontrat.models import  Alternant,  Personnel, Contrat
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


    msg_plain = render_to_string('information_raf.html', context)
    msg_html = render_to_string('information_raf.html', context)

    send_mail(
        "Fiche mission de %s %s.pdf" % (alternant.nom, alternant.prenom),
        msg_plain,
        'cactus.test.tg@gmail.com',
        [formation.courriel_raf],
        html_message=msg_html
    )


def creerrecapinscriptions(formation_hash):

    pass