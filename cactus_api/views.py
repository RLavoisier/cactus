from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from collections import namedtuple

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from saisiecontrat.models import Alternant, Formation
from saisiecontrat.utils.fonctions_metier import PeriodesFormationManager

ApiResponse = namedtuple("ApiReponse", ("success", "response", "data"))

@method_decorator(csrf_exempt, name='dispatch')
class ValiderDateDebutContrat(View):
    """
    Cette vue renvoi vrai si la date de début de contrat passée dans le post est valide
    """
    def post(self, request):
        if not request.POST.get("date_saisie"):
            response = ApiResponse(
                success=False,
                response="Une date doit être renseignée",
                data={}
            )
            return JsonResponse(response._asdict())

        date_saisie_str = request.POST["date_saisie"]

        # conversion de la date saisie en datetime
        try:
            date_saisie = datetime.strptime(date_saisie_str, "%d/%m/%y").date()
        except ValueError:
            response = ApiResponse(
                success=False,
                response="Impossible d'interpréter la date %s" % date_saisie_str,
                data={}
            )
            return JsonResponse(response._asdict())

        # récupération de la formation
        formation = Formation.objects.get(code_formation="1351140684007")

        try:
            debut_contrat_valide = PeriodesFormationManager.controle_debut_contrat(date_saisie,
                                                                                  formation.an_1_du)

            response = ApiResponse(
                success=debut_contrat_valide,
                response="",
                data={}
            )
        except Exception as e:
            response = ApiResponse(
                success=False,
                response=str(e),
                data={}
            )

        return JsonResponse(response._asdict())
        