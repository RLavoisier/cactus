# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from saisiecontrat.models import Contrat, Entreprise


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
    if not (type_contrat_avenant and mode_contractuel):
        raise forms.ValidationError("Vous devez renseigner ces données pour créer le contrat")

    return cleaned_data


class CreationEntrepriseForm(forms.ModelForm):

    class Meta:
        """
        Cette classe est propre au form de type "Model Form"
        On y paramètre toutes les information du modèle lié ainsi que la définition des champs
        """
        model = Entreprise
        fields = ("__all__")

        # Si vous souhaitez éditez les widgets des champs (si ceux par défaut ne vous conviennent pas
        widgets = {
            "numero_SIRET": forms.TextInput()
        }

    # Vous pouvez définir une methode clean_*nom de votre champ* qui servira a valider ce dernier
    def clean_numero_SIRET(self):
        siret = self.cleaned_data["numero_SIRET"]

        # Code de validation du numéro de SIRET
        # Ecrire la logique puis renvoyer la valeur si elle est juste, sinon erreur de validation
        if True:
            return siret
        else:
            raise forms.ValidationError("Le numéro de siret n'est pas au bon format")