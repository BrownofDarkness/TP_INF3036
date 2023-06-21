from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r"ajouter_voiture?", views.create_voiture, name="ajouter_voiture")
]
