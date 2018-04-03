# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from saisiecontrat.models import Contrat

class LoginForm(forms.Form):
  email = forms.EmailField(label='Courriel :')
  password = forms.CharField(label='Mot de passe :', widget=forms.PasswordInput)

  def clean(self):
    cleaned_data = super(LoginForm, self).clean()
    email = cleaned_data.get("email")
    password = cleaned_data.get("password")

    # Vérifie que les deux champs sont valides
    if email and password:
        result = User.objects.filter(email=email, password=password)
        if len(result) != 0:
            raise forms.ValidationError("Courriel inexistant ou mot de passe erroné.")

    return cleaned_data

class CreationContratForm(forms.Form):

  type_contrat_avenant = forms.ChoiceField(label='Type de contrat/avenant :',
                                         widget=forms.Select(choices=Contrat.TYPE_CONTRAT_AVENANT),
                                         required=True)
  mode_contractuel = forms.ChoiceField(label='Mode contractuel :',
                                      widget=forms.Select(choices=Contrat.MODE_CONTRACTUEL),
                                      required=True)

  def clean(self):
    cleaned_data = super(CreationContratForm, self).clean()
    type_contrat_avenant = cleaned_data.get("type_contrat_avenant")
    mode_contractuel = cleaned_data.get("mode_contractuel")

    # Vérifie que les deux champs sont valides
    if not (typecontratavenant and modecontractuel):
        raise forms.ValidationError("Vous devez renseigner ces données pour créer le contrat")

    return cleaned_data
