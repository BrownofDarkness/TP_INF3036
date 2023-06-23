from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    
    path("dashboard/",DashbordHome.as_view(),name="dashboard_home"),
    
    path("annonces/",AnnoncesListView.as_view(),name="annonces"),
    path("annonces/<int:pk>/",AnnoncesDetailView.as_view(),name="annonce_details"),
    path("annonces/<int:pk>/delete",DropAnnonceView.as_view(),name="delete_annonce"),
    path("voiture/<int:pk>/delete",DropVoitureView.as_view(),name="delete_voiture"),
    path("annonces/<int:pk>/update",MdAnnonceView.as_view(),name="update_annonce"),
    path("remove_annonce/<int:pk>",RemoveAnnonceView.as_view(),name="remove_voiture"),
    path("voiture/<int:pk>/update",MdVoitureView.as_view(),name="update_voiture"),
    path("new_annonce/",NewAnnonceView2.as_view(),name="new_annonce"),
    path("other_annonce/",OtherAnnonceView.as_view(),name="other_annonce"),
    
    re_path(r"ajouter_voiture/?", CreateVoiture.as_view(), name="ajouter_voiture"),
    re_path(r"nouvelle_annonce/?",NewAnnonceView.as_view(),name="nouvelle_annonce"),

    re_path(r"register/?",RegisterUserView.as_view(),name="register"),
    re_path(r"login/?",LoginView.as_view(),name="login"),
    re_path(r"logout/?",LogoutView.as_view(),name="logout")
    
]
