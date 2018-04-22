import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from saisiecontrat.models import SMIC


class Command(BaseCommand):
    help = 'Importation du SMIC'

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, "SMIC.csv")
        f = open(file, 'r')
        reader = csv.reader(f)
        for row in reader:
            _, created = SMIC.objects.get_or_create(
                du=row[0],
                au=row[1],
                montant=row[2],
            )
            # visu des row pendant l'exécution
            # print(row[0])
        print("Import SMIC Ok")