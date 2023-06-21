from django.shortcuts import render
from django.views import View
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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
    def get(self,request,*args,**kwargs):

        form = NewAnnonceForm()

        self.context['form'] = form

        return render(request,self.template_name,self.context)
    
    def post(self,request,*args,**kwargs):

        form = NewAnnonceForm(request.POST)
        voiture_form = VoitureForm(request.POST)
        if form.is_valid():
            voiture_form.is_valid()
            # print(form.cleaned_data['voiture'])
            # voiture_data = validated_annonce.pop('voiture',None)

            voiture = voiture_form.save()

            if voiture:
                images = request.FILES.getlist('photos')
                for image_file in images:
                    image = PhotoVoiture.objects.create(voiture = voiture, photo = ImageFile(image_file))
                    print(image.voiture)
            annonce = form.save(commit=False)
            annonce.voiture = voiture
            annonce.save()
        self.context['form'] = form
        
        return render(request,self.template_name,self.context)
