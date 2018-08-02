from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.urls import path, include, reverse_lazy
from django.contrib.auth import urls as auth_urls

from comptes.views import UserSignupView, UserSignupOrLoginView, PasswordResetView

app_name = "comptes"

urlpatterns = [
    path("", UserSignupOrLoginView.as_view(), name="signup_or_login"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserSignupOrLoginView.as_view(), name="login"),
    path('password_reset/',
         PasswordResetView.as_view(success_url=reverse_lazy("comptes:password_reset_done")),
         name='password_reset'),
    path("reset/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(post_reset_login=True,
                                          success_url=reverse_lazy("accueil")),
         name="password_reset_confirm"),
    path("", include("django.contrib.auth.urls")),
]
