import random
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from django.core.files.images import ImageFile

from .models import PhotoVoiture

from django.core.files.images import ImageFile
from django.contrib.auth import login,login,authenticate
# from django.views

from .forms import VoitureForm,NewAnnonceForm, AnnonceForm,UserRegisterForm,UserUpdateForm
from .models import Voiture,PhotoVoiture,Annonce
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

class RegisterUserView(View):

    template_name = "core/register.html"
    context = {}

    def get(self,request,*args,**kwargs):
        form =  UserRegisterForm()
        self.context['form'] = form
        return render(request, self.template_name,self.context)
        

    def post(self,request,*args,**kwargs):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            # redirect("login")
        self.context['form'] = form
        
        return render(request, self.template_name,self.context)

class LoginView(View):

    template_name="core/login.html"
    context = {}

    def get(self,request,*args,**kwargs):
        print("Athenticated",request.user.is_authenticated)
        if request.user.is_authenticated:
            return redirect("home")
        form =  AuthenticationForm()
        self.context['form'] = form
        return render(request, self.template_name,self.context)
        

    def post(self,request,*args,**kwargs):
        form = AuthenticationForm(request.POST)
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)

        if user is not None:
            login(request,user)
            return redirect("register")
        else:
            self.context['form'] = form
        
        return render(request, self.template_name,self.context)
    
class LogoutView(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):
        login(request)

        return redirect("home")
        

class CreateVoiture(LoginRequiredMixin,View):
    template_name = 'core/ajouter_voiture.html'
    login_url = 'login'
    redirect_url = 'ajouter_voiture'
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


class AnnonceOtherView(View):
    template_name = "core/other_annonce.html"
    form_class = AnnonceForm
    context = {}
    
    def get(self,request, *args, **kwargs):
        form = self.form_class()
        self.context["form"] = form
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            form = self.form_class()
            """return redirect('')"""
        self.context["form"] = form
        return render(request, self.template_name, self.context)
    

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
        annee = request.GET.get('annee',None)
        prix =  request.GET.get('prix',None)
        marque = requests.GET.get('marque',None)
        model = request.GET.get('model',None)
        titre = request.GET.get('titre',None)

        if titre:
            queries = queries.filter(titre=titre)
        if annee:
            queries = queries.filter(voiture__annee=annee)
        if prix:
            queries = queries.filter(prix=prix)
        if marque:
            queries = queries.filter(voiture__model__marque__nom__icontains=marque)
        if model:
            queries = queries.filter(voiture__model__nom__icontains=model)
        
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
    
