from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Voiture(models.Model):
    model = models.CharField(max_length=255)
    marque  = models.CharField(max_length=255)
    num_chassi = models.CharField(max_length=255)
    
class Annonce(models.Model):
    STATUTS = (("en attente", "en attente"), ("validé", "validé"), ("retiré","retiré"),)
    
    titre = models.CharField()
    description = models.TextField()
    status = models.CharField( max_length=255, choices= STATUTS, default=STATUTS[0])
    montant = models.IntegerField()
    voiture = models.ForeignKey(Voiture, on_delete = models.CASCADE, related_name="annonces")
    propriétaire = models.ForeignKey(User, on_delete = models.CASCADE, related_name="annonces")

class Photo(models.Model):
    iamge = models.ImageField(upload_to='/voitures')
    voiture = models.ForeignKey(Voiture, on_delete = models.CASCADE, related_name='images')