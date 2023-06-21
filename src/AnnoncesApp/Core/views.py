from django.shortcuts import render
from django.views import View
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.core.files.images import ImageFile

from.models import PhotoVoiture

from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
# from django.views

from .forms import VoitureForm, PhotoForm
# Create your views here.

def create_voiture(request,*args,**kwargs):
    template_name = 'core/ajouter_voiture.html'
    context = {}

    form = VoitureForm()
    context['form'] =form

    return render(request,template_name,context)


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
                # buffer = BytesIO()
                # for chunk in image_file.chunks():
                #     buffer.write(chunk)

                # buffer.seek(0)

                # uploaded_image = InMemoryUploadedFile(
                #     buffer,
                #     'ImageField',  # Nom du champ de l'image
                #     image_file.name,  # Nom du fichier d'origine
                #     image_file.content_type,  # Type de contenu
                #     buffer.tell(),  # Taille du fichier
                #     None  # Charset (optionnel)
                # )
                image = PhotoVoiture.objects.create(voiture = voiture, photo = ImageFile(image_file))
                print(image.voiture)
            form = self.form_class()
            """return redirect('')"""
        return render(request, self.template_name, {'form': form})
