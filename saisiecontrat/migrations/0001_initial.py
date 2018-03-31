# Generated by Django 2.0.3 on 2018-03-28 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alternant',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nom', models.CharField(max_length=70)),
                ('prenom', models.CharField(max_length=35)),
                ('sexe', models.CharField(max_length=1)),
                ('datenaissance', models.DateField()),
                ('numerodepartementnaissance', models.CharField(max_length=3)),
                ('codeINSEEcommuneNaissance', models.CharField(max_length=5)),
                ('adresse1', models.CharField(max_length=100)),
                ('adresse2', models.CharField(max_length=100)),
                ('codepostal', models.CharField(max_length=5)),
                ('ville', models.CharField(max_length=60)),
                ('telephone', models.CharField(max_length=15)),
                ('handicape', models.BooleanField(default=False)),
                ('courriel', models.CharField(max_length=40)),
                ('nationalite', models.PositiveSmallIntegerField(choices=[(1, 'Française'), (2, 'Union Européenne'), (3, 'Etranger hors Union Européenne')])),
                ('regimesocial', models.PositiveSmallIntegerField(choices=[(1, 'MSA'), (2, 'URSSAF')])),
                ('situationavantcontrat', models.PositiveSmallIntegerField(choices=[(1, 'Scolaire (hors DIMA)'), (2, 'Dispositif d’initiation aux métiers en alternance (DIMA) ou autre classe préparatoire à l’apprentissage (CLIPA, CPA...)'), (3, 'Etudiant'), (4, 'Contrat d’apprentissage'), (5, 'Contrat de professionnalisation'), (6, 'Contrat aidé'), (7, 'Stagiaire de la formation professionnelle'), (8, 'Salarié'), (9, 'Personne à la recherche d’un emploi (inscrite ou non au Pôle Emploi)'), (10, 'Inactif')])),
                ('dernierdiplomeprepare', models.PositiveSmallIntegerField(choices=[(10, 'Doctorat'), (11, 'Master professionnel/DESS/diplôme grande école'), (12, 'Master recherche/DEA'), (19, 'Autre diplôme ou titre de niveau bac+5 ou plus'), (21, 'Master professionnel (M1+M2 ou seul M2)'), (22, 'Master général (M1+M2 ou seul M2)'), (23, 'Licence professionnelle'), (24, 'Licence générale'), (29, 'Autre diplôme ou titre de niveau bac +3 ou 4'), (31, 'Brevet de Technicien Supérieur'), (32, 'Diplôme Universitaire de technologie'), (39, 'Autre diplôme ou titre de niveau bac+2'), (41, 'Baccalauréat professionnel'), (42, 'Baccalauréat général'), (43, 'Baccalauréat technologique'), (49, 'Autre diplôme ou titre de niveau bac'), (51, 'CAP'), (52, 'BEP'), (53, 'Mention complémentaire'), (59, 'Autre diplôme ou titre de niveau CAP/BEP'), (60, 'Aucun diplôme ni titre professionnel')])),
                ('derniereanneesuivie', models.PositiveSmallIntegerField(choices=[(1, 'l’apprenti a suivi la dernière année du cycle de formation et a obtenu le diplôme ou titre'), (11, 'l’apprenti a suivi la 1ère année du cycle et l’a validée (examens réussis mais année non diplômante)'), (12, 'l’apprenti a suivi la 1ère année du cycle mais ne l’a pas validée (échec aux examens, interruption ou abandon de formation)'), (21, 'l’apprenti a suivi la 2è année du cycle et l’a validée (examens réussis mais année non diplômante)'), (22, 'l’apprenti a suivi la 2è année du cycle mais ne l’a pas validée (échec aux examens, interruption ou abandon de formation)'), (31, 'l’apprenti a suivi la 3è année du cycle et l’a validée (examens réussis mais année non diplômante, cycle adapté)'), (32, 'l’apprenti a suivi la 3è année du cycle mais ne l’a pas validée (échec aux examens, interruption ou abandon de formation)'), (40, 'l’apprenti a achevé le 1er cycle de l’enseignement secondaire (collège)'), (41, 'l’apprenti a interrompu ses études en classe de 3è'), (42, 'l’apprenti a interrompu ses études en classe de 4è')])),
                ('intituledernierdiplomeprepare', models.CharField(max_length=100)),
                ('diplomelepluseleve', models.PositiveSmallIntegerField(choices=[(10, 'Doctorat'), (11, 'Master professionnel/DESS/diplôme grande école'), (12, 'Master recherche/DEA'), (19, 'Autre diplôme ou titre de niveau bac+5 ou plus'), (21, 'Master professionnel (M1+M2 ou seul M2)'), (22, 'Master général (M1+M2 ou seul M2)'), (23, 'Licence professionnelle'), (24, 'Licence générale'), (29, 'Autre diplôme ou titre de niveau bac +3 ou 4'), (31, 'Brevet de Technicien Supérieur'), (32, 'Diplôme Universitaire de technologie'), (39, 'Autre diplôme ou titre de niveau bac+2'), (41, 'Baccalauréat professionnel'), (42, 'Baccalauréat général'), (43, 'Baccalauréat technologique'), (49, 'Autre diplôme ou titre de niveau bac'), (51, 'CAP'), (52, 'BEP'), (53, 'Mention complémentaire'), (59, 'Autre diplôme ou titre de niveau CAP/BEP'), (60, 'Aucun diplôme ni titre professionnel')])),
                ('nomrepresentant', models.CharField(max_length=70)),
                ('prenomrepresentant', models.CharField(max_length=35)),
                ('adresse1representant', models.CharField(max_length=100)),
                ('adresse2representant', models.CharField(max_length=100)),
                ('codepostalrepresentant', models.CharField(max_length=5)),
                ('villerepresentant', models.CharField(max_length=60)),
                ('datemaj', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CFA',
            fields=[
                ('numeroUAI', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=70)),
                ('adresse1', models.CharField(max_length=100)),
                ('adresse2', models.CharField(max_length=100)),
                ('codepostal', models.CharField(max_length=5)),
                ('ville', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('modecontractuel', models.PositiveSmallIntegerField(choices=[(1, "dans le cade d'un CDD"), (2, "dans le cade d'un CDI"), (3, 'entreprise de travail temporaire'), (4, 'activités saisonnières à deux employeurs')])),
                ('mission', models.TextField()),
                ('typecontratavenant', models.PositiveSmallIntegerField(choices=[(11, 'Premier contrat d’apprentissage de l’apprenti'), (21, 'Renouvellement de contrat chez le même employeur'), (22, 'Contrat avec un apprenti qui a terminé son précédent contrat auprès d’un autre employeur'), (23, 'Contrat avec un apprenti dont le précédent contrat auprès d’un autre employeur a été rompu'), (31, 'Modification de la situation juridique de l’employeur'), (32, 'Changement d’employeur dans le cadre d’un contrat saisonnier'), (33, 'Prolongation du contrat suite à un échec à l’examen de l’apprenti'), (34, 'Prolongation du contrat suite à la reconnaissance de l’apprenti comme travailleur handicapé'), (35, 'Modification du diplôme préparé par l’apprenti'), (36, 'Autres changements : changement de maître d’apprentissage, de durée de travail hebdomadaire, etc ...')])),
                ('dateinscription', models.DateField()),
                ('typederogation', models.PositiveSmallIntegerField(choices=[(11, 'Age de l’apprenti inférieur à 16 ans'), (12, 'Age supérieur à 25 ans : cas spécifiques prévus dans le code du travail'), (21, 'Réduction de la durée du contrat ou de la période d’apprentissage'), (22, 'Allongement  de la durée du contrat ou de la période d’apprentissage'), (31, 'Début de l’apprentissage hors période légale (plus de 3 mois avant ou après la date de début du cycle de formation)'), (40, 'Troisième contrat pour une formation de même niveau'), (50, 'Cumul de dérogations'), (60, 'Autre dérogation')])),
                ('numerocontratanterieur', models.CharField(max_length=20)),
                ('dateembauche', models.DateField()),
                ('datedebutcontrat', models.DateField()),
                ('dateeffetavenant', models.DateField()),
                ('datefincontrat', models.DateField()),
                ('dureehebdomadairetravail', models.DurationField()),
                ('risquesparticuliers', models.BooleanField(default=False)),
                ('numeroanneedebutcontrat', models.PositiveSmallIntegerField()),
                ('salaireminimumconventionnel', models.FloatField()),
                ('salairebrutmensuel', models.FloatField()),
                ('caisseretraitecomplementaire', models.CharField(max_length=35)),
                ('nourriture', models.FloatField()),
                ('logement', models.FloatField()),
                ('primepanier', models.FloatField()),
                ('faita', models.CharField(max_length=60)),
                ('faitle', models.DateField()),
                ('attestationpieces', models.BooleanField(default=False)),
                ('attestationmaitreapprentissage', models.BooleanField(default=False)),
                ('datemaj', models.DateTimeField()),
                ('detamajmission', models.DateTimeField()),
                ('datesaisiecomplete', models.DateTimeField()),
                ('dategenerationCERFA', models.DateTimeField()),
                ('dateexportationCFA', models.DateTimeField()),
                ('alternant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saisiecontrat.Alternant')),
            ],
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('raisonsociale', models.CharField(max_length=70)),
                ('numeroSIRET', models.CharField(max_length=14)),
                ('adresse1', models.CharField(max_length=100)),
                ('adresse2', models.CharField(max_length=100)),
                ('codepostal', models.CharField(max_length=5)),
                ('ville', models.CharField(max_length=70)),
                ('typeemployeur', models.PositiveSmallIntegerField(choices=[(11, 'Entreprise inscrite au répertoire des métiers ou au registre des entreprises pour l’Alsace-Moselle'), (12, 'Entreprise inscrite uniquement au registre du commerce et des sociétés'), (13, 'Entreprises dont les salariés relèvent de la mutualité sociale agricole'), (14, 'Profession libérale'), (15, 'Association'), (16, 'Autre employeur privé'), (21, 'Service de l’Etat (administrations centrales et leurs services déconcentrés de la fonction publique d’Etat)'), (22, 'Commune'), (23, 'Département'), (24, 'Région'), (25, 'Etablissement public hospitalier'), (26, 'Etablissement public local d’enseignement'), (27, 'Etablissement public administratif de l’Etat'), (28, 'Etablissement public administratif local (y compris établissement public de coopération intercommunale EPCI)'), (29, 'Autre employeur public')])),
                ('secteuremployeur', models.PositiveSmallIntegerField(choices=[(1, 'Privé'), (2, 'Public')])),
                ('employeurspecifique', models.PositiveSmallIntegerField(choices=[(1, 'Entreprise de travail temporaire'), (2, 'Groupement d’employeurs'), (3, 'Employeur saisonnier'), (4, 'Apprentissage familial : l’employeur est un ascendant de l’apprenti'), (0, 'Aucun de ces cas')])),
                ('codeAPE', models.CharField(max_length=5)),
                ('effectifentreprise', models.PositiveSmallIntegerField()),
                ('telephone', models.CharField(max_length=15)),
                ('telecopie', models.CharField(max_length=15)),
                ('courriel', models.CharField(max_length=40)),
                ('codeconventioncollective', models.CharField(max_length=4)),
                ('libelleconventioncollective', models.CharField(max_length=200)),
                ('adhesionregimeassurancechomage', models.BooleanField(default=False)),
                ('datemaj', models.DateTimeField()),
                ('datemajcontacts', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('numeroUAI', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('diplome', models.PositiveSmallIntegerField(choices=[(10, 'Doctorat'), (11, 'Master professionnel/DESS/diplôme grande école'), (12, 'Master recherche/DEA'), (19, 'Autre diplôme ou titre de niveau bac+5 ou plus'), (21, 'Master professionnel (M1+M2 ou seul M2)'), (22, 'Master général (M1+M2 ou seul M2)'), (23, 'Licence professionnelle'), (24, 'Licence générale'), (29, 'Autre diplôme ou titre de niveau bac +3 ou 4'), (31, 'Brevet de Technicien Supérieur'), (32, 'Diplôme Universitaire de technologie'), (39, 'Autre diplôme ou titre de niveau bac+2'), (41, 'Baccalauréat professionnel'), (42, 'Baccalauréat général'), (43, 'Baccalauréat technologique'), (49, 'Autre diplôme ou titre de niveau bac'), (51, 'CAP'), (52, 'BEP'), (53, 'Mention complémentaire'), (59, 'Autre diplôme ou titre de niveau CAP/BEP'), (60, 'Aucun diplôme ni titre professionnel')])),
                ('intitule', models.CharField(max_length=100)),
                ('codediplome', models.CharField(max_length=8)),
                ('an1du', models.DateField()),
                ('an1au', models.DateField()),
                ('heuresan1', models.PositiveSmallIntegerField()),
                ('an2du', models.DateField()),
                ('an2au', models.DateField()),
                ('heuresan2', models.PositiveSmallIntegerField()),
                ('an3du', models.DateField()),
                ('an3au', models.DateField()),
                ('heuresan3', models.PositiveSmallIntegerField()),
                ('niveau', models.PositiveSmallIntegerField()),
                ('duree', models.PositiveSmallIntegerField()),
                ('inpectionpedagogiquecompetente', models.PositiveSmallIntegerField()),
                ('cfa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saisiecontrat.CFA')),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=25)),
                ('civilite', models.CharField(max_length=12)),
                ('nom', models.CharField(max_length=70)),
                ('prenom', models.CharField(max_length=35)),
                ('datenaissance', models.DateField()),
                ('datemaj', models.DateTimeField()),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saisiecontrat.Entreprise')),
            ],
        ),
        migrations.CreateModel(
            name='Remuneration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('annee', models.PositiveSmallIntegerField()),
                ('anper1du', models.DateField()),
                ('anper1au', models.DateField()),
                ('anper1taux', models.FloatField()),
                ('anper1base', models.CharField(choices=[(1, 'SMIC'), (2, 'SMC')], max_length=4)),
                ('anper2du', models.DateField()),
                ('anper2au', models.DateField()),
                ('anper2taux', models.FloatField()),
                ('anper2base', models.CharField(choices=[(1, 'SMIC'), (2, 'SMC')], max_length=4)),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saisiecontrat.Contrat')),
            ],
        ),
        migrations.CreateModel(
            name='SMIC',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('du', models.DateField()),
                ('au', models.DateField()),
                ('montant', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='contrat',
            name='entreprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saisiecontrat.Entreprise'),
        ),
        migrations.AddField(
            model_name='contrat',
            name='formation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saisiecontrat.Formation'),
        ),
    ]
