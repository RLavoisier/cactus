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
from saisiecontrat.views import create_alternant, inform_contrat, inform_mission, liste_formation, detail_formation, \
    appliquer_formation, exportypareo, choisirautreformation, exporttotal
from django.urls import path, include

from cactus.views import accueil
from saisiecontrat.views import creationcontrat, create_entreprise, telechargerCERFA, cerfa, envoyermailvalidationraf, recapinscriptions, envoyerficheraf,validationmission

urlpatterns = [
    path('comptes/', include("comptes.urls"), name="comptes"),
    path('api/', include("cactus_api.urls"), name="api"),
    path('admin/', admin.site.urls, name="admin"),
    path('', accueil, name="accueil"),
    path('accueil/', accueil, name="accueil"),
    path('creationcontrat/',creationcontrat, name="creationcontrat"),
    path('creationentreprise/', create_entreprise, name="creationentreprise"),
    path('creationalternant/', create_alternant, name="creationalternant"),
    path('informationcontrat/', inform_contrat, name="informationcontrat"),
    path('informationmission/', inform_mission, name="informationmission"),
    path('liste_formation/', liste_formation.as_view(), name="liste_formation"),
    path('appliquer_formation/<str:pk>', appliquer_formation.as_view(), name="appliquer_formation"),
    path('detail_formation/', detail_formation.as_view(), name='detail_formation'),
    path('cerfa/', cerfa, name='cerfa'),
    path('telechargerCERFA/', telechargerCERFA.as_view(), name='telechargerCERFA'),
    path('envoyerficheraf/<str:alternant_hash>/', envoyerficheraf, name='envoyerficheraf'),
    path('validationmission/<str:alternant_hash>/', validationmission, name='validationmission'),
    path('envoyermailvalidationraf/', envoyermailvalidationraf, name='envoyermailvalidationraf'),
    path('choisirautreformation/', choisirautreformation, name='choisirautreformation'),
    path('recapinscriptions/<str:formation_hash>/', recapinscriptions, name='recapinscriptions'),
    path('exportypareo/<str:cfa_hash>/<str:email_livraison>/<str:aaaammjj_du>/<str:aaaammjj_au>/<int:extraction>/<int:etat>', exportypareo, name='exportypareo'),
    path('exporttotal/<str:cfa_hash>/<str:email_livraison>', exporttotal, name='exporttotal'),
]
