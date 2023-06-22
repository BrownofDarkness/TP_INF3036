import random
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from django.core.files.images import ImageFile

from.models import PhotoVoiture

from django.core.files.images import ImageFile
# from django.views

from .forms import VoitureForm,NewAnnonceForm
from .models import Voiture,PhotoVoiture,Annonce


# Create your views here.


class CreateVoiture(View):
    template_name = 'core/ajouter_voiture.html'
    form_class = VoitureForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            voiture = form.save()
            images = request.FILES.getlist('photos')
            for image_file in images:
                image = PhotoVoiture.objects.create(voiture = voiture, photo = ImageFile(image_file))
                print(image.voiture)
            form = self.form_class()
            """return redirect('')"""
        return render(request, self.template_name, {'form': form})



class NewAnnonceView(View):
    context = {}
    template_name = 'core/nouvelle_annonce.html'
    form_class = NewAnnonceForm
    
    def get(self,request,*args,**kwargs):

        form = self.form_class()

        self.context['form'] = form

        return render(request,self.template_name,self.context)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)
        voiture_form = VoitureForm(request.POST)
        if form.is_valid():
            voiture_form.is_valid()
            # print(form.cleaned_data['voiture'])
            # voiture_data = validated_annonce.pop('voiture',None)

            voiture = voiture_form.save(user = request.user)

            if voiture:
                images = request.FILES.getlist('photos')
                for image_file in images:
                    image = PhotoVoiture.objects.create(voiture = voiture, photo = ImageFile(image_file))
                    print(image.voiture)
            annonce = form.save(commit=False)
            annonce.voiture = voiture
            annonce.save()
        self.context['form'] = self.form_class()
        
        return render(request,self.template_name,self.context)


class HomeView(View):
    template_name = "core/home.html"
    
    def get (self, request, *args, **kwargs):
        queries = list(Annonce.objects.filter(status = 'validé'))
        random.shuffle(queries)
        queries = queries[:4]
        context = {
            'annonces': queries,
        }
        return render(request, self.template_name, context)
    
class AnnoncesListView(View):
    template_name = "core/annonces.html"
    
    def get (self, request, *args, **kwargs):
        queries = Annonce.objects.filter(status = 'validé')
        context = {
            'annonces': queries,
        }
        return render(request, self.template_name, context)
    
class AnnoncesDetailView(View):
    template_name = "core/annonces.html"
    
    def get (self, request, pk, *args, **kwargs):
        annonce = Annonce.objects.get(pk = pk)
        same_category = Annonce.objects.valid().filter(Q(voiture__model=annonce.voiture.model) | Q(voiture__model__marque=annonce.voiture.model.marque))
        same_category = same_category.exclude(pk=annonce.pk)[:10]
        context = {
            'annonce': annonce,
            'same_category': same_category,
        }
        return render(request, self.template_name, context)
    
class ValidateAnnonceView(View):
    
    def post (self, request, pk, *args, **kwargs):
        annonce = Annonce.objects.get(pk = pk)
        if annonce:
            annonce.status = "validé"
            annonce.save()
            return redirect("dashboard")
    
class DropAnnonceView(View):
    template_name = "core/refused.html"
    
    def get (self, request, pk, *args, **kwargs):
        annonce = Annonce.objects.get(pk = pk)
        context = {
            'annonce': annonce,
        }
        return render(request, self.template_name, context)
    
    def post (self, request, pk, *args, **kwargs):
        annonce = Annonce.objects.get(pk = pk)
        if annonce:
            annonce.delete()
            return redirect("home")
        
        context = {
            'annonce': annonce,
        }
        return render(request, self.template_name, context)
