# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from datetime import datetime

from django.views.generic import ListView

from saisiecontrat.forms import LoginForm, CreationContratForm, CreationEntrepriseForm, CreationAlternantForm, InformationContratForm, InformationMissionForm
from saisiecontrat.forms import CreationContratForm, CreationEntrepriseForm
from saisiecontrat.models import Contrat, Formation


def creationcontrat(request):

    if len(request.POST) > 0:

        form=CreationContratForm(request.POST)
        if form.is_valid():

            contrat=Contrat(type_contrat_avenant=Contrat(request.POST['type_contrat_avenant']),
                            mode_contractuel=Contrat(request.POST['mode_contractuel']),
                            numero_contrat_anterieur=Contrat(request.POST['numero_contrat_anterieur']),

            )
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

            # Ici, on sauvegarde le formulaire, ce qui nous renvoie automatiauement
            # un nouvel objet entreprise

            entreprise = form.save()
            entreprise.secteur_employeur = int(form.data.get("type_employeur")[1])
            entreprise.save()

            # Pour l'exemple, lorsque nous gererons les sessions et le contrat en cours
            # Nous pourrons venir rattacher la societé au contrat de cette manière :
            #id_contrat = request.session.get("id_contrat")
            #if id_contrat:
            #    # Récupération du contrat en base de donnée
            #    contrat = Contrat.objects.get(id=id_contrat)
            #    # Rattachement de l'entreprise
            #    contrat.entreprise = entreprise
            #    # Sauvegarde du contrat
            #    contrat.save()

            #return redirect("creationentreprise")
            return render(request, "entreprise_form.html", {"form": form})
        else:
            return render(request, "entreprise_form.html", {"form": form})
    else:
        form = CreationEntrepriseForm()
        return render(request, "entreprise_form.html", {"form": form})

def create_alternant(request):

    if request.method == "POST":
        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée
        form = CreationAlternantForm(request.POST)

        if form.is_valid():

            # Ici, on sauvegarde le formulaire, ce qui nous renvoie automatiauement
            # un nouvel objet entreprise

            # commit = false n'enregistre pas en base
            alternant = form.save(commit=False)
            alternant.user = request.user
            alternant.save()

            #alternant.secteur_employeur = int(form.data.get("type_employeur")[1])
            #alternant.save()

            # Pour l'exemple, lorsque nous gererons les sessions et le contrat en cours
            # Nous pourrons venir rattacher la societé au contrat de cette manière :
            #id_contrat = request.session.get("id_contrat")
            #if id_contrat:
            #    # Récupération du contrat en base de donnée
            #    contrat = Contrat.objects.get(id=id_contrat)
            #    # Rattachement de l'entreprise
            #    contrat.entreprise = entreprise
            #    # Sauvegarde du contrat
            #    contrat.save()

            #return redirect("creationalternant")
            return render(request, "alternant_form.html", {"form": form})
        else:
            return render(request, "alternant_form.html", {"form": form})
    else:
        form = CreationAlternantForm()
        return render(request, "alternant_form.html", {"form": form})

def inform_contrat(request):

    if request.method == "POST":
        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée
        form = InformationContratForm(request.POST)

        if form.is_valid():

            # Ici, on sauvegarde le formulaire, ce qui nous renvoie automatiauement
            # un nouvel objet entreprise

            contrat = form.save()


            return render(request, "contrat_form.html", {"form": form})
        else:
            return render(request, "contrat_form.html", {"form": form})
    else:
        # Il faut que la date de naissance de l'alternant soit renseignée avant l'appel à ce formulaire

        form = InformationContratForm()

        return render(request, "contrat_form.html", {"form": form})

def inform_mission(request):

    if request.method == "POST":
        # On créé le formulaire en lui passant le contenu du post
        # Comme c'est un formulaire modèle, cela prépare également un objet de base de donnée

        form = InformationMissionForm(request.POST)

        if form.has_changed():

            if form.is_valid():

                # Ici, on sauvegarde le formulaire, ce qui nous renvoie automatiauement
                # un nouvel objet entreprise

                contrat = form.save()


                return render(request, "mission_form.html", {"form": form})
            else:
                return render(request, "mission_form.html", {"form": form})
    else:

        form = InformationMissionForm()
        return render(request, "mission_form.html", {"form": form})


class liste_formation(ListView):
    queryset = Formation.objects.order_by("specialite")
    template_name = "formations_list.html"
    context_object_name = "formations"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        specialites = Formation.objects.order_by("specialite").values_list("specialite", flat=True).distinct()
        context["specialites"] = ["Toutes"] + list(specialites)
        context["request"] = self.request

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        specialite_filter = self.request.GET.get("specialite")

        if specialite_filter and specialite_filter != "Toutes":
            queryset = queryset.filter(specialite=self.request.GET.get("specialite"))

        return queryset