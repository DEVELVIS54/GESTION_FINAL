from django.contrib import admin
from .models import  Profil,Categorie,Propriete,Favori,RendezVous
from django.db import models
admin.site.register( Profil)
admin.site.register( Categorie)
admin.site.register(Propriete)
admin.site.register(Favori)
admin.site.register( RendezVous)
# Register your models here.
