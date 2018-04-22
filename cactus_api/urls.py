from django.urls import path

from cactus_api.views import ValiderDateDebutContrat

urlpatterns = [
    path("valider_date_debut_contrat/", ValiderDateDebutContrat.as_view(), name="valider_date_debut_contrat"),
]