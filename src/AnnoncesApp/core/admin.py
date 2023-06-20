from django.contrib import admin
from .models import Voiture, Annonce, Photo

# Register your models here.


@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "marque")
    search_fields = ("model","marque")
    
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "photo_preview")

    readonly_fields = ["photo_preview"]
    
@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "status", "montant")
    search_fields = ("title", "status")