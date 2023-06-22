from typing import Any
from django import forms
from django.forms.models import inlineformset_factory
from django.forms import formset_factory
from .models import Marque, Modele, Voiture, Annonce, PhotoVoiture

from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model

# Forumulaire des user

User = get_user_model()

class UserRegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','first_name','last_name','email','phone_1','phone_2','address']

class UserUpdateForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username','first_name','last_name','email','phone_1','phone_2','address']

# Formulaire des Marque


class MarqueForm(forms.ModelForm):
    class Meta:
        model = Marque
        fields = (
            "__all__"  # Inclure tous les champs du modèle Marque dans le formulaire
        )


# Forumulaire des Modele


class ModeleForm(forms.ModelForm):
    class Meta:
        model = Modele
        fields = (
            "__all__"  # Inclure tous les champs du modèle Modele dans le formulaire
        )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = PhotoVoiture
        fields = ["photo","voiture"]


# VoiturePhotoFormSet = formset_factory(PhotoForm, extra=1)

# Formulaire des Voiture


class VoitureForm(forms.ModelForm):
    # photos = VoiturePhotoFormSet()
    # photo = forms.ImageField(required=True, label='',widget=forms.ClearableFileInput(
    #     attrs={
    #         "multiple": True,
    #         "class": "form-control",
    #     }
    # ))

    class Meta:
        model = Voiture
        # fields = (
        #     "__all__"  # Inclure tous les champs du modèle Voiture dans le formulaire
        # )
        exclude = ("proprietaire",)

    def save(self,user, commit: bool = True) -> Any:
        form = self.cleaned_data
        voiture = Voiture.objects.create(proprietaire = user,**form)
        return voiture
            
             

# Formulaire des Annonce


class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        # fields = "__all__"  # Inclure tous les champs du modèle AnnonceForm dans le formulaire
        exclude = ("status",)

    def __init__(self, user=None, *args, **kwargs):
        super(AnnonceForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["voiture"].queryset = Voiture.objects.filter(proprietaire=user)


# Formulaires des ImageVoiture

ImageVoitureFormSet = inlineformset_factory(Voiture, PhotoVoiture, fields=("photo",))


class ImageVoitureForm(forms.ModelForm):
    class Meta:
        model = PhotoVoiture
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ImageVoitureForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs.update({"class": "form-control-file"})

VoitureFormSet = formset_factory(VoitureForm,extra=1)

class NewAnnonceForm(forms.ModelForm):
    voiture = VoitureForm()
    class Meta:
        model = Annonce
        # fields = "__all__"  # Inclure tous les champs du modèle AnnonceForm dans le formulaire
        exclude = ('voiture',"status")