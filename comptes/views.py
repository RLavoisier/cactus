from django.contrib.auth import login, authenticate

# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from comptes.forms import CactusUserCreationForm
from saisiecontrat.models import Alternant


class UserSignupView(CreateView):

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
        alternant.save()

        return is_valid

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Si l'utilisateur est authentifié, on le renvoi sur la page d'accueil
            return redirect("creationcontrat")
        else:
            return super().get(request, *args, **kwargs)


class UserSignupOrLoginView(TemplateView):

    template_name = "registration/signup_login.html"

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