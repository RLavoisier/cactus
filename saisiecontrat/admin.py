from django.contrib import admin
from .models import Alternant, Entreprise, Personnel, CFA, Formation, Contrat, SMIC, Minima, Parametre, Commune, NAF

# Register your models here.

admin.site.register(Alternant)
admin.site.register(Entreprise)
admin.site.register(Personnel)
admin.site.register(CFA)
admin.site.register(Formation)
admin.site.register(Contrat)
admin.site.register(SMIC)
admin.site.register(Minima)
admin.site.register(Parametre)
admin.site.register(Commune)
admin.site.register(NAF)