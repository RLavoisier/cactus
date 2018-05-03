from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from saisiecontrat.models import Minima


class Periode(object):
    """
    Cette class represente une période de formation
    """
    def __init__(self, du=None, au=None, base=0, taux=0):
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
        for i, p in enumerate([self.periode1, self.periode2]):
            period = "periode%d" % (i + 1)
            if not p:
                continue
            ret_dict[period] = {
                "du": p.du.strftime("%d/%m/%y"),
                "au": p.au.strftime("%d/%m/%y"),
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

    param date_fin_contrat: la date de fin du contrat
    :type date_fin_contrat: datetime

    :param duree_formation: La durée de la formation
    :type duree_formation: int

    :param formation: l'objet formation
    :type formation: Formation
    """
    def __init__(self, date_naissance_alternant, date_debut_contrat,
                 date_fin_contrat, duree_formation, formation):
        self.date_naissance_alternant = date_naissance_alternant
        self.date_debut_contrat = date_debut_contrat
        self.date_fin_contrat = date_fin_contrat
        self.duree_formation = duree_formation
        self.formation = formation
        self.date_fin_formation = formation.an_3_du or formation.an_2_du or formation.an_1_du
        self.premiere_annee_remuneration = self.formation.annee_remuneration_annee_diplome - duree_formation + 1
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

        date_debut_annee = self.date_debut_contrat + relativedelta(years=annee_formation)

        date_fin_annee = date_debut_annee + relativedelta(years=1)

        annee_en_cours = self.premiere_annee_remuneration + annee_formation

        # Si annee est égale à l'annee de diplome, on sort
        if (annee_formation == self.duree_formation) and \
                (self.date_fin_contrat.date() > self.date_fin_formation):
            # On ajoute juste un année avec une seule période jusqu'à la fin du contrat
            age_alternant = self.__age_alternant_a_date(date_debut_annee)
            taux = self.__get_minima_taux(age_alternant, annee_en_cours)
            periode1 = Periode(date_debut_annee, self.date_fin_contrat, taux=taux)
            annee = AnneeFormation(periode1, None)
            self.annees["annee%d" % annee_en_cours] = annee.to_dict()
            return

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


        # Calcul de l'âge de l'aternant
        age_alternant = self.__age_alternant_a_date(date_debut_annee)

        # On récupère l'object minima concerné
        taux_minimum = self.__get_minima_taux(age_alternant,
                                              annee_en_cours)

        # Création de la période
        periode1 = Periode(date_debut_annee, date_fin_periode1,
                           taux=taux_minimum)

        # Calcul de la seconde période
        taux_minimum = self.__get_minima_taux(age_alternant+1,
                                              annee_en_cours)

        fin_periode_2 = date_fin_annee - timedelta(days=1)

        # Gestion de la fin de période supérieur à la date de fin de contrat
        derniere_periode = False
        if fin_periode_2 > self.date_fin_contrat:
            fin_periode_2 = self.date_fin_contrat
            derniere_periode = True

        periode2 = Periode(date_fin_periode1 + timedelta(days=1),
                           fin_periode_2,
                           taux=taux_minimum)

        # Création de la période
        annee = AnneeFormation(periode1, periode2)

        self.annees["annee%d" % annee_en_cours] = annee.to_dict()

        if not derniere_periode:
            return self.calculer_annees(annee_formation+1)

    @staticmethod
    def __get_minima_taux(age, annee):
        """
        Cette méthode récupère le minima correspondant à l'age et l'année passée en argument
        :param age:
        :param annee:
        :return:
        """
        try:
            minima = Minima.objects.filter(age__lte=age,
                                           annee__lte=annee).order_by("-annee", "-age")[0]

            #print("Taux Minima pour annee %d - age %d : %s (id: %s)" % (annee,
            #                                                            age,
            #                                                            minima.taux_minimum,
            #                                                            minima.id))

            return minima.taux_minimum
        except:
            return 0

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
    def controle_debut_contrat(self, date_debut_contrat, date_debut_formation, type_derogation):
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

        if type_derogation in ["31", "50"]:
            return True
        else:
            min_debut_contrat = date_debut_formation - relativedelta(months=3)
            max_debut_contrat = date_debut_formation + relativedelta(months=3)

            return (min_debut_contrat <= date_debut_contrat) & (date_debut_contrat <= max_debut_contrat)


    @classmethod
    def controle_fin_contrat(self, date_fin_contrat, date_fin_formation):
        """
        Cette méthode vérifie si la date de fin de contrat est valide selon la règle :

        date_fin_formation < contrat.date_fin_contrat <= date_fin_formation + 2 mois

        :param date_fin_contrat: la date de fin de contrat
        :type date_fin_contrat; datetime

        :param date_fin_formation: la date de fin de formation
        :type date_fin_formation: datetime

        :return: Valid
        :type: bool
        """
        min_fin_contrat = date_fin_formation
        max_fin_contrat = date_fin_formation + relativedelta(months=2)

        return (min_fin_contrat <= date_fin_contrat) & (date_fin_contrat <= max_fin_contrat)
