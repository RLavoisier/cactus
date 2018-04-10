from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from saisiecontrat.models import Alternant


def accueil(request):
    # logout(request)
    # On vérifie que l'utilisateur est loggé
    if not request.user.is_authenticated:
        return redirect("comptes:signup_or_login")
    else:
        return redirect("creationcontrat")