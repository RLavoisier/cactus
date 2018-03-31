from django.contrib import admin
from .models import Alternant, Entreprise,Personnel,CFA,Formation,Contrat,Remuneration,SMIC

# Register your models here.

admin.site.register(Alternant)
admin.site.register(Entreprise)
admin.site.register(Personnel)
admin.site.register(CFA)
admin.site.register(Formation)
admin.site.register(Contrat)
admin.site.register(Remuneration)
admin.site.register(SMIC)
