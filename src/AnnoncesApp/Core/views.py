from django.shortcuts import render

from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
# from django.views

from .forms import VoitureForm
# Create your views here.

def create_voiture(request,*args,**kwargs):
    template_name = 'core/ajouter_voiture.html'
    context = {}

    form = VoitureForm()
    context['form'] =form

    return render(request,template_name,context)
