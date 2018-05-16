from datetime import datetime
from django.core.management import BaseCommand

from saisiecontrat.models import Formation


class Command(BaseCommand):
    help = 'Importation des formations'

    def handle(self, *args, **options):

        formations = Formation.objects.all()

        for formation in formations:
            if formation.an_1_du.year == 1899:
                formation.an_1_du = None
            if formation.an_1_au.year == 1899:
                formation.an_1_au = None
            if formation.an_2_du.year == 1899:
                formation.an_2_du = None
            if formation.an_2_au.year == 1899:
                formation.an_2_au = None
            if formation.an_3_du.year == 1899:
                formation.an_3_du = None
            if formation.an_3_au.year == 1899:
                formation.an_3_au = None
            if formation.heures_an_1 == 0:
                formation.heures_an_1 = None
            if formation.heures_an_2 == 0:
                formation.heures_an_2 = None
            if formation.heures_an_3 == 0:
                formation.heures_an_3 = None
            formation.save()
