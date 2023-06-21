from django.urls import path, re_path

from .views import *

urlpatterns = [
    re_path(r"ajouter_voiture?", CreateVoiture.as_view(), name="ajouter_voiture")
]
