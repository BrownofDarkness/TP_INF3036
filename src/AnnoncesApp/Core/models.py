from django.utils.html import format_html
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.nom


class Modele(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="models")
    def __str__(self) -> str:
        return self.nom


class Voiture(models.Model):
    annee = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    num_chassi = models.CharField(max_length=255)
    model = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name="voitures")
    proprietaire = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="annonces"
    )

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
    status = models.CharField(max_length=255, choices=STATUTS, default=STATUTS[0])
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
        if self.image:
            return format_html(
                f"<img src='{self.photo.url}' width='400px' heigth='400px' class='rounded float-right' />"
            )

        return None

    def __str__(self):
        return f"Image de {self.voiture.modele.marque} {self.voiture.modele} ({self.voiture.annee})"
