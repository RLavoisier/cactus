from django.urls import path

from comptes.views import UserSignupView

app_name = "comptes"

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
]