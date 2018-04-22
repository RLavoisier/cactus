import csv

from django.core.management import BaseCommand

from saisiecontrat.models import User, Alternant, Contrat, Entreprise, Personnel

class Command(BaseCommand):

    def handle(self, *args, **options):

        c = csv.writer(open("export.csv", "w"), delimiter="|")

        c.writerow(["",""])

        c.writerow(["CIVILITE",
                    "NOM JEUNE",
                    "PRENOM JEUNE",
                    "CIV REP LEG",
                    "NOM REP LEG",
                    "PRENOM LEG",
                    "AD1 JEUNE",
                    "AD2 JEUNE",
                    "CP JEUNE",
                    "VILLE JEUNE",
                    "DISTANCE",
                    "TEL JEUNE",
                    "DATE DE NAISSANCE",
                    "LIEU NAIS",
                    "DEP NAIS",
                    "NATION",
                    "GROUPE",
                    "CALENDRIER",
                    "SITUATION",
                    "DERNIER DIP",
                    "METIER",
                    "ORIGINE",
                    "QUAL",
                    "NUMERO CON",
                    "DATE DEB CONTRAT",
                    "DATE FIN CONT",
                    "DATE ENRE",
                    "DUREE",
                    "ENT",
                    "CIV REP",
                    "NOM REP",
                    "PRENOM REP",
                    "ADR 1 ENT",
                    "ADR2 ENT",
                    "CP ENT",
                    "VILLE ENT",
                    "TEL ENT",
                    "FAX ENT",
                    "NAF",
                    "SIRET",
                    "NB SAL",
                    "AFF ENT",
                    "CIV MA",
                    "NOM MA",
                    "PRENOM MA",
                    "DATE RESIL",
                    "MOTIF RESIL",
                    "DATE ENTREE GRP",
                    "DATE DEP CFA",
                    "NOM ETAB",
                    "CP ETAB",
                    "VILLE ETAB",
                    "ID EXT JEUNE",
                    "ID EXT CONTRAT",
                    "ID EXT ENT",
                    "ID EXT COMMUNE",
                    "ID EXT VILLE ENT",
                    "DATE DE NAISSANCE MA",
                    "QUALIFICATION MA",
                    "TELEPHONE 1 MA",
                    "TELEPHONE 2 MA",
                    "FAX MA",
                    "EMAIL MA",
                    "DATE DEPART MA",
                    "AUTRE ADR APP ADRESSE 1",
                    "AUTRE ADR APP ADRESSE 2",
                    "AUTRE ADR APP CP",
                    "AUTRE ADR APP VILLE",
                    "AUTRE ADR APP TEL 1",
                    "AUTRE ADR APP TEL 2",
                    "EMAIL APPRENANT",
                    "INE APPRENANT",
                    "TEL 2 ENTREPRISE",
                    "EMAIL 2 ENTREPRISE",
                    "SITE WEB ENTREPRISE",
                    "DUMMY"])

        # get comme pour le filtre
        # Attention si plusieurs objets retournés => exception : multipleobjectreturn
        # si aucun exception DoesNotExist
        # On utilise un Try

        # Pour récupérer plusieurs objets spécifier un filter
        # contrats = Contrat.objects.filter()

        # RPour récupérer tout : all()

        contrats = Contrat.objects.all()

        # contrat = Contrat() crée l'objet sans save (si save on crée un nouvel objet donnée  si id=null)

        # Create créé l'objet + save en base
        # contrat = Contrat.objects.create(contrat_courant=True)

        for contrat in contrats:

            enr=[]

            alternant = Alternant.objects.get(alternant=contrat.alternant)
            entreprise = Alternant.objects.get(entreprise=contrat.entreprise)
            maitreapprentissage = Personnel.objects.get(entreprise=entreprise,role=2)
            formation = Alternant.objects.get(formation=contrat.formation)

            #1 CIVILITE
            if alternant.sexe == 1:
                enr.append("Mme")
            else:
                enr.append("Mr")
            #2 NOM JEUNE
            enr.append(alternant.nom)
            #3 PRENOM JEUNE
            enr.append(alternant.prenom)
            #4 CIV REP LEG
            if alternant.civilite_representant == "Madame":
                enr.append("Mme")
            elif alternant.civilite_representant == "Monsieur":
                enr.append("Mr")
            else:
                pass
            #5 NOM REP LEG
            enr.append(alternant.nom_representant)
            #6 PRENOM LEG
            enr.append(alternant.prenom_representant)
            #7 AD1 JEUNE

            #8 AD2 JEUNE

            #9 CP JEUNE

            #10 VILLE JEUNE

            #11 DISTANCE

            #12 TEL JEUNE

            #13 DATE DE NAISSANCE

            #14 LIEU NAIS

            #15 DEP NAIS

            #16 NATION

            #17 GROUPE

            #18 CALENDRIER

            #19 SITUATION

            #20 DERNIER DIP

            #21 METIER

            #22 ORIGINE

            #23 QUAL

            #24 NUMERO CON

            #25 DATE DEB CONTRAT

            #26 DATE FIN CONT

            #27 DATE ENRE

            #28 DUREE

            #29 ENT

            #30 CIV REP

            #31 NOM REP

            #32 PRENOM REP

            #33 ADR 1 ENT

            #34 ADR2 ENT

            #35 CP ENT

            #36 VILLE ENT

            #37 TEL ENT

            #38 FAX ENT

            #39 NAF

            #40 SIRET

            #41 NB SAL

            #42 AFF ENT

            #43 CIV MA

            #44 NOM MA

            #45 PRENOM MA

            #46 DATE RESIL

            #47 MOTIF RESIL

            #48 DATE ENTREE GRP

            #49 DATE DEP CFA

            #50 NOM ETAB

            #51 CP ETAB

            #52 VILLE ETAB

            #53 ID EXT JEUNE

            #54 ID EXT CONTRAT

            #55 ID EXT ENT

            #56 ID EXT COMMUNE

            #57 ID EXT VILLE ENT

            #58 DATE DE NAISSANCE MA

            #59 QUALIFICATION MA

            #60 TELEPHONE 1 MA

            #61 TELEPHONE 2 MA

            #62 FAX MA

            #63 EMAIL MA

            #64 DATE DEPART MA

            #65 AUTRE ADR APP ADRESSE 1

            #66 AUTRE ADR APP ADRESSE 2

            #67 AUTRE ADR APP CP

            #68 AUTRE ADR APP VILLE

            #69 AUTRE ADR APP TEL 1

            #70 AUTRE ADR APP TEL 2

            #71 EMAIL APPRENANT

            #72 INE APPRENANT

            #73 TEL 2 ENTREPRISE

            #74 EMAIL 2 ENTREPRISE

            #75 SITE WEB ENTREPRISE

            #76 DUMMY

            c.writerow(enr)