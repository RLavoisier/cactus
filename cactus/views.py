from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from saisiecontrat.models import Alternant


def accueil(request):
    # logout(request)
    # On vérifie que l'utilisateur est loggé
    if not request.user.is_authenticated:
        return redirect("comptes:signup")
    else:
        try:
            alternant = Alternant(user=request.user)
        except ObjectDoesNotExist:
            alternant = None

        context = {
            "user": request.user,
            "alternant": alternant
        }
    # on retourne la page d'accueil
    return render(request, "index.html", context)