from django.utils.html import format_html
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):


    phone_1 = models.CharField(max_length=20,blank=True,null=True)
    phone_2 = models.CharField(max_length=20,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    class Meta(AbstractUser.Meta):
        pass
    

class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.nom


class Modele(models.Model):
    TYPE = (('electrique','electrique'),('essence','essence'),('diesele','diesele'))
    nom = models.CharField(max_length=100, unique=True)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="models")
    type = models.CharField(max_length=20,choices=TYPE)
    def __str__(self) -> str:
        return self.nom


class Voiture(models.Model):

    
    annee = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    num_chassi = models.CharField(max_length=255)
    km_parcouru = models.IntegerField()
    model = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name="voitures")
    proprietaire = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="annonces"
    )
    
    @property
    def main_image(self):
        image = self.images.first()

        if image:
            if image.photo:
                return image.photo.url
            return

    def __str__(self) -> str:
        return f"{self.model.marque} {self.model} ({self.annee})"


class Annonce(models.Model):
    STATUTS = (
        ("en attente", "en attente"),
        ("validé", "validé"),
        ("retiré", "retiré"),
    )

    titre = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=STATUTS, default='en attente')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    voiture = models.ForeignKey(
        Voiture, on_delete=models.CASCADE, related_name="annonces"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class PhotoVoiture(models.Model):
    photo = models.ImageField(upload_to="voitures/")
    voiture = models.ForeignKey(
        Voiture, on_delete=models.CASCADE, related_name="images"
    )

    def photo_preview(self):
        if self.photo:
            return format_html(
                f"<img src='{self.photo.url}' width='400px' heigth='400px' class='rounded float-right' />"
            )

        return None

    def __str__(self):
        return f"Image de {self.voiture.modele.marque} {self.voiture.model} ({self.voiture.annee})"
