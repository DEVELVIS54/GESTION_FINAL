from django.db import models
from django.utils.timezone import now



from django.db import models
from django.db import models
from django.contrib.auth.models import User



# PROFIL

class Profil(models.Model):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('agent', 'Agent'),
        ('manager', 'Manager'),
        ('bailleur', 'Bailleur'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} ({self.role})"



# CAT

class Categorie(models.Model):
    type_categorie = models.CharField(max_length=100)

    def __str__(self):
        return self.type_categorie



# PRO

from django.db import models

class Propriete(models.Model):
    TYPE_CHOICES = [
        ('villa', 'Villa'),
        ('appartement', 'Appartement'),
        ('terrain', 'Terrain'),
        ('bureau', 'Bureau'),
    ]

    OPTION_CHOICES = [
        ('vente', 'Vente'),
        ('location', 'Location'),
    ]

    type_bien = models.CharField(max_length=50, choices=TYPE_CHOICES)
    option = models.CharField(max_length=10, choices=OPTION_CHOICES)
    adresse = models.CharField(max_length=255)
    surface = models.FloatField()
    nombre_piece = models.IntegerField()
    annee = models.IntegerField()
    prix = models.IntegerField()

    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    bailleur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proprietes_bailleur')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='proprietes_agent')

    # Nouveau champ image
    image = models.ImageField(upload_to='images_proprietes/', null=True, blank=True)

    def __str__(self):
        return f"{self.type_bien} - {self.prix} FCFA"




# FAV

class Favori(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)  # ← AJOUTE CECI
    class Meta:
        unique_together = ('client', 'propriete')

    def __str__(self):
        return f"{self.client.username}  {self.propriete}"



# RDV

class RendezVous(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE)

    lieu = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    date = models.DateField()
    heure = models.TimeField()

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"RDV {self.client.username} - {self.date}"