import os
import uuid

from saisiecontrat.utils import pypdftk
from django.conf import settings


class PDFGenerator:
    """
    Class gérant la génération des PDF
    """
    OUTPUT_DIR = os.path.join(settings.BASE_DIR, "pdf_outputs")

    @classmethod
    def generate_cerfa_pdf_with_datas(cls, filename, input_datas, flatten=True):
        """
        Cette méthode prends en argument un dictionnaire contenant les nom des champs
        du pdf et les valeurs à injecter

        les fichiers sont générés avec un nom encodés pour éviter les écrasements

        :param input_datas: Dictionnaire des valeurs
        :type input_datas: dict

        :return: Le nom du fichier généré
        :rtype: str
        """
        cerfa_pdf = os.path.join(settings.TEMPLATE_DIR, "pdf", "cerfa_10103.pdf")
        # Transformation des nom de champ du dictionnaire
        formatted_datas = cls.__format_input_datas_dict(input_datas)

        return cls.__fill_pdf(filename, cerfa_pdf, formatted_datas, flatten)


    @classmethod
    def generate_mission_pdf_with_datas(cls, filename, input_datas, flatten=True):
        """
        Cette méthode génère un pdf avec les données passées en argument

        :param input_datas: Dictionnaire des valeurs
        :type input_datas: dict

        :return: Le nom du fichier généré
        :rtype: str
        """
        template_pdf = os.path.join(settings.TEMPLATE_DIR, "pdf", "fiche_mission.pdf")
        return cls.__fill_pdf(filename, template_pdf, input_datas, flatten)

    @classmethod
    def __fill_pdf(cls, filename, template, datas, flatten=True):
        """
        Cette méthode injecte les données dans le template pdf passé en argument

        :param template:
        :param datas:
        :param flatten:
        :return:
        """
        # génération du nom de fichier
        #filename = "%s.pdf" % str(uuid.uuid4())

        # génération du chemin complet vers le fichier
        output_file_path = os.path.join(cls.OUTPUT_DIR, filename)

        # Remplissage du pdf
        pypdftk.fill_form(pdf_path=template, flatten=flatten,
                          datas=datas, out_file=output_file_path)

        return filename

    @classmethod
    def __format_input_datas_dict(cls, input_datas):
        """
        Cette méthode modifie les clés du dictionnaire input data pour coller
        au nom donné dans le pdf

        entrée : contrat_type
        sortie : topmostSubform[0].Page1[0].contrat_type[0]

        :param input_datas: les données en entrées
        :type input_datas: dict

        :return: le dict formaté
        :rtype: dict
        """
        # Attention si plusieurs pages dns le pdf. Ne fonctionne pas !
        return {"topmostSubform[0].Page1[0].%s[0]" % k: v
                for k, v in input_datas.items()}