from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from saisiecontrat.models import Formation


class CactusUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
        strip=False,
    )

    code_formation = forms.CharField(
        label="Code d'accès",
        widget=forms.TextInput,
        strip=False,
        help_text="Entrez le code d'accès fourni par le(la) responsable de la formation."
    )

    class Meta:
        model = get_user_model()
        fields = ("email",)

    def clean_code_formation(self):

        try:
            Formation.objects.get(code_acces=self.cleaned_data["code_formation"])
        except ObjectDoesNotExist:
            raise forms.ValidationError("Code d'accès inconnu.")
        except MultipleObjectsReturned:
            return None

        return self.cleaned_data["code_formation"]
