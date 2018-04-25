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

            alternant=contrat.alternant
            entreprise = contrat.entreprise
            maitreapprentissage = Personnel.objects.get(entreprise=entreprise,role=2)
            formation = contrat.formation

            #1 CIVILITE
            if alternant.sexe == "F":
                enr.append("Mme")
            else:
                enr.append("Mr")
            #2 NOM JEUNE
            enr.append(alternant.nom)
            #3 PRENOM JEUNE
            enr.append(alternant.prenom)
            #4 CIV REP LEG
            if alternant.civilite_representant == 1:
                enr.append("Mme")
            elif alternant.civilite_representant == 2:
                enr.append("Mr")
            else:
                pass
            #5 NOM REP LEG
            enr.append(alternant.nom_representant)
            #6 PRENOM LEG
            enr.append(alternant.prenom_representant)
            #7 AD1 JEUNE
            enr.append("%s %s" % (alternant.adresse_numero, alternant.adresse_voie))
            #8 AD2 JEUNE
            enr.append("")
            #9 CP JEUNE
            enr.append(alternant.code_postal)
            #10 VILLE JEUNE
            enr.append(alternant.ville)
            #11 DISTANCE
            enr.append("0")
            #12 TEL JEUNE
            enr.append(alternant.telephone)
            #13 DATE DE NAISSANCE
            enr.append(alternant.date_naissance.strftime('%d/%m/%Y'))
            #14 LIEU NAIS
            enr.append(alternant.commune_naissance)
            #15 DEP NAIS
            enr.append(alternant.numero_departement_naissance)
            #16 NATION
            if alternant.nationalite == 1:
                enr.append("FRANCAISE")
            elif alternant.nationalite == 2:
                enr.append("EUROPEENNE")
            elif alternant.nationalite == 3:
                enr.append("ETRANGERE HORS EUROPE")
            #17 GROUPE
            enr.append("")
            #18 CALENDRIER
            enr.append("")
            #19 SITUATION
            enr.append("")
            #20 DERNIER DIP
            enr.append(alternant.dernier_diplome_prepare)
            #21 METIER
            enr.append("")
            #22 ORIGINE
            if alternant.situation_avant_contrat == 10:
                enr.append("0117")
            elif alternant.situation_avant_contrat == 9:
                enr.append("0113")
            elif alternant.situation_avant_contrat == 8:
                enr.append("0111")
            elif alternant.situation_avant_contrat == 7:
                enr.append("0110")
            elif alternant.situation_avant_contrat == 6:
                enr.append("0117")
            elif alternant.situation_avant_contrat == 5:
                enr.append("5901")
            elif alternant.situation_avant_contrat == 4:
                enr.append("0999")
            elif alternant.situation_avant_contrat == 3:

                if alternant.derniere_annee_suivie == 11 or alternant.derniere_annee_suivie == 12:
                    annee = 1
                elif alternant.derniere_annee_suivie == 21 or alternant.derniere_annee_suivie == 22:
                    annee = 2
                elif alternant.derniere_annee_suivie == 31 or alternant.derniere_annee_suivie == 32:
                    annee = 3
                elif alternant.derniere_annee_suivie == 1:
                    if alternant.dernier_diplome_prepare == 39:
                        annee = 2
                    elif alternant.dernier_diplome_prepare == 32:
                        annee = 2
                    elif alternant.dernier_diplome_prepare == 31:
                        annee = 2
                    elif alternant.dernier_diplome_prepare == 29:
                        annee = 3
                    elif alternant.dernier_diplome_prepare == 24:
                        annee = 3
                    elif alternant.dernier_diplome_prepare == 23:
                        annee = 1
                    elif alternant.dernier_diplome_prepare == 22:
                        annee = 2
                    elif alternant.dernier_diplome_prepare == 21:
                        annee = 2
                    elif alternant.dernier_diplome_prepare == 19:
                        annee = 2
                    elif alternant.dernier_diplome_prepare == 12:
                        annee = 2
                    elif alternant.dernier_diplome_prepare == 11:
                        annee = 2
                enr.append("%s%s" % (alternant.dernier_diplome_prepare,annee))
            elif alternant.situation_avant_contrat == 2:
                enr.append("0999")
            elif alternant.situation_avant_contrat == 1:
                if alternant.derniere_annee_suivie == 11 or alternant.derniere_annee_suivie == 12:
                    annee = 1
                elif alternant.derniere_annee_suivie == 21 or alternant.derniere_annee_suivie == 22:
                    annee = 2
                elif alternant.derniere_annee_suivie == 31 or alternant.derniere_annee_suivie == 32:
                    annee = 3
                elif alternant.derniere_annee_suivie == 1:
                    annee = 3

                enr.append("%s%s" % (alternant.dernier_diplome_prepare, annee))
            #23 QUAL
                enr.append("DP")
            #24 NUMERO CON --------------------------------------------------------------------------------A VOIR
                enr.append("")
            #25 DATE DEB CONTRAT
            enr.append(contrat.date_debut_contrat.strftime('%d/%m/%Y'))
            #26 DATE FIN CONT
            enr.append(contrat.date_fin_contrat.strftime('%d/%m/%Y'))
            #27 DATE ENRE
            enr.append(datetime.now().strftime('%d/%m/%Y'))
            #28 DUREE
            if contrat.nombre_annees is None:
                duree_an = formation.nombre_annees
            else:
                duree_an = contrat.nombre_annees
            enr.append(duree_an * 12)
            #29 ENT
            enr.append(entreprise.raison_sociale)
            #30 CIV REP
            enr.append("")
            #31 NOM REP
            enr.append("")
            #32 PRENOM REP
            enr.append("")
            #33 ADR 1 ENT
            enr.append("%s %s" % (entreprise.adresse_numero, entreprise.adresse_voie))
            #34 ADR2 ENT
            enr.append(entreprise.adresse_complement)
            #35 CP ENT
            enr.append(entreprise.code_postal)
            #36 VILLE ENT
            enr.append(entreprise.ville)
            #37 TEL ENT
            enr.append(entreprise.telephone)
            #38 FAX ENT
            enr.append(entreprise.telecopie)
            #39 NAF
            enr.append(entreprise.code_APE)
            #40 SIRET
            enr.append(entreprise.numero_SIRET)
            #41 NB SAL
            enr.append(entreprise.effectif_entreprise)
            #42 AFF ENT--------------------------------------------------------------------------------A VOIR
            enr.append("")
            #43 CIV MA
            if alternant.civilite_representant == 1:
                enr.append("Mme")
            elif alternant.civilite_representant == 2:
                enr.append("Mr")
            else:
                pass
            #44 NOM MA
            enr.append(maitreapprentissage.nom)
            #45 PRENOM MA
            enr.append(maitreapprentissage.prenom)
            #46 DATE RESIL
            enr.append("")
            #47 MOTIF RESIL
            enr.append("")
            #48 DATE ENTREE GRP--------------------------------------------------------------------------------A VOIR
            enr.append("")
            #49 DATE DEP CFA
            enr.append("")
            #50 NOM ETAB
            enr.append("")
            #51 CP ETAB
            enr.append("")
            #52 VILLE ETAB
            enr.append("")
            #53 ID EXT JEUNE
            enr.append("")
            #54 ID EXT CONTRAT
            enr.append("")
            #55 ID EXT ENT
            enr.append("")
            #56 ID EXT COMMUNE
            enr.append("")
            #57 ID EXT VILLE ENT
            enr.append("")
            #58 DATE DE NAISSANCE MA
            enr.append(maitreapprentissage.date_naissance.strftime('%d/%m/%Y'))
            #59 QUALIFICATION MA
            enr.append("")
            #60 TELEPHONE 1 MA
            enr.append("")
            #61 TELEPHONE 2 MA
            enr.append("")
            #62 FAX MA
            enr.append("")
            #63 EMAIL MA
            enr.append("")
            #64 DATE DEPART MA
            enr.append("")
            #65 AUTRE ADR APP ADRESSE 1
            enr.append("")
            #66 AUTRE ADR APP ADRESSE 2
            enr.append("")
            #67 AUTRE ADR APP CP
            enr.append("")
            #68 AUTRE ADR APP VILLE
            enr.append("")
            #69 AUTRE ADR APP TEL 1
            enr.append("")
            #70 AUTRE ADR APP TEL 2
            enr.append("")
            #71 EMAIL APPRENANT
            enr.append(alternant.user.email)
            #72 INE APPRENANT
            enr.append("")
            #73 TEL 2 ENTREPRISE
            enr.append("")
            #74 EMAIL 2 ENTREPRISE
            enr.append("")
            #75 SITE WEB ENTREPRISE
            enr.append("")
            #76 DUMMY
            enr.append("")

            c.writerow(enr)
