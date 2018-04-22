import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from saisiecontrat.models import Minima


class Command(BaseCommand):
    help = 'Importation des communes'

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, "Minima.csv")
        f = open(file, 'r')
        reader = csv.reader(f)
        for row in reader:
            _, created = Minima.objects.get_or_create(
                annee=row[0],
                age=row[1],
                taux_minimum=row[2]
            )
            # visu des row pendant l'exécution
            # print(row[0])
        print("Import minima Ok")