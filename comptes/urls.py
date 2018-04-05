from django.contrib.auth.views import LoginView
from django.urls import path, include

from comptes.views import UserSignupView, UserSignupOrLoginView

app_name = "comptes"

urlpatterns = [
    path("", UserSignupOrLoginView.as_view(), name="signup_or_login"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("", include("django.contrib.auth.urls")),
]