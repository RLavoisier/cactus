import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from saisiecontrat.models import Formation,CFA


class Command(BaseCommand):
    help = 'Importation des formations'

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, "Formations.csv")
        f = open(file, 'r')
        reader = csv.reader(f)
        for row in reader:
            _, created = Formation.objects.get_or_create(
                code_formation=row[0],
                cfa=CFA(numeroUAI=row[1]),
                intitule_formation=row[2],
                ville=row[3],
                specialite=row[4],
                diplome=row[5],
                intitule_diplome=row[6],
                numero_UAI=row[7],
                heures_an_1=row[10],
                niveau=row[17],
                nombre_annees=row[18],
                annee_remuneration_annee_diplome=row[19],
                inspection_pedagogique_competente=row[20],
                an_1_du = row[8],
                an_1_au = row[9],
                an_2_du = row[11],
                an_2_au = row[12],
                an_3_du = row[14],
                an_3_au = row[15],
                heures_an_2 = row[13],
                heures_an_3 = row[16],
            )
            print(row[2])


