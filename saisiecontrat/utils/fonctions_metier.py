from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from saisiecontrat.models import Minima


class Periode(object):
    """
    Cette class represente une période de formation
    """
    def __init__(self, du, au, base=0, taux=0):
        self.du = du
        self.au = au
        self.base = base
        self.taux = taux

class AnneeFormation(object):
    """
    Cette classe représente une année de formation
    """
    def __init__(self, periode1, periode2):
        self.periode1 = periode1
        self.periode2 = periode2

    def to_dict(self):
        ret_dict = {}
        for i, p in enumerate(self.periode1, self.periode2):
            period = "periode%d" % (i + 1)
            ret_dict[period] = {
                "du": p.du,
                "au": p.au,
                "base": p.base,
                "taux": p.taux
            }
        return ret_dict


class PeriodesFormationManager(object):
    """
    Cette classe sert de base de calcul des periodes de formations
    ainsi que des taux applicables

    :param date_naissance_alternant: la date de naissance de l'alternant
    :type date_naissance_alternant: datetime

    :param date_debut_contrat: la date de début du contrat
    :type date_debut_contrat: datetime

    :param duree_formation: La durée de la formation
    :type duree_formation: int

    :param date_debut_formation: la date de début de la formation
    :type date_debut_formation: datetime
    """
    def __init__(self, date_naissance_alternant, date_debut_contrat,
                 duree_formation, date_debut_formation,
                 annee_remuneration):
        self.date_naissance_alternant = date_naissance_alternant
        self.date_debut_contrat = date_debut_contrat
        self.duree_formation = duree_formation
        self.date_debut_formation = date_debut_formation
        self.premiere_annee_remuneration = annee_remuneration - duree_formation + 1
        self.annees = {
            "annee1": None,
            "annee2": None,
            "annee3": None,
            "annee4": None,
        }

    def calculer_annees(self, annee_formation=0):
        """
        Cette méthode calcul l'ensemble des années de formation
        """
        # Si annee est égale à l'annee de dilome, on sort
        if annee_formation == self.duree_formation:
            return

        date_debut_annee = self.date_debut_contrat + relativedelta(years=annee_formation)

        date_fin_annee = date_debut_annee + relativedelta(years=1)

        # calcul de la première période
        if ((date_debut_annee.month, date_debut_annee.day) >
                (self.date_naissance_alternant.month, self.date_naissance_alternant.day)):
            date_fin_periode1 = datetime(day=self.date_naissance_alternant.day,
                                         month=self.date_naissance_alternant.month,
                                         year=date_debut_annee.year + 1) - timedelta(days=1)
        else:
            try:
                date_fin_periode1 = datetime(day=self.date_naissance_alternant.day,
                                             month=self.date_naissance_alternant.month,
                                             year=date_debut_annee.year) - timedelta(days=1)
            except ValueError:
                # gestion des alternant nés le 29 fevrier...
                date_fin_periode1 = datetime(day=1,
                                             month=3,
                                             year=date_debut_annee.year) - timedelta(days=1)

        periode1 = Periode(date_debut_annee, date_fin_periode1)


        # Calcul de la seconde période
        periode2 = Periode(date_fin_periode1 + timedelta(days=1),
                           date_fin_annee - timedelta(days=1))

        annee = AnneeFormation(periode1, periode2)

        annee_en_cours = self.premiere_annee_remuneration + annee_formation
        self.annees["annee%d" % annee_en_cours] = annee

        return self.calculer_annees(annee_formation+1)

        #age_alternant = self.__age_alternant_a_date(self.date_debut_contrat)
        #minima = Minima.objects.get()

    def __age_alternant_a_date(self, date_base):
        """
        Cette méthode calcul l'age de l'alternant à une date donnée

        :param date_base: La date à laquelle l'âge doit être déduit
        :type date_base: datetime

        :return: L'age de l'alternant
        :rtype: int
        """
        age = date_base.year - self.date_naissance_alternant.year

        # deduction par rapport aux jours
        age = age - ((date_base.month, date_base.date()) <
                     (self.date_naissance_alternant.month, self.date_naissance_alternant.day))

        return age

    @classmethod
    def controle_debut_contrat(self, date_debut_contrat, date_debut_formation):
        """
        Cette méthode vérifie si la date de début de contrat est valide selon la règle :

        date_debut_formation – 3 mois <= contrat.date_debut_contrat <= date_debut_formation + 3 mois

        :param date_debut_contrat: la date de debut de contrat
        :type date_debut_contrat; datetime

        :param date_debut_formation: la date de début de formation
        :type date_debut_formation: datetime

        :return: Valid
        :type: bool
        """
        min_debut_contrat = date_debut_formation - relativedelta(months=3)
        max_debut_contrat = date_debut_formation + relativedelta(months=3)

        return (min_debut_contrat < date_debut_contrat) & (date_debut_contrat < max_debut_contrat)
