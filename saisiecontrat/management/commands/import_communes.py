import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from saisiecontrat.models import Commune


class Command(BaseCommand):
    help = 'Importation des communes'

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, "Communes.csv")
        f = open(file, 'r')
        reader = csv.reader(f)
        for row in reader:
            _, created = Commune.objects.get_or_create(
                code_INSEE=row[0],
                code_postal=row[1],
                libelle=row[2]
            )
