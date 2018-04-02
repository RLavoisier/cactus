# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from datetime import datetime
from saisiecontrat.forms import LoginForm,CreationContratForm
from saisiecontrat.models import Contrat

def creationcontrat(request):

    if len(request.POST) > 0:

        form=CreationContratForm(request.POST)
        if form.is_valid():
            contrat=Contrat(request.POST['typecontratavenant'])
            contrat.save()
        else:
            return render(request,'creationcontrat.html',{'form':form})
    else:
        form = CreationContratForm()
        return render(request,'creationcontrat.html',{'form':form})

