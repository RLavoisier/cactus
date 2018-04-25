from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
        label="Code formation",
        widget=forms.TextInput,
        strip=False,
        help_text="Entrez le code fourni par le responsable de la formation."
    )

    class Meta:
        model = get_user_model()
        fields = ("email",)

    def clean_code_formation(self):
        if self.cleaned_data["code_formation"] != "cfa":
            raise forms.ValidationError("Code formation inconnu.")
        return self.cleaned_data["code_formation"]
