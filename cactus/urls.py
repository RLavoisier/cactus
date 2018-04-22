"""cactus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from saisiecontrat.views import create_alternant, inform_contrat, inform_mission, \
    liste_formation, detail_formation, appliquer_formation
from django.urls import path, include

from cactus.views import accueil
from saisiecontrat.views import creationcontrat, create_entreprise, creerCERFA, creerfichemission

urlpatterns = [
    path('comptes/', include("comptes.urls"), name="comptes"),
    path('admin/', admin.site.urls),
    path('', accueil, name="accueil"),
    path('accueil/', accueil, name="accueil"),
    path('creationcontrat/',creationcontrat, name="creationcontrat"),
    path('creationentreprise/', create_entreprise, name="creationentreprise"),
    path('creationalternant/', create_alternant, name="creationalternant"),
    path('informationcontrat/', inform_contrat, name="informationcontrat"),
    path('informationmission/', inform_mission, name="informationmission"),
    path('liste_formation/', liste_formation.as_view(), name="liste_formation"),
    path('appliquer_formation/<int:pk>', appliquer_formation.as_view(), name="appliquer_formation"),
    path('detail_formation/', detail_formation.as_view(), name='detail_formation'),
    path('creerCERFA/', creerCERFA.as_view(), name='creerCERFA'),
    path('creerfichemission/', creerfichemission.as_view(), name='creerfichemission')
]
