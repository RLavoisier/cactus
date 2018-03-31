# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from saisiecontrat.models import Contrat

class LoginForm(forms.Form):
  email = forms.EmailField(label='Courriel :')
  password = forms.CharField(label='Mot de passe :', widget = forms.PasswordInput)

  def clean(self):
    cleaned_data = super(LoginForm, self).clean()
    email = cleaned_data.get("email")
    password = cleaned_data.get("password")

    # Vérifie que les deux champs sont valides
    if email and password:
        result = User.objects.filter(email=email,password=password)
        if len(result) != 0:
            raise forms.ValidationError("Courriel inexistant ou mot de passe erroné.")

    return cleaned_data

class CreationContratForm(forms.Form):
  typecontratavenant = forms.ChoiceField(label='Type de contrat/avenant :',widget=forms.select(),required=True)
  modecontractuel = forms.ChoiceField(label='Mode contractuel :',widget=forms.select(),required=True)

  def clean(self):
    cleaned_data = super(CreationContratForm, self).clean()
    typecontratavenant = cleaned_data.get("typecontratavenant")
    modecontractuel = cleaned_data.get("modecontractuel")

    # Vérifie que les deux champs sont valides
    if not (typecontratavenant and modecontractuel):
        raise forms.ValidationError("Vous devez renseigner ces données pour créer le contrat")

    return cleaned_data
