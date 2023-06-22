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
    username = forms.CharField(label="", widget=forms.TextInput(
            attrs={
                "placeholder": "username"
            }
        ))
        
    first_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            "placeholder": "first_name"
        }
    ))
    
    last_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            "placeholder": "last_name"
        }
    ))
    
    email = forms.CharField(label="", widget=forms.EmailInput(
        attrs={
            "placeholder": "example@gmail.com"
        }
    ))
    
    address = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            "placeholder": "your address"
        }
    ))
    
    phone_1 = forms.CharField(label="phone_1", widget=forms.NumberInput(
        attrs={
            "placeholder": "your first number"
        }
    ))
    phone_2 = forms.CharField(label="phone_2", widget=forms.NumberInput(
        attrs={
            "placeholder": "your second number"
        }
    ))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={
            "placeholder": "password"
        }
    ))
    
    password2 = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={
            "placeholder": "confirm password"
        }
    ))
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username','first_name','last_name','email','phone_1','phone_2','address','password1','password2']

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
    
    # annee = forms.CharField(label="", widget=forms.NumberInput(
    #         attrs={
    #             "placeholder": "annee de fabrication"
    #         }
    #     ))
        
    # prix = forms.CharField(label="", widget=forms.NumberInput(
    #     attrs={
    #         "placeholder": "prix_voiture"
    #     }
    # ))
    
    # description = forms.CharField(label="", widget=forms.Textarea(
    #     attrs={
    #         "placeholder": "description_voiture"
    #     }
    # ))
    
    # num_chassi = forms.CharField(label="", widget=forms.TextInput(
    #     attrs={
    #         "placeholder": "numero chassi"
    #     }
    # ))
    
    # km_parcouru = forms.CharField(label="", widget=forms.NumberInput(
    #     attrs={
    #         "placeholder": "Km parcouru"
    #     }
    # ))
    
    # model = forms.ChoiceField(label="",choices=[(m.id, m.nom) for m in Modele.objects.all()] , widget=forms.Select(
    #     attrs={
    #         "name": "model"
    #     }
    # ))

    class Meta:
        model = Voiture
        fields = (
            "__all__"  # Inclure tous les champs du modèle Voiture dans le formulaire
        )
        exclude = ("proprietaire",)

            
             

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
        
    # prix = forms.CharField(label="", widget=forms.NumberInput(
    #     attrs={
    #         "placeholder": "prix_annonce"
    #     }
    # ))
    
    # description = forms.CharField(label="", widget=forms.Textarea(
    #     attrs={
    #         "placeholder": "description_annonce"
    #     }
    # ))
    
    # titre = forms.ChoiceField(label="",widget=forms.TextInput(
    #     attrs={
    #         "placeholder": "Titre"
    #     }
    # ))
    voiture = VoitureForm()
    class Meta:
        model = Annonce
        # fields = "__all__"  # Inclure tous les champs du modèle AnnonceForm dans le formulaire
        exclude = ('voiture',"status")