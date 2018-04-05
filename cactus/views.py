from django.contrib.auth import logout
from django.shortcuts import render, redirect


def accueil(request):
    # logout(request)
    if not request.user.is_authenticated:
        return redirect("comptes:signup")
    else:
        context = {
            "user": request.user
        }
    return render(request, "index.html", context)