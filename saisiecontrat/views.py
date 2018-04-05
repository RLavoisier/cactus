# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from saisiecontrat.forms import CreationContratForm, CreationEntrepriseForm
from saisiecontrat.models import Contrat

def creationcontrat(request):

    if len(request.POST) > 0:

        form=CreationContratForm(request.POST)
        if form.is_valid():
            contrat=Contrat(request.POST['type_contrat_avenant'])
            contrat.save()
        else:
            return render(request, 'creationcontrat.html', {'form': form})
    else:
        form = CreationContratForm()
        return render(request, 'creationcontrat.html', {'form': form})

def create_entreprise(request):
    if request.method == "POST":
        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée
        form = CreationEntrepriseForm(request.POST)

        if form.is_valid():
            # Ici, on sauvegarde le formulaire, ce qui nous renvoi automatiauement
            # un nouvel objet entreprise
            entreprise = form.save()

            # Pour l'exemple, lorsque nous gererons les sessions et le contrat en cours
            # Nous pourrons venir rattacher la societé au contrat de cette manière :
            id_contrat = request.session.get("id_contrat")
            if id_contrat:
                # Récupération du contrat en base de donnée
                contrat = Contrat.objects.get(id=id_contrat)
                # Rattachement de l'entreprise
                contrat.entreprise = entreprise
                # Sauvegarde du contrat
                contrat.save()

            return redirect("creationentreprise")
        else:
            return render(request, "entreprise_form.html", {"form": form})
    else:
        form = CreationEntrepriseForm()
        return render(request, "entreprise_form.html", {"form": form})
