import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from saisiecontrat.models import CFA


class Command(BaseCommand):
    help = 'Importation du cfa'

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, "CFA.csv")
        f = open(file, 'r')
        reader = csv.reader(f)
        for row in reader:
            _, created = CFA.objects.get_or_create(
                numeroUAI=row[0],
                nom=row[1],
                adresse_numero=row[2],
                adresse_voie=row[3],
                adresse_complement=row[4],
                code_postal=row[5],
                ville=row[6]
            )