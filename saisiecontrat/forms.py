# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from saisiecontrat.models import Contrat, Entreprise, NAF, Alternant


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

  type_contrat_avenant = forms.IntegerField(label='Type de contrat/avenant :',
                                         widget=forms.Select(choices=Contrat.TYPE_CONTRAT_AVENANT),
                                         required=True)
  mode_contractuel = forms.IntegerField(label='Mode contractuel :',
                                      widget=forms.Select(choices=Contrat.MODE_CONTRACTUEL),
                                      required=True)
  numero_contrat_anterieur = forms.CharField(required=False)

  def clean(self):

    cleaned_data = super(CreationContratForm, self).clean()
    type_contrat_avenant = cleaned_data.get("type_contrat_avenant")
    mode_contractuel = cleaned_data.get("mode_contractuel")
    numero_contrat_anterieur = cleaned_data.get("numero_contrat_anterieur")

    # Vérifie que les deux champs sont valides
    if not (type_contrat_avenant and mode_contractuel):
        raise forms.ValidationError("Vous devez renseigner ces données pour créer le contrat")
    else:
        if len(numero_contrat_anterieur) == 0 and type_contrat_avenant in (21,31,32,33,34,35,36):
            raise forms.ValidationError("Le numéro de contrat antérieur doit être renseigné pour les avenants et les renouvellements de contrat chez le même employeur.")


    return cleaned_data


class CreationEntrepriseForm(forms.ModelForm):

    class Meta:
        """
        Cette classe est propre au form de type "Model Form"
        On y paramètre toutes les information du modèle lié ainsi que la définition des champs
        """
        model = Entreprise
        fields = ("__all__")

        exclude = ["secteur_employeur", "date_maj", "date_maj_contacts"]

        # Si vous souhaitez éditez les widgets des champs (si ceux par défaut ne vous conviennent pas
        widgets = {
            "courriel": forms.EmailInput(),

        }

    # Vous pouvez définir une methode clean_*nom de votre champ* qui servira a valider ce dernier

    def clean_numero_SIRET(self):

        siret = self.cleaned_data["numero_SIRET"]

        # Code de validation du numéro de SIRET
        # Ecrire la logique puis renvoyer la valeur si elle est juste, sinon erreur de validation

        S=0

        if len(siret) == 14:
            for i in range(1, 14):
                if divmod(i, 2)[1] == 1:
                    if int(siret[i]) < 5:
                        S += int(siret[i]) * 2
                    else:
                        S += int(siret[i]) * 2 - 9
                else:
                    S += int(siret[i])

            # Le code SIREN 356000000 est celui de la poste dont le modulo de S est fait par 5 et non 10
            if (siret[0:9]=="356000000" and divmod(S,5)[1] == 0) or (siret[0:9]!="356000000" and divmod(S,10)[1] == 0):
                return siret
            else:
                raise forms.ValidationError("Le SIRET n'est pas valide.")
        else:
            raise forms.ValidationError("Le SIRET doit comporter 14 caractères numériques.")


    def clean_code_APE(self):

        codeape = self.cleaned_data["code_APE"]

        result = NAF.Objects.filter(code=codeape)
        if len(result) != 0:
            return codeape
        else:
            raise forms.ValidationError("Le code NAF %s n'existe pas." % codeape)

class CreationAlternantForm(forms.ModelForm):

    class Meta:
        """
        Cette classe est propre au form de type "Model Form"
        On y paramètre toutes les information du modèle lié ainsi que la définition des champs
        """
        model = Alternant
        fields = ("__all__")

        exclude = ["date_maj"]

        # Si vous souhaitez éditez les widgets des champs (si ceux par défaut ne vous conviennent pas
        widgets = {

        }

class InformationContratForm(forms.ModelForm):

    class Meta:
        """
        Cette classe est propre au form de type "Model Form"
        On y paramètre toutes les information du modèle lié ainsi que la définition des champs
        """
        model = Contrat
        fields = ("__all__")

        exclude = ["date_maj", "type_contrat_avenant", "mode_contractuel", "numero_contrat_anterieur", "alternant",
                   "formation", "entreprise", "mission", "date_inscription", "contrat_courant", "date_maj_mission",
                   "date_maj", "date_generation_CERFA", "date_exportation_CFA"]

        # Si vous souhaitez éditez les widgets des champs (si ceux par défaut ne vous conviennent pas
        widgets = {

        }

class InformationMissionForm(forms.ModelForm):

    class Meta:
        """
        Cette classe est propre au form de type "Model Form"
        On y paramètre toutes les information du modèle lié ainsi que la définition des champs
        """
        model = Contrat
        fields = ['mission']

    def clean_mission(self):

       raise forms.ValidationError("Mission erronée.")
