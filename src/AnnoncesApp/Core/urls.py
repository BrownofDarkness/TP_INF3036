from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    
    re_path(r"annonces/?",AnnoncesListView.as_view(),name="annonces"),
    re_path(r"annonces/<int:pk>/?",AnnoncesDetailView.as_view(),name="annonce_details"),
    
    re_path(r"ajouter_voiture/?", CreateVoiture.as_view(), name="ajouter_voiture"),
    re_path(r"nouvelle_annonce/?",NewAnnonceView.as_view(),name="new_annonce"),
    
]
