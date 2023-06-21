from django.contrib import admin
from .models import Voiture, Annonce, ImageVoiture, Marque, Modele

# Register your models here.


@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ("id", "nom")
    search_fields = ("nom",)


@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "marque")
    search_fields = ("nom", "marque__nom")


@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "prix", "annee", "description", "proprietaire")
    search_fields = ("model__nom", "model__marque__nom", "annee", "prix")
    list_filter = ("annee", "model", "prix")


@admin.register(ImageVoiture)
class ImageVoiture(admin.ModelAdmin):
    list_display = ("id", "image", "photo_preview")

    readonly_fields = ["photo_preview"]


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "titre",
        "prix",
        "voiture",
        "description",
        "status",
        "prix",
        "date_creation",
    )
    search_fields = ("title", "status")
