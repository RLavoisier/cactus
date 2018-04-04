from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Alternant(models.Model):

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
        ("01", "Ain"),
        ("02", "Aisne"),
        ("03", "Allier"),
        ("04", "Alpes-de-Haute-Provence"),
        ("05", "Hautes-Alpes"),
        ("06", "Alpes-Maritimes"),
        ("07", "Ardèche"),
        ("08", "Ardennes"),
        ("09", "Ariège"),
        ("10", "Aube"),
        ("11", "Aude"),
        ("12", "Aveyron"),
        ("13", "Bouches-du-Rhône"),
        ("14", "Calvados"),
        ("15", "Cantal"),
        ("16", "Charente"),
        ("17", "Charente-Maritime"),
        ("18", "Cher"),
        ("19", "Corrèze"),
        ("2A", "Corse-du-Sud"),
        ("2B", "Haute-Corse"),
        ("21", "Côte-d'Or"),
        ("22", "Côtes-d'Armor"),
        ("23", "Creuse"),
        ("24", "Dordogne"),
        ("25", "Doubs"),
        ("26", "Drôme"),
        ("27", "Eure"),
        ("28", "Eure-et-Loir"),
        ("29", "Finistère"),
        ("30", "Gard"),
        ("31", "Haute-Garonne"),
        ("32", "Gers"),
        ("33", "Gironde"),
        ("34", "Hérault"),
        ("35", "Ille-et-Vilaine"),
        ("36", "Indre"),
        ("37", "Indre-et-Loire"),
        ("38", "Isère"),
        ("39", "Jura"),
        ("40", "Landes"),
        ("41", "Loir-et-Cher"),
        ("42", "Loire"),
        ("43", "Haute-Loire"),
        ("44", "Loire-Atlantique"),
        ("45", "Loiret"),
        ("46", "Lot"),
        ("47", "Lot-et-Garonne"),
        ("48", "Lozère"),
        ("49", "Maine-et-Loire"),
        ("50", "Manche"),
        ("51", "Marne"),
        ("52", "Haute-Marne"),
        ("53", "Mayenne"),
        ("54", "Meurthe-et-Moselle"),
        ("55", "Meuse"),
        ("56", "Morbihan"),
        ("57", "Moselle"),
        ("58", "Nièvre"),
        ("59", "Nord"),
        ("60", "Oise"),
        ("61", "Orne"),
        ("62", "Pas-de-Calais"),
        ("63", "Puy-de-Dôme"),
        ("64", "Pyrénées-Atlantiques"),
        ("65", "Hautes-Pyrénées"),
        ("66", "Pyrénées-Orientales"),
        ("67", "Bas-Rhin"),
        ("68", "Haut-Rhin"),
        ("69", "Rhône"),
        ("70", "Haute-Saône"),
        ("71", "Saône-et-Loire"),
        ("72", "Sarthe"),
        ("73", "Savoie"),
        ("74", "Haute-Savoie"),
        ("75", "Paris"),
        ("76", "Seine-Maritime"),
        ("77", "Seine-et-Marne"),
        ("78", "Yvelines"),
        ("79", "Deux-Sèvres"),
        ("80", "Somme"),
        ("81", "Tarn"),
        ("82", "Tarn-et-Garonne"),
        ("83", "Var"),
        ("84", "Vaucluse"),
        ("85", "Vendée"),
        ("86", "Vienne"),
        ("87", "Haute-Vienne"),
        ("88", "Vosges"),
        ("89", "Yonne"),
        ("90", "Territoire de Belfort"),
        ("91", "Essonne"),
        ("92", "Hauts-de-Seine"),
        ("93", "Seine-Saint-Denis"),
        ("94", "Val-de-Marne"),
        ("95", "Val-d'Oise"),
        ("971", "Guadeloupe"),
        ("972", "Martinique"),
        ("973", "Guyane"),
        ("974", "La Réunion"),
        ("976", "Mayotte"),
        ("099", "Personnes nées l’étranger"),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    nom = models.CharField(max_length=70)
    prenom = models.CharField(max_length=35)
    sexe = models.CharField(max_length=1)
    date_naissance = models.DateField()
    numero_departement_naissance = models.CharField(max_length=3)
    commune_naissance = models.CharField(max_length=60, blank=True)
    adresse_1 = models.CharField(max_length=100)
    adresse_2 = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=5)
    ville = models.CharField(max_length=60)
    telephone = models.CharField(max_length=15)
    handicape = models.BooleanField(default=False)
    courriel = models.CharField(max_length=40, blank=True)
    nationalite = models.PositiveSmallIntegerField(choices=NATIONALITE)
    regime_social = models.PositiveSmallIntegerField(choices=REGIME_SOCIAL)
    situation_avant_contrat = models.PositiveSmallIntegerField(choices=SITUATION_AVANT_CONTRAT)
    dernier_diplome_prepare = models.PositiveSmallIntegerField(choices=DIPLOME)
    derniere_annee_suivie = models.PositiveSmallIntegerField(choices=DERNIERE_ANNEE_SUIVIE)
    intitule_dernier_diplome_prepare = models.CharField(max_length=100)
    diplome_le_plus_eleve = models.PositiveSmallIntegerField(choices=DIPLOME)
    nom_representant = models.CharField(max_length=70, blank=True)
    prenom_representant = models.CharField(max_length=35, blank=True)
    adresse_1_representant = models.CharField(max_length=100, blank=True)
    adresse_2_representant = models.CharField(max_length=100, blank=True)
    code_postal_representant = models.CharField(max_length=5, blank=True)
    ville_representant = models.CharField(max_length=60, blank=True)
    date_maj = models.DateTimeField()

    def __str__(self):
        return self.nom + " " + self.prenom


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
    raison_sociale = models.CharField(max_length=70)
    numero_SIRET = models.CharField(max_length=14)
    adresse_1 = models.CharField(max_length=100)
    adresse_2 = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=5)
    ville = models.CharField(max_length=70)
    type_employeur = models.PositiveSmallIntegerField(choices=TYPE_EMPLOYEUR)
    secteur_employeur = models.PositiveSmallIntegerField(choices=SECTEUR_EMPLOYEUR)
    employeur_specifique = models.PositiveSmallIntegerField(choices=EMPLOYEUR_SPECIFIQUE)
    codeAPE = models.CharField(max_length=5)
    effectif_entreprise = models.PositiveSmallIntegerField()
    telephone = models.CharField(max_length=15)
    telecopie = models.CharField(max_length=15, blank=True)
    courriel = models.CharField(max_length=40)
    code_convention_collective = models.CharField(max_length=4, blank=True)
    libelle_convention_collective = models.CharField(max_length=200, blank=True)
    adhesion_regime_assurance_chomage = models.BooleanField(default=False, blank=True)
    date_maj = models.DateTimeField(blank=True)
    date_maj_contacts = models.DateTimeField(blank=True)

    def __str__(self):
        return self.raison_sociale


class Personnel(models.Model):

    CIVILITE = (
        (1, "Madame"),
        (2, "Monsieur"),
    )

    id = models.AutoField(primary_key=True)
    entreprise = models.ForeignKey(Entreprise,on_delete=models.CASCADE)
    role = models.CharField(max_length=25)
    civilite = models.CharField(max_length=12)
    nom = models.CharField(max_length=70)
    prenom = models.CharField(max_length=35)
    courriel = models.CharField(max_length=40, blank=True)
    date_naissance = models.DateField()
    date_maj = models.DateTimeField()

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


    code_formation = models.AutoField(primary_key=True)
    cfa = models.ForeignKey(CFA,on_delete=models.CASCADE)
    intitule_formation = models.CharField(max_length=150)
    ville = models.CharField(max_length=35)
    specialite = models.CharField(max_length=50)
    diplome = models.PositiveSmallIntegerField(choices=DIPLOME)
    intitule_diplome = models.CharField(max_length=100)
    numero_UAI = models.CharField(max_length=8)
    an_1_du = models.DateField(blank=True)
    an_1_au = models.DateField(blank=True)
    heures_an_1 = models.PositiveSmallIntegerField()
    an_2_du = models.DateField(blank=True)
    an_2_au = models.DateField(blank=True)
    heures_an_2 = models.PositiveSmallIntegerField(blank=True)
    an_3_du = models.DateField(blank=True)
    an_3_au = models.DateField(blank=True)
    heures_an_3 = models.PositiveSmallIntegerField(blank=True)
    niveau = models.PositiveSmallIntegerField()
    nombre_annees = models.PositiveSmallIntegerField()
    annee_remuneration_annee_diplome = models.PositiveSmallIntegerField()
    inspection_pedagogique_competente = models.PositiveSmallIntegerField()
    clef_formation = models.CharField(max_length=10)


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
        (36,"Autres changements : changement de maître d’apprentissage, de durée de travail hebdomadaire, etc ..."),
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
    mode_contractuel = models.PositiveSmallIntegerField(choices=MODE_CONTRACTUEL)
    alternant = models.ForeignKey(Alternant, on_delete=models.CASCADE, blank=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, blank=True)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, blank=True)
    mission = models.TextField(blank=True)
    type_contrat_avenant = models.PositiveSmallIntegerField(choices=TYPE_CONTRAT_AVENANT)
    date_inscription = models.DateField(blank=True)
    type_derogation = models.PositiveSmallIntegerField(choices=TYPE_DEROGATION, blank=True)
    numero_contrat_anterieur = models.CharField(max_length=20, blank=True)
    date_embauche = models.DateField(blank=True)
    date_debut_contrat = models.DateField(blank=True)
    date_effet_avenant = models.DateField(blank=True)
    date_fin_contrat = models.DateField(blank=True)
    duree_hebdomadaire_travail = models.DurationField(blank=True)
    risques_particuliers = models.BooleanField(default=False)
    numero_annee_debut_contrat = models.PositiveSmallIntegerField(blank=True)
    salaire_minimum_conventionnel = models.FloatField(blank=True)
    salaire_brut_mensuel = models.FloatField(blank=True)
    caisse_retraite_complementaire = models.CharField(max_length=35, blank=True)
    nourriture = models.FloatField(blank=True)
    logement = models.FloatField(blank=True)
    prime_panier = models.FloatField(blank=True)
    fait_a = models.CharField(max_length=60, blank=True)
    fait_le = models.DateField(blank=True)
    attestation_pieces = models.BooleanField(default=False)
    attestation_maitre_apprentissage = models.BooleanField(default=False)
    an_1_per_1_du = models.DateField(blank=True)
    an_1_per_1_au = models.DateField(blank=True)
    an_1_per_1_taux = models.FloatField(blank=True)
    an_1_per_1_base = models.CharField(max_length=4, choices=BASE, blank=True)
    an_1_per_2_du = models.DateField(blank=True)
    an_1_per_2_au = models.DateField(blank=True)
    an_1_per_2_taux = models.FloatField(blank=True)
    an_1_per_2_base = models.CharField(max_length=4, choices=BASE, blank=True)
    an_2_per_1_du = models.DateField(blank=True)
    an_2_per_1_au = models.DateField(blank=True)
    an_2_per_1_taux = models.FloatField(blank=True)
    an_2_per_1_base = models.CharField(max_length=4, choices=BASE, blank=True)
    an_2_per_2_du = models.DateField(blank=True)
    an_2_per_2_au = models.DateField(blank=True, default=None)
    an_2_per_2_taux = models.FloatField(blank=True)
    an_2_per_2_base = models.CharField(max_length=4, choices=BASE, blank=True)
    an_3_per_1_du = models.DateField(blank=True)
    an_3_per_1_au = models.DateField(blank=True)
    an_3_per_1_taux = models.FloatField(blank=True)
    an_3_per_1_base = models.CharField(max_length=4, choices=BASE, blank=True)
    an_3_per_2_du = models.DateField(blank=True)
    an_3_per_2_au = models.DateField(blank=True)
    an_3_per_2_taux = models.FloatField(blank=True)
    an_3_per_2_base = models.CharField(max_length=4, choices=BASE, blank=True)
    an_4_per_1_du = models.DateField(blank=True)
    an_4_per_1_au = models.DateField(blank=True)
    an_4_per_1_taux = models.FloatField(blank=True)
    an_4_per_1_base = models.CharField(max_length=4, choices=BASE, blank=True)
    an_4_per_2_du = models.DateField(blank=True)
    an_4_per_2_au = models.DateField(blank=True)
    an_4_per_2_taux = models.FloatField(blank=True)
    an_4_per_2_base = models.CharField(max_length=4, choices=BASE, blank=True)
    date_maj = models.DateTimeField(blank=True)
    date_maj_mission = models.DateTimeField(blank=True)
    date_saisie_complete = models.DateTimeField(blank=True)
    date_generation_CERFA = models.DateTimeField(blank=True)
    date_exportation_CFA = models.DateTimeField(blank=True)
    cursus_abrege = models.BooleanField(default=False)
    nombre_annees = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.id


class SMIC (models.Model):
    id = models.AutoField(primary_key=True)
    du = models.DateField()
    au = models.DateField()
    montant = models.FloatField()

    def __str__(self):
        return self.id


class Minima (models.Model):
    annee = models.PositiveSmallIntegerField()
    age_de = models.PositiveSmallIntegerField()
    age_a = models.PositiveSmallIntegerField()
    taux_minimum = models.FloatField()

    def __str__(self):
        return self.annee


class Parametres (models.Model):
    majoration_taux_public = models.FloatField()

    def __str__(self):
        return "Paramètres"