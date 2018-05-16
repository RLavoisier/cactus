from django.contrib.auth import login, authenticate

# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from comptes.forms import CactusUserCreationForm
from saisiecontrat.models import Alternant


class UserSignupView(CreateView):
    """
    Vue servant à l'enregistrement d'un utilisateur
    """
    template_name = "registration/signup.html"
    form_class = CactusUserCreationForm
    success_url = reverse_lazy("creationcontrat")

    def form_valid(self, form):
        is_valid =  super().form_valid(form)

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]

        user = authenticate(email=email, password=password)
        login(self.request, user)

        alternant = Alternant()
        alternant.user = user

        # Stockage du code d'accès dans l'alternant
        if form.cleaned_data["code_formation"]:
            alternant.code_acces = form.cleaned_data["code_formation"]

        alternant.save()

        return is_valid

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["signup_form"] = CactusUserCreationForm()
        context["login_form"] = AuthenticationForm()

        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
            return redirect("creationcontrat")
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("login"):
            self.form_class = AuthenticationForm
        elif request.POST.get("signup"):
            self.form_class = CactusUserCreationForm

        return super().post(request, *args, **kwargs)

class UserSignupOrLoginView(LoginView):
    template_name = "registration/signup_login.html"
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["signup_form"] = CactusUserCreationForm()
        context["login_form"] = AuthenticationForm()

        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            #return redirect(reverse_lazy("accueil"))
            return redirect(reverse("creationcontrat"))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("login"):
            self.form_class = AuthenticationForm
        elif request.POST.get("signup"):
            self.form_class = CactusUserCreationForm

        return super().post(request, *args, **kwargs)