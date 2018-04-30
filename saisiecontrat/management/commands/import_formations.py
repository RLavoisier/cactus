import csv
import os
import random

from django.conf import settings
from django.core.management import BaseCommand

from saisiecontrat.models import Formation,CFA


class Command(BaseCommand):
    help = 'Importation des formations'

    def handle(self, *args, **options):
        Formation.objects.all().delete()
        file = os.path.join(settings.BASE_DIR, "Formations.csv")
        f = open(file, 'r')
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            cfa, _ = CFA.objects.get_or_create(numeroUAI=row[1])
            if Formation.objects.filter(code_formation=row[0]).exists():
                continue
            _, created = Formation.objects.get_or_create(
                code_formation=row[0],
                cfa=cfa,
                intitule_formation=row[2],
                ville=row[3],
                specialite=row[4],
                diplome=row[5] or random.randint(21, 24),
                intitule_diplome=row[6],
                code_diplome_apprentissage=row[7],
                heures_an_1=row[10],
                niveau=row[17],
                nombre_annees=row[18],
                annee_remuneration_annee_diplome=row[19],
                inspection_pedagogique_competente=row[20],
                raf=row[21],
                courriel_raf=row[22],
                code_acces=row[23]
            )
            print(row[2])


