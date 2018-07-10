from datetime import datetime

from django.http import JsonResponse
from collections import namedtuple

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from saisiecontrat.utils.fonctions_metier import PeriodesFormationManager


ApiResponse = namedtuple("ApiReponse", ("success", "response", "data"))

@method_decorator(csrf_exempt, name='dispatch')
class ValiderDateDebutContrat(View):
    """
    Cette vue renvoi vrai si la date de début de
    contrat passée dans le post est valide

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
        type_derogation = request.POST["type_derogation"]

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
        # formation = Formation.objects.get(code_formation="1351140684007")
        contrat = request.user.alternant.get_contrat_courant()
        formation = contrat.formation

        try:
            debut_contrat_valide = PeriodesFormationManager.controle_debut_contrat(date_saisie,formation.an_1_du, type_derogation)
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


@method_decorator(csrf_exempt, name='dispatch')
class ValiderDateFinContrat(View):
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
        # formation = Formation.objects.get(code_formation="1351140684007")
        contrat = request.user.alternant.get_contrat_courant()
        formation = contrat.formation

        fin_formation = formation.an_3_au or formation.an_2_au or formation.an_1_au

        try:
            fin_contrat_valide = PeriodesFormationManager.controle_fin_contrat(date_saisie,
                                                                              fin_formation)

            response = ApiResponse(
                success=fin_contrat_valide,
                response="",
                data={}
            )
        except Exception as e:
            response = ApiResponse(
                success=False,
                response=str(e),
                data={}
            )

        print(response._asdict())
        return JsonResponse(response._asdict())


@method_decorator(csrf_exempt, name='dispatch')
class RecupererAnneesFormations(View):
    """
    Cette vue permet de récupérer les différentes années de formations ainsi que les valeurs associées
    """
    def post(self, request):
        if not request.POST.get("date_debut_contrat") or \
                not request.POST.get("date_fin_contrat"):
            response = ApiResponse(
                success=False,
                response="Une date de début et de fn de contrat doit être renseignée",
                data={}
            )
            return JsonResponse(response._asdict())

        date_debut_contrat_str = request.POST["date_debut_contrat"]
        date_fin_contrat_str = request.POST["date_fin_contrat"]

        # conversion de la date saisie en datetime
        try:
            date_debut_contrat = datetime.strptime(date_debut_contrat_str, "%d/%m/%y")
            date_fin_contrat = datetime.strptime(date_fin_contrat_str, "%d/%m/%y")
        except ValueError:
            response = ApiResponse(
                success=False,
                response="Impossible d'interpréter la date %s" % date_debut_contrat_str,
                data={}
            )
            return JsonResponse(response._asdict())

        # Récupération de l'alternant, du contrat et de la formation
        alternant = request.user.alternant
        contrat  = alternant.get_contrat_courant()
        formation = contrat.formation

        # Prévue initialement, la gestion d'un nombre d'années personnalisé n'a pas été maintenue (problème de dates)
        # seul le nombre_annees de la formation est utilisé
        #if contrat.nombre_annees:
        #    nb_annee = contrat.nombre_annees
        #else:
        nb_annee = formation.nombre_annees

        # Calcul des années
        pm = PeriodesFormationManager(alternant.date_naissance,
                                      date_debut_contrat,
                                      date_fin_contrat,
                                      nb_annee,
                                      formation)

        pm.calculer_annees()

        response = ApiResponse(
            success=True,
            response="",
            data={
                "annees": pm.annees,
                "salaire": pm.salaire
            }
        )

        return JsonResponse(response._asdict())