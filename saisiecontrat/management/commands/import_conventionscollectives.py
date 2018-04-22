import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from saisiecontrat.models import ConventionCollective


class Command(BaseCommand):
    help = 'Importation des communes'

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, "ConventionsCollectives.csv")
        f = open(file, 'r')
        reader = csv.reader(f)
        for row in reader:
            _, created = ConventionCollective.objects.get_or_create(
                code=row[0],
                libelle=row[1]
            )
            # visu des row pendant l'exécution
            # print(row[0])
        print("Import conventions collectives Ok")