from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
import datetime


User = get_user_model()


class Alternant(models.Model):


    SEXE = (
        ('M','M'),
        ('F','F'),
    )

    NATIONALITE = (
        (1, "Française"),
        (2, "Union Européenne"),
        (3, "Etranger hors Union Européenne"),
    )

    REGIME_SOCIAL = (
        (1, "MSA"),
        (2, "URSSAF"),
    )

    SITUATION_AVANT_CONTRAT = (
        (1, "Scolaire (hors DIMA)"),
        (2, "Dispositif d’initiation aux métiers en alternance (DIMA) ou autre classe préparatoire à l’apprentissage (CLIPA, CPA...)"),
        (3, "Etudiant"),
        (4, "Contrat d’apprentissage"),
        (5, "Contrat de professionnalisation"),
        (6, "Contrat aidé"),
        (7, "Stagiaire de la formation professionnelle"),
        (8, "Salarié"),
        (9, "Personne à la recherche d’un emploi (inscrite ou non au Pôle Emploi)"),
        (10, "Inactif"),
    )

    DIPLOME = (
        (10, "Doctorat"),
        (11, "Master professionnel/DESS/diplôme grande école"),
        (12, "Master recherche/DEA"),
        (19, "Autre diplôme ou titre de niveau bac+5 ou plus"),
        (21, "Master professionnel (M1+M2 ou seul M2)"),
        (22, "Master général (M1+M2 ou seul M2)"),
        (23, "Licence professionnelle"),
        (24, "Licence générale"),
        (29, "Autre diplôme ou titre de niveau bac +3 ou 4"),
        (31, "Brevet de Technicien Supérieur"),
        (32, "Diplôme Universitaire de technologie"),
        (39, "Autre diplôme ou titre de niveau bac+2"),
        (41, "Baccalauréat professionnel"),
        (42, "Baccalauréat général"),
        (43, "Baccalauréat technologique"),
        (49, "Autre diplôme ou titre de niveau bac"),
        (51, "CAP"),
        (52, "BEP"),
        (53, "Mention complémentaire"),
        (59, "Autre diplôme ou titre de niveau CAP/BEP"),
        (60, "Aucun diplôme ni titre professionnel"),
    )

    DERNIERE_ANNEE_SUIVIE = (
        (1, "l’apprenti a suivi la dernière année du cycle de formation et a obtenu le diplôme ou titre"),
        (11, "l’apprenti a suivi la 1ère année du cycle et l’a validée (examens réussis mais année non diplômante)"),
        (12, "l’apprenti a suivi la 1ère année du cycle mais ne l’a pas validée (échec aux examens, interruption ou abandon de formation)"),
        (21, "l’apprenti a suivi la 2è année du cycle et l’a validée (examens réussis mais année non diplômante)"),
        (22, "l’apprenti a suivi la 2è année du cycle mais ne l’a pas validée (échec aux examens, interruption ou abandon de formation)"),
        (31, "l’apprenti a suivi la 3è année du cycle et l’a validée (examens réussis mais année non diplômante, cycle adapté)"),
        (32, "l’apprenti a suivi la 3è année du cycle mais ne l’a pas validée (échec aux examens, interruption ou abandon de formation)"),
        (40, "l’apprenti a achevé le 1er cycle de l’enseignement secondaire (collège)"),
        (41, "l’apprenti a interrompu ses études en classe de 3è"),
        (42, "l’apprenti a interrompu ses études en classe de 4è"),
    )

    DEPARTEMENT_NAISSANCE = (
        ("01", "01 Ain"),
        ("02", "02 Aisne"),
        ("03", "03 Allier"),
        ("04", "04 Alpes-de-Haute-Provence"),
        ("05", "05 Hautes-Alpes"),
        ("06", "06 Alpes-Maritimes"),
        ("07", "07 Ardèche"),
        ("08", "08 Ardennes"),
        ("09", "09 Ariège"),
        ("10", "10 Aube"),
        ("11", "11 Aude"),
        ("12", "12 Aveyron"),
        ("13", "13 Bouches-du-Rhône"),
        ("14", "14 Calvados"),
        ("15", "15 Cantal"),
        ("16", "16 Charente"),
        ("17", "17 Charente-Maritime"),
        ("18", "18 Cher"),
        ("19", "19 Corrèze"),
        ("2A", "2A Corse-du-Sud"),
        ("2B", "2B Haute-Corse"),
        ("21", "21 Côte-d'Or"),
        ("22", "22 Côtes-d'Armor"),
        ("23", "23 Creuse"),
        ("24", "24 Dordogne"),
        ("25", "25 Doubs"),
        ("26", "26 Drôme"),
        ("27", "27 Eure"),
        ("28", "28 Eure-et-Loir"),
        ("29", "29 Finistère"),
        ("30", "30 Gard"),
        ("31", "31 Haute-Garonne"),
        ("32", "32 Gers"),
        ("33", "33 Gironde"),
        ("34", "34 Hérault"),
        ("35", "35 Ille-et-Vilaine"),
        ("36", "36 Indre"),
        ("37", "37 Indre-et-Loire"),
        ("38", "38 Isère"),
        ("39", "39 Jura"),
        ("40", "40 Landes"),
        ("41", "41 Loir-et-Cher"),
        ("42", "42 Loire"),
        ("43", "43 Haute-Loire"),
        ("44", "44 Loire-Atlantique"),
        ("45", "45 Loiret"),
        ("46", "46 Lot"),
        ("47", "47 Lot-et-Garonne"),
        ("48", "48 Lozère"),
        ("49", "49 Maine-et-Loire"),
        ("50", "50 Manche"),
        ("51", "51 Marne"),
        ("52", "52 Haute-Marne"),
        ("53", "53 Mayenne"),
        ("54", "54 Meurthe-et-Moselle"),
        ("55", "55 Meuse"),
        ("56", "56 Morbihan"),
        ("57", "57 Moselle"),
        ("58", "58 Nièvre"),
        ("59", "59 Nord"),
        ("60", "60 Oise"),
        ("61", "61 Orne"),
        ("62", "62 Pas-de-Calais"),
        ("63", "63 Puy-de-Dôme"),
        ("64", "64 Pyrénées-Atlantiques"),
        ("65", "65 Hautes-Pyrénées"),
        ("66", "66 Pyrénées-Orientales"),
        ("67", "67 Bas-Rhin"),
        ("68", "68 Haut-Rhin"),
        ("69", "69 Rhône"),
        ("70", "70 Haute-Saône"),
        ("71", "71 Saône-et-Loire"),
        ("72", "72 Sarthe"),
        ("73", "73 Savoie"),
        ("74", "74 Haute-Savoie"),
        ("75", "75 Paris"),
        ("76", "76 Seine-Maritime"),
        ("77", "77 Seine-et-Marne"),
        ("78", "78 Yvelines"),
        ("79", "79 Deux-Sèvres"),
        ("80", "80 Somme"),
        ("81", "81 Tarn"),
        ("82", "82 Tarn-et-Garonne"),
        ("83", "83 Var"),
        ("84", "84 Vaucluse"),
        ("85", "85 Vendée"),
        ("86", "86 Vienne"),
        ("87", "87 Haute-Vienne"),
        ("88", "88 Vosges"),
        ("89", "89 Yonne"),
        ("90", "90 Territoire de Belfort"),
        ("91", "91 Essonne"),
        ("92", "92 Hauts-de-Seine"),
        ("93", "93 Seine-Saint-Denis"),
        ("94", "94 Val-de-Marne"),
        ("95", "95 Val-d'Oise"),
        ("971", "971 Guadeloupe"),
        ("972", "972 Martinique"),
        ("973", "973 Guyane"),
        ("974", "974 La Réunion"),
        ("976", "976 Mayotte"),
        ("099", "099 Né(e) l’étranger"),
    )

    # Le related name permet de renvoyer l'alternant depuis le user avec la syntaxe user.alternant
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True, related_name="alternant")
    nom = models.CharField(max_length=70, blank=True, null=True)
    prenom = models.CharField(verbose_name="Prénom", max_length=35, blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=SEXE, default='M')
    date_naissance = models.DateField(verbose_name="Date de naissance", blank=True, null=True)
    numero_departement_naissance = models.CharField(verbose_name="Département de naissance", max_length=3, choices=DEPARTEMENT_NAISSANCE, help_text="Sélectionnez votre département de naissance ou '099 Né(e) à l'étranger'", blank=True, null=True)
    commune_naissance = models.CharField(verbose_name="Commune de naissance", max_length=60, blank=True, null=True)
    adresse_1 = models.CharField(verbose_name="Adresse", max_length=100, blank=True, null=True)
    adresse_2 = models.CharField(verbose_name="Complément d'adresse", max_length=100, blank=True, null=True)
    code_postal = models.CharField(verbose_name="Code postal", max_length=5, blank=True, null=True)
    ville = models.CharField(max_length=60, blank=True, null=True)
    telephone = models.CharField(verbose_name="Téléphone", max_length=15, blank=True, null=True)
    handicape = models.BooleanField(verbose_name="Travailleur handicapé", default=False)
    courriel = models.CharField(max_length=40, blank=True, null=True)
    nationalite = models.PositiveSmallIntegerField(verbose_name="Nationalité", choices=NATIONALITE, default=1, blank=True, null=True)
    regime_social = models.PositiveSmallIntegerField(verbose_name="Régime social", choices=REGIME_SOCIAL, blank=True, null=True)
    situation_avant_contrat = models.PositiveSmallIntegerField(verbose_name="Situation avant contrat", choices=SITUATION_AVANT_CONTRAT, blank=True, null=True)
    dernier_diplome_prepare = models.PositiveSmallIntegerField(verbose_name="Dernier diplôme ou titre préparé", choices=DIPLOME,
                                                               help_text="Choisissez le dernier diplôme ou titre que vous avez préparé même si le cursus n'a pas été achevé.",
                                                               blank=True, null=True)
    derniere_annee_suivie = models.PositiveSmallIntegerField(verbose_name="Dernière année suivie", choices=DERNIERE_ANNEE_SUIVIE, blank=True, null=True)
    intitule_dernier_diplome_prepare = models.CharField(verbose_name="Intitulé du dernier diplôme obtenu", max_length=100,
                                                        help_text="Saisissez le libellé précis du dernier diplôme préparé.",
                                                        blank = True, null = True)
    diplome_le_plus_eleve = models.PositiveSmallIntegerField(verbose_name="Diplôme le plus élevé obtenu", choices=DIPLOME, blank=True, null=True)
    nom_representant = models.CharField(verbose_name="Nom", max_length=70, blank=True, null=True)
    prenom_representant = models.CharField(verbose_name="Prénom", max_length=35, blank=True, null=True)
    adresse_1_representant = models.CharField(verbose_name="Adresse", max_length=100, blank=True, null=True)
    adresse_2_representant = models.CharField(verbose_name="Complément d'adresse", max_length=100, blank=True, null=True)
    code_postal_representant = models.CharField(verbose_name="Code postal", max_length=5, blank=True, null=True)
    ville_representant = models.CharField(max_length=60, blank=True, null=True)
    date_maj = models.DateTimeField(default=datetime.datetime.now())

    def get_contrat_courant(self):
        """
        Cette méthode retourne le contrats courant de l'alternant
        """
        if self.contrats.filter(contrat_courant=True).exists():
            return self.contrats.filter(contrat_courant=True)[0]
        else:
            return None

    def __str__(self):
        return "%s %s" % (self.nom, self.prenom)


class Entreprise(models.Model):

    TYPE_EMPLOYEUR = (
        (11, "Entreprise inscrite au répertoire des métiers ou au registre des entreprises pour l’Alsace-Moselle"),
        (12, "Entreprise inscrite uniquement au registre du commerce et des sociétés"),
        (13, "Entreprises dont les salariés relèvent de la mutualité sociale agricole"),
        (14, "Profession libérale"),
        (15, "Association"),
        (16, "Autre employeur privé"),
        (21, "Service de l’Etat (administrations centrales et leurs services déconcentrés de la fonction publique d’Etat)"),
        (22, "Commune"),
        (23, "Département"),
        (24, "Région"),
        (25, "Etablissement public hospitalier"),
        (26, "Etablissement public local d’enseignement"),
        (27, "Etablissement public administratif de l’Etat"),
        (28, "Etablissement public administratif local (y compris établissement public de coopération intercommunale EPCI)"),
        (29, "Autre employeur public"),
    )

    SECTEUR_EMPLOYEUR = (
        (1, "Privé"),
        (2, "Public"),
    )

    EMPLOYEUR_SPECIFIQUE = (
        (1, "Entreprise de travail temporaire"),
        (2, "Groupement d’employeurs"),
        (3, "Employeur saisonnier"),
        (4, "Apprentissage familial : l’employeur est un ascendant de l’apprenti"),
        (0, "Aucun de ces cas"),
    )

    id = models.AutoField(primary_key=True)
    raison_sociale = models.CharField(max_length=70, blank=True, null=True)
    numero_SIRET = models.CharField(max_length=14, blank=True, null=True)
    adresse_1 = models.CharField(max_length=100, blank=True, null=True)
    adresse_2 = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=5, blank=True, null=True)
    ville = models.CharField(max_length=70, blank=True, null=True)
    type_employeur = models.PositiveSmallIntegerField(choices=TYPE_EMPLOYEUR, blank=True, null=True)
    secteur_employeur = models.PositiveSmallIntegerField(choices=SECTEUR_EMPLOYEUR, default=1)
    employeur_specifique = models.PositiveSmallIntegerField(choices=EMPLOYEUR_SPECIFIQUE, default=0)
    code_APE = models.CharField(max_length=5, blank=True, null=True)
    effectif_entreprise = models.PositiveSmallIntegerField(blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    telecopie = models.CharField(max_length=15, blank=True, null=True)
    courriel = models.CharField(max_length=40, blank=True, null=True)
    code_convention_collective = models.CharField(max_length=4, blank=True, null=True, help_text="Saisissez le code de la convention collective (4 chiffres). Si la convention collective n'est pas encore entrée en vigueur saisissez 9998. S'il n'y a aucune convention collective, saisissez 9999.")
    libelle_convention_collective = models.CharField(max_length=200, blank=True, null=True, help_text="Cette donnée est obligatoire. Si le code de convention existe, elle sera renseignée automatiquement.")
    adhesion_regime_assurance_chomage = models.BooleanField(default=False, help_text="Cochez cette case si l'employeur appartient au secteur public et si l'apprenti adhère au régime spécifique d'assurance chômage.")
    date_maj = models.DateTimeField(default=datetime.datetime.now())
    date_maj_contacts = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return "%s" % (self.raison_sociale)


class Personnel(models.Model):

    CIVILITE = (
        (1, "Madame"),
        (2, "Monsieur"),
    )

    ROLE = (
        (1, "Dirigeant"),
        (2, "Maître d'apprentissage")
    )

    id = models.AutoField(primary_key=True)
    entreprise = models.ForeignKey(Entreprise,on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE)
    civilite = models.CharField(max_length=12,choices=CIVILITE)
    nom = models.CharField(max_length=70)
    prenom = models.CharField(max_length=35)
    courriel = models.CharField(max_length=40, blank=True)
    date_naissance = models.DateField()
    date_maj = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return "%s %s" % (self.nom, self.prenom)


class CFA(models.Model):
    numeroUAI = models.CharField(max_length=8,primary_key=True)
    nom = models.CharField(max_length=70)
    adresse_1 = models.CharField(max_length=100)
    adresse_2 = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=5)
    ville = models.CharField(max_length=60)

    def __str__(self):
        return self.nom


class Formation(models.Model):

    DIPLOME = (
        (10,"Doctorat"),
        (11,"Master professionnel/DESS/diplôme grande école"),
        (12,"Master recherche/DEA"),
        (19,"Autre diplôme ou titre de niveau bac+5 ou plus"),
        (21,"Master professionnel (M1+M2 ou seul M2)"),
        (22,"Master général (M1+M2 ou seul M2)"),
        (23,"Licence professionnelle"),
        (24,"Licence générale"),
        (29,"Autre diplôme ou titre de niveau bac +3 ou 4"),
        (31,"Brevet de Technicien Supérieur"),
        (32,"Diplôme Universitaire de technologie"),
        (39,"Autre diplôme ou titre de niveau bac+2"),
        (41,"Baccalauréat professionnel"),
        (42,"Baccalauréat général"),
        (43,"Baccalauréat technologique"),
        (49,"Autre diplôme ou titre de niveau bac"),
        (51,"CAP"),
        (52,"BEP"),
        (53,"Mention complémentaire"),
        (59,"Autre diplôme ou titre de niveau CAP/BEP"),
        (60,"Aucun diplôme ni titre professionnel"),
    )

    code_formation = models.AutoField(max_length=13, primary_key=True)
    cfa = models.ForeignKey(CFA, on_delete=models.CASCADE)
    intitule_formation = models.CharField(max_length=150,blank=True, null=True)
    ville = models.CharField(max_length=35,blank=True, null=True)
    specialite = models.CharField(max_length=50,blank=True, null=True)
    diplome = models.PositiveSmallIntegerField(choices=DIPLOME, blank=True, null=True)
    intitule_diplome = models.CharField(max_length=100,blank=True, null=True)
    numero_UAI = models.CharField(max_length=8,blank=True, null=True)
    an_1_du = models.DateField(blank=True, null=True)
    an_1_au = models.DateField(blank=True, null=True)
    heures_an_1 = models.PositiveSmallIntegerField(blank=True, null=True)
    an_2_du = models.DateField(blank=True, null=True)
    an_2_au = models.DateField(blank=True, null=True)
    heures_an_2 = models.PositiveSmallIntegerField(blank=True, null=True)
    an_3_du = models.DateField(blank=True, null=True)
    an_3_au = models.DateField(blank=True, null=True)
    heures_an_3 = models.PositiveSmallIntegerField(blank=True, null=True)
    niveau = models.PositiveSmallIntegerField(blank=True, null=True)
    nombre_annees = models.PositiveSmallIntegerField(blank=True, null=True)
    annee_remuneration_annee_diplome = models.PositiveSmallIntegerField(blank=True, null=True)
    inspection_pedagogique_competente = models.PositiveSmallIntegerField(blank=True, null=True)


    def __str__(self):
        return self.intitule_formation


class Contrat(models.Model):

    MODE_CONTRACTUEL = (
        (1,"dans le cadre d'un CDD"),
        (2,"dans le cadre d'un CDI"),
        (3,"entreprise de travail temporaire"),
        (4,"activités saisonnières à deux employeurs"),
    )

    TYPE_CONTRAT_AVENANT = (
        (11,"Premier contrat d’apprentissage de l’apprenti"),
        (21,"Renouvellement de contrat chez le même employeur"),
        (22,"Contrat avec un apprenti qui a terminé son précédent contrat auprès d’un autre employeur"),
        (23,"Contrat avec un apprenti dont le précédent contrat auprès d’un autre employeur a été rompu"),
        (31,"Modification de la situation juridique de l’employeur"),
        (32,"Changement d’employeur dans le cadre d’un contrat saisonnier"),
        (33,"Prolongation du contrat suite à un échec à l’examen de l’apprenti"),
        (34,"Prolongation du contrat suite à la reconnaissance de l’apprenti comme travailleur handicapé"),
        (35,"Modification du diplôme préparé par l’apprenti"),
        (36, "Autres changements : changement de maître d’apprentissage, de durée de travail hebdomadaire, etc ..."),
    )

    TYPE_DEROGATION = (
        (11,"Age de l’apprenti inférieur à 16 ans"),
        (12,"Age supérieur à 25 ans : cas spécifiques prévus dans le code du travail"),
        (21,"Réduction de la durée du contrat ou de la période d’apprentissage"),
        (22,"Allongement  de la durée du contrat ou de la période d’apprentissage"),
        (31,"Début de l’apprentissage hors période légale (plus de 3 mois avant ou après la date de début du cycle de formation)"),
        (40,"Troisième contrat pour une formation de même niveau"),
        (50,"Cumul de dérogations"),
        (60,"Autre dérogation"),
    )
    
    BASE = (
        (1,"SMIC"),
        (2,"SMC"),
    )

    id = models.AutoField(primary_key=True)
    alternant = models.ForeignKey(Alternant, on_delete=models.CASCADE, blank=True, null=True, related_name="contrats")
    mode_contractuel = models.PositiveSmallIntegerField(choices=MODE_CONTRACTUEL)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, blank=True, null=True)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    type_contrat_avenant = models.PositiveSmallIntegerField(choices=TYPE_CONTRAT_AVENANT, blank=True, null=True)
    date_inscription = models.DateField(blank=True, null=True)
    type_derogation = models.PositiveSmallIntegerField(verbose_name="Type de dérogation", choices=TYPE_DEROGATION, blank=True, null=True)
    numero_contrat_anterieur = models.CharField(max_length=8, blank=True, null=True)
    date_embauche = models.DateField(blank=True, null=True)
    date_debut_contrat = models.DateField(blank=True, null=True)
    date_effet_avenant = models.DateField(blank=True, null=True)
    date_fin_contrat = models.DateField(blank=True, null=True)
    duree_hebdomadaire_travail = models.DurationField(blank=True, null=True)
    risques_particuliers = models.BooleanField(default=False)
    numero_annee_debut_contrat = models.PositiveSmallIntegerField(blank=True, null=True)
    salaire_minimum_conventionnel = models.FloatField(blank=True, null=True)
    salaire_brut_mensuel = models.FloatField(blank=True, null=True)
    caisse_retraite_complementaire = models.CharField(max_length=35, blank=True, null=True)
    nourriture = models.FloatField(blank=True, null=True)
    logement = models.FloatField(blank=True, null=True)
    prime_panier = models.FloatField(blank=True, null=True)
    fait_a = models.CharField(max_length=60, blank=True, null=True)
    fait_le = models.DateField(blank=True, null=True)
    attestation_pieces = models.BooleanField(default=True)
    attestation_maitre_apprentissage = models.BooleanField(default=True)
    an_1_per_1_du = models.DateField(blank=True, null=True)
    an_1_per_1_au = models.DateField(blank=True, null=True)
    an_1_per_1_taux = models.FloatField(blank=True, null=True)
    an_1_per_1_base = models.CharField(max_length=4, choices=BASE, blank=True, null=True)
    an_1_per_2_du = models.DateField(blank=True, null=True)
    an_1_per_2_au = models.DateField(blank=True, null=True)
    an_1_per_2_taux = models.FloatField(blank=True, null=True)
    an_1_per_2_base = models.CharField(max_length=4, choices=BASE, blank=True, null=True)
    an_2_per_1_du = models.DateField(blank=True, null=True)
    an_2_per_1_au = models.DateField(blank=True, null=True)
    an_2_per_1_taux = models.FloatField(blank=True, null=True)
    an_2_per_1_base = models.CharField(max_length=4, choices=BASE, blank=True, null=True)
    an_2_per_2_du = models.DateField(blank=True, null=True)
    an_2_per_2_au = models.DateField(blank=True, null=True)
    an_2_per_2_taux = models.FloatField(blank=True, null=True)
    an_2_per_2_base = models.CharField(max_length=4, choices=BASE, blank=True, null=True)
    an_3_per_1_du = models.DateField(blank=True, null=True)
    an_3_per_1_au = models.DateField(blank=True, null=True)
    an_3_per_1_taux = models.FloatField(blank=True, null=True)
    an_3_per_1_base = models.CharField(max_length=4, choices=BASE, blank=True, null=True)
    an_3_per_2_du = models.DateField(blank=True, null=True)
    an_3_per_2_au = models.DateField(blank=True, null=True)
    an_3_per_2_taux = models.FloatField(blank=True, null=True)
    an_3_per_2_base = models.CharField(max_length=4, choices=BASE, blank=True, null=True)
    an_4_per_1_du = models.DateField(blank=True, null=True)
    an_4_per_1_au = models.DateField(blank=True, null=True)
    an_4_per_1_taux = models.FloatField(blank=True, null=True)
    an_4_per_1_base = models.CharField(max_length=4, choices=BASE, blank=True, null=True)
    an_4_per_2_du = models.DateField(blank=True, null=True)
    an_4_per_2_au = models.DateField(blank=True, null=True)
    an_4_per_2_taux = models.FloatField(blank=True, null=True)
    an_4_per_2_base = models.CharField(max_length=4, choices=BASE, blank=True, null=True)
    date_maj = models.DateTimeField(default=datetime.datetime.now())
    date_maj_mission = models.DateTimeField(blank=True, null=True)
    date_saisie_complete = models.DateTimeField(blank=True, null=True)
    date_generation_CERFA = models.DateTimeField(blank=True, null=True)
    date_exportation_CFA = models.DateTimeField(blank=True, null=True)
    nombre_annees = models.PositiveSmallIntegerField(blank=True, null=True)
    contrat_courant = models.BooleanField(default=True)

    def __str__(self):
        return "Contrat %i" % self.id


class SMIC (models.Model):
    id = models.AutoField(primary_key=True)
    du = models.DateField()
    au = models.DateField()
    montant = models.FloatField()

    def __str__(self):
        return "SMIC %i" % self.id


class Minima (models.Model):
    annee = models.PositiveSmallIntegerField()
    age_de = models.PositiveSmallIntegerField()
    age_a = models.PositiveSmallIntegerField()
    taux_minimum = models.FloatField()

    def __str__(self):
        return self.annee


class Parametre (models.Model):
    majoration_taux_public = models.FloatField()

    def __str__(self):
        return "Paramètre"


class Commune (models.Model):
    code_INSEE = models.CharField(max_length=5)
    code_postal = models.CharField(max_length=5)
    libelle = models.CharField(max_length=50)

    def __str__(self):
        return self.libelle


class NAF (models.Model):
    code = models.CharField(max_length=5)
    libelle = models.CharField(max_length=150)

    def __str__(self):
        return self.code


class ConventionCollective(models.Model):
    code = models.CharField(max_length=4)
    libelle = models.CharField(max_length=300)

    def __str__(self):
        return "%s" % (self.code)

