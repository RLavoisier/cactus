from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist

from saisiecontrat.models import Minima, SMIC


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
        self.salaire = 0

    def calculer_annees(self, annee_formation=0):
        """
        Cette méthode calcul l'ensemble des années de formation
        """
        derniere_periode = False
        if not self.date_naissance_alternant:
            return None

        date_debut_annee = self.date_debut_contrat + relativedelta(years=annee_formation)

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
        date_debut_mois_suivant_ann = self.__debut_mois_suivant_annversaire(self.date_naissance_alternant)

        # calcul de la première période
        if ((date_debut_annee.month, date_debut_annee.day) >
                (self.date_naissance_alternant.month, self.date_naissance_alternant.day)):
            date_fin_periode1 = datetime(day=date_debut_mois_suivant_ann.day,
                                         month=date_debut_mois_suivant_ann.month,
                                         year=date_debut_annee.year + 1) - relativedelta(days=1)
        else:
            try:
                # Vérification d'un saut d'année pour les anniversaire en décembre
                year_to_add = 0
                if self.date_naissance_alternant.year < date_debut_mois_suivant_ann.year:
                    year_to_add = 1
                date_fin_periode1 = datetime(day=date_debut_mois_suivant_ann.day,
                                             month=date_debut_mois_suivant_ann.month,
                                             year=date_debut_annee.year + year_to_add) - relativedelta(days=1)
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
        if date_fin_periode1 > self.date_fin_contrat:
            date_fin_periode1 = self.date_fin_contrat
            derniere_periode = True
        periode1 = Periode(date_debut_annee, date_fin_periode1,
                           taux=taux_minimum)

        # Calcul de la seconde période
        if not derniere_periode:
            taux_minimum = self.__get_minima_taux(age_alternant+1,
                                                  annee_en_cours)

            fin_periode_2 = date_fin_annee - timedelta(days=1)

            # Gestion de la fin de période supérieur à la date de fin de contrat
            if fin_periode_2 > self.date_fin_contrat:
                fin_periode_2 = self.date_fin_contrat
                derniere_periode = True

            periode2 = Periode(date_fin_periode1 + timedelta(days=1),
                               fin_periode_2,
                               taux=taux_minimum)
        else:
            periode2 = None

        # Création de la période
        annee = AnneeFormation(periode1, periode2)

        self.annees["annee%d" % annee_en_cours] = annee.to_dict()

        # si c'est la première période on calcul la rémunération
        if not self.salaire:
            try:
                smic = SMIC.objects.get(du__year=date_debut_annee.year)
                self.salaire = float("{0:.2f}".format(smic.montant * (taux_minimum / 100)))
            except ObjectDoesNotExist:
                self.salaire = 0

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
        age = age - ((date_base.month, date_base.day) <
                     (self.date_naissance_alternant.month, self.date_naissance_alternant.day))

        return age

    def __debut_mois_suivant_annversaire(self, date_anniversaire):
        """
        Cette méthode retourne le debut du mois suivant l'anniversaire de l'alternant

        :param date_anniversaire: la date d'anniversaire courant de l'alternant
        :type date_anniversaire: datetime

        :return: La date de début de mois suivant
        :rtype: datetime
        """
        debut_mois_anniversaire = date_anniversaire.replace(day=1)
        return debut_mois_anniversaire + relativedelta(months=1)


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
