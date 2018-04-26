from django.urls import path

from cactus_api.views import ValiderDateDebutContrat, RecupererAnneesFormations, ValiderDateFinContrat

urlpatterns = [
    path("valider_date_debut_contrat/", ValiderDateDebutContrat.as_view(), name="valider_date_debut_contrat"),
    path("valider_date_fin_contrat/", ValiderDateFinContrat.as_view(), name="valider_date_fin_contrat"),
    path("recuperer_remuneration/", RecupererAnneesFormations.as_view(), name="recuperer_remuneration"),
]