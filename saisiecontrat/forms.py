# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import InlineField, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field, Div
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from saisiecontrat.models import Contrat, Entreprise, NAF, Alternant, Personnel, ConventionCollective


class CreationContratForm(forms.Form):

    type_contrat_avenant = forms.IntegerField(label='Type de contrat/avenant :',
                                         widget=forms.Select(choices=((0, "---"),) + Contrat.TYPE_CONTRAT_AVENANT),
                                         )
    mode_contractuel = forms.IntegerField(label='Mode contractuel :',
                                      widget=forms.Select(choices=Contrat.MODE_CONTRACTUEL),
                                      )
    date_effet_avenant = forms.DateField(required=False)
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

    civilite_ma_1 = forms.IntegerField(widget=forms.Select(choices=Personnel.CIVILITE))
    nom_ma_1 = forms.CharField(max_length=40)
    prenom_ma_1 = forms.CharField(max_length=40)
    date_naissance_ma_1 = forms.DateField()
    civilite_ma_2 = forms.IntegerField(widget=forms.Select(choices=Personnel.CIVILITE))
    nom_ma_2= forms.CharField(max_length=40, required=False)
    prenom_ma_2 = forms.CharField(max_length=40, required=False)
    date_naissance_ma_2 = forms.DateField(required=False)

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

    def clean_raison_sociale(self):

        raisonsociale = self.cleaned_data["raison_sociale"]

        if raisonsociale is None:
            raise forms.ValidationError("La raison sociale doit être renseignée.")
        else:
            return raisonsociale

    def clean_adresse_voie(self):

        adresse_voie = self.cleaned_data["adresse_voie"]

        if adresse_voie is None:
            raise forms.ValidationError("L'adresse doit être renseignée.")
        else:
            return adresse_voie

    def clean_code_postal(self):

        code_postal = self.cleaned_data["code_postal"]

        if code_postal is None:
            raise forms.ValidationError("Le code postal doit être renseigné.")
        else:
            return code_postal

    def clean_ville(self):

        ville = self.cleaned_data["ville"]

        if ville is None:
            raise forms.ValidationError("La ville doit être renseignée.")
        else:
            return ville

    # Vous pouvez définir une methode clean_*nom de votre champ* qui servira a valider ce dernier
    def clean_numero_SIRET(self):

        siret = self.cleaned_data["numero_SIRET"]

        # Code de validation du numéro de SIRET
        # Ecrire la logique puis renvoyer la valeur si elle est juste, sinon erreur de validation

        if siret is None:
            raise forms.ValidationError("Le SIRET doit être renseigné.")
        else:
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

        result = NAF.objects.filter(code=codeape)
        if len(result) != 0:
            return codeape
        else:
            raise forms.ValidationError("Le code NAF %s n'existe pas." % codeape)

    def clean_type_employeur(self):

        type_employeur = self.cleaned_data["type_employeur"]
        if type_employeur is None:
            raise forms.ValidationError("Sélectionnez un type d'employeur dans la liste proposée.")
        else:
            return type_employeur

    def clean_effectif_entreprise(self):

        effectif_entreprise = self.cleaned_data["effectif_entreprise"]

        if effectif_entreprise is None:
            raise forms.ValidationError("L'effectif salarié de l'entreprise doit être renseigné.")
        else:
            return effectif_entreprise

    def clean_telephone(self):

        telephone = self.cleaned_data["telephone"]

        if telephone is None:
            raise forms.ValidationError("Le numéro de téléphone doit être renseigné.")
        else:
            return telephone

    def clean_telecopie(self):

        telecopie = self.cleaned_data["telecopie"]

        if telecopie is None:
            raise forms.ValidationError("Le numéro de télécopie de l'entreprise doit être renseigné.")
        else:
            return telecopie

    def clean_courriel(self):

        courriel = self.cleaned_data["courriel"]

        if courriel is None:
            raise forms.ValidationError("Le courriel de l'entreprise doit être renseigné.")
        else:
            return courriel

    def clean_code_convention_collective(self):

        code_convention_collective = self.cleaned_data.get("code_convention_collective")

        if code_convention_collective is None:
            raise forms.ValidationError("Le code de la convention collective doit être renseigné.")
        else:
            return code_convention_collective

    def clean_libelle_convention_collective(self):

        libelle_convention_collective = self.cleaned_data.get("libelle_convention_collective")
        code_convention_collective = self.cleaned_data.get("code_convention_collective")

        if not code_convention_collective is None:
            try:
                conventioncollective = ConventionCollective.objects.get(code=self.cleaned_data.get("code_convention_collective"))
            except ObjectDoesNotExist:
                conventioncollective = None

            if conventioncollective is None and libelle_convention_collective is None:
                raise forms.ValidationError("La convention collective %s est inconnue, veuillez renseigner le libellé." % (code_convention_collective))
            else:
                return libelle_convention_collective

    def clean_nom_ma_1(self):

        nom_ma_1 = self.cleaned_data["nom_ma_1"]

        if nom_ma_1 is None:
            raise forms.ValidationError("Le nom du maître d'apprentissage doit être renseigné.")
        else:
            return nom_ma_1

    def clean_prenom_ma_1(self):

        prenom_ma_1 = self.cleaned_data["prenom_ma_1"]

        if prenom_ma_1 is None:
            raise forms.ValidationError("Le prénom du maître d'apprentissage doit être renseigné.")
        else:
            return prenom_ma_1

    def clean_date_naissance_ma_1(self):

        date_naissance_ma_1 = self.cleaned_data["date_naissance_ma_1"]

        if date_naissance_ma_1 is None:
            raise forms.ValidationError("La date de naissance du maître d'apprentissage doit être renseigné.")
        else:
            return date_naissance_ma_1


class CreationAlternantForm(forms.ModelForm):

    class Meta:
        """
        Cette classe est propre au form de type "Model Form"
        On y paramètre toutes les information du modèle lié ainsi que la définition des champs
        """
        model = Alternant
        fields = ("__all__")

        exclude = ["date_maj", "user", "courriel"]

        # Si vous souhaitez éditez les widgets des champs (si ceux par défaut ne vous conviennent pas
        widgets = {

        }

    def clean_handicape(self):
        if self.cleaned_data["handicape"] == "on":
            return True
        else:
            return False

    def clean_nom(self):

        nom = self.cleaned_data.get("nom")

        if nom is None:
            raise forms.ValidationError("Le nom doit être renseigné.")
        else:
            return nom

    def clean_prenom(self):

        prenom = self.cleaned_data.get("prenom")

        if prenom is None:
            raise forms.ValidationError("Le prénom doit être renseigné.")
        else:
            return prenom

    def clean_date_naissance(self):

        date_naissance = self.cleaned_data.get("date_naissance")

        if date_naissance is None:
            raise forms.ValidationError("Le date de naissance doit être renseignée.")
        else:
            return date_naissance

    def clean_numero_departement_naissance(self):

        numero_departement_naissance = self.cleaned_data.get("numero_departement_naissance")

        if numero_departement_naissance is None:
            raise forms.ValidationError("Le numéro_de département de naissance doit être renseigné.")
        else:
            return numero_departement_naissance

    def clean_commune_naissance(self):

        commune_naissance = self.cleaned_data.get("commune_naissance")

        if commune_naissance is None:
            raise forms.ValidationError("La commune de naissance doit être renseignée.")
        else:
            return commune_naissance

    def clean_adresse_voie(self):

        adresse_voie = self.cleaned_data.get("adresse_voie")

        if adresse_voie is None:
            raise forms.ValidationError("La voie doit être renseignée.")
        else:
            return adresse_voie

    def clean_code_postal(self):

        code_postal = self.cleaned_data.get("code_postal")

        if code_postal is None:
            raise forms.ValidationError("Le code postal doit être renseigné.")
        else:
            return code_postal

    def clean_ville(self):

        ville = self.cleaned_data.get("ville")

        if ville is None:
            raise forms.ValidationError("La ville doit être renseignée.")
        else:
            return ville

    def clean_telephone(self):

        telephone = self.cleaned_data.get("telephone")

        if telephone is None:
            raise forms.ValidationError("Le téléphone doit être renseigné.")
        else:
            return telephone

    def clean_nationalite(self):

        nationalite = self.cleaned_data.get("nationalite")

        if nationalite is None:
            raise forms.ValidationError("La nationalité doit être renseignée.")
        else:
            return nationalite

    def clean_regime_social(self):

        regime_social = self.cleaned_data.get("regime_social")

        if regime_social is None:
            raise forms.ValidationError("Le régime social doit être renseigné.")
        else:
            return regime_social

    def clean_situation_avant_contrat(self):

        situation_avant_contrat = self.cleaned_data.get("situation_avant_contrat")

        if situation_avant_contrat is None:
            raise forms.ValidationError("La situation avant contrat doit être renseignée.")
        else:
            return situation_avant_contrat

    def clean_dernier_diplome_prepare(self):

        dernier_diplome_prepare = self.cleaned_data.get("dernier_diplome_prepare")

        if dernier_diplome_prepare is None:
            raise forms.ValidationError("Le dernier diplôme préparé doit être renseigné.")
        else:
            return dernier_diplome_prepare

    def clean_derniere_annee_suivie(self):

        derniere_annee_suivie = self.cleaned_data.get("derniere_annee_suivie")

        if derniere_annee_suivie is None:
            raise forms.ValidationError("La dernière année suivie pour le dernier diplôme préparé doit être renseignée.")
        else:
            return derniere_annee_suivie

    def clean_intitule_dernier_diplome_prepare(self):

        intitule_dernier_diplome_prepare = self.cleaned_data.get("intitule_dernier_diplome_prepare")

        if intitule_dernier_diplome_prepare is None:
            raise forms.ValidationError("L'intitulé précis du dernier diplôme préparé être renseignée.")
        else:
            return intitule_dernier_diplome_prepare

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
                   "date_maj", "date_generation_CERFA", "date_exportation_CFA","date_saisie_complete","nombre_années",
                   "attestation_pieces", "attestation_maitre_apprentissage"]

        labels = {
            "an_1_per_1_du": "Période 1 du :",
            "an_1_per_1_au": "Période 1 au :",
            "an_1_per_1_taux": "Taux :",
            "an_1_per_1_base": "Base :",
            "an_1_per_2_du": "Période 2 du :",
            "an_1_per_2_au": "Période 2 au :",
            "an_1_per_2_taux": "Taux :",
            "an_1_per_2_base": "Base :",
            "an_2_per_1_du": "Période 1 du :",
            "an_2_per_1_au": "Période 1 au :",
            "an_2_per_1_taux": "Taux :",
            "an_2_per_1_base": "Base :",
            "an_2_per_2_du": "Période 2 du :",
            "an_2_per_2_au": "Période 2 au :",
            "an_2_per_2_taux": "Taux :",
            "an_2_per_2_base": "Base :",
        }

        # Si vous souhaitez, éditez les widgets des champs (si ceux par défaut ne vous conviennent pas
        widgets = {
            "date_embauche": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "date_debut_contrat": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "date_fin_contrat": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "date_effet_avenant": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_1_per_1_du": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_1_per_1_au": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_1_per_2_du": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_1_per_2_au": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_1_per_1_taux": forms.TextInput(attrs={"class": "form-control"}),
            "an_1_per_1_base": forms.TextInput(attrs={"class": "form-control"}),
            "an_1_per_2_taux": forms.TextInput(attrs={"class": "form-control"}),
            "an_1_per_2_base": forms.TextInput(attrs={"class": "form-control"}),
            "an_2_per_1_du": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_2_per_1_au": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_2_per_2_du": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_2_per_2_au": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "an_2_per_1_taux": forms.TextInput(attrs={"class": "form-control"}),
            "an_2_per_1_base": forms.TextInput(attrs={"class": "form-control"}),
            "an_2_per_2_taux": forms.TextInput(attrs={"class": "form-control"}),
            "an_2_per_2_base": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)


    def clean_date_embauche(self):

        date_embauche = self.cleaned_data.get("date_embauche")

        if date_embauche is None:
            raise forms.ValidationError("La date d'embauche doit être renseignée.")
        else:
            return date_embauche

    def clean_date_debut_contrat(self):

        date_debut_contrat = self.cleaned_data.get("date_debut_contrat")

        if date_debut_contrat is None:
            raise forms.ValidationError("La date de début de contrat doit être renseignée.")
        else:
            return date_debut_contrat

    def clean_date_effet_avenant(self):

        date_effet_avenant = self.cleaned_data.get("date_effet_avenant")
        alternant = Alternant(user=self.request.user)
        contrat = Contrat.objects.get(alternant=alternant, contrat_courant=True)

        if contrat.type_contrat_avenant in (31, 32, 33,34,35,36):
            if date_effet_avenant is None:
                raise forms.ValidationError("La date d'effet de l'avenant doit être renseignée.")
            else:
                return date_effet_avenant

    def clean_date_fin_contrat(self):

        date_fin_contrat = self.cleaned_data.get("date_fin_contrat")

        if date_fin_contrat is None:
            raise forms.ValidationError("La date de fin de contrat doit être renseignée.")
        else:
            return date_fin_contrat

    def clean_duree_hebdomadaire_travail(self):

        duree_hebdomadaire_travail = self.cleaned_data.get("duree_hebdomadaire_travail")

        if duree_hebdomadaire_travail is None:
            raise forms.ValidationError("La durée hebdomadaire du travail doit être renseignée.")
        else:
            return duree_hebdomadaire_travail


class InformationMissionForm(forms.ModelForm):

    class Meta:
        """
        Cette classe est propre au form de type "Model Form"
        On y paramètre toutes les information du modèle lié ainsi que la définition des champs
        """
        model = Contrat
        fields = ['mission']

    def clean_mission(self):

        mission = self.cleaned_data.get("mission")

        if mission is None:
            raise forms.ValidationError("Vous devez saisir une mission.")
        else:
            return mission

