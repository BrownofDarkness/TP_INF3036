from django.contrib import admin
from .models import Voiture, Annonce, PhotoVoiture, Marque, Modele
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.

User = get_user_model()


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_1','phone_2','address')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email','first_name','last_name', 'phone_1','phone_2','address', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'phone_1','phone_2','address', 'is_staff')

    search_fields = ('username', 'first_name', 'last_name', 'email', 'address')


admin.site.register(User, MyUserAdmin)

class ModeleInlineAdmin(admin.TabularInline):
    model = Modele
    extra = 0
    

class MarqueInlineAdmin(admin.TabularInline):
    model = Marque
    extra = 0
    

@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ("id", "nom")
    search_fields = ("nom",)
    inlines = [ModeleInlineAdmin]


@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ("id", "nom",'marque',"type")
    search_fields = ("nom",'marque__nom',)


class PhotoVoitureInline(admin.TabularInline):
    model = PhotoVoiture
    extra = 0

class AnnonceInline(admin.TabularInline):
    model = Annonce
    extra = 0

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "prix_voiture", "annee","km_parcouru", "proprietaire")
    search_fields = ("model__nom","model__marque__nom", "annee", "prix_voiture")
    list_filter = ("annee", "model", "prix_voiture")

    inlines= [PhotoVoitureInline,AnnonceInline]


@admin.register(PhotoVoiture)
class PhotoVoiture(admin.ModelAdmin):
    list_display = ("id","voiture", "photo_preview")

    readonly_fields = ["photo_preview"]


@admin.action(description="Valide annonce")
def valider_annonce(modeladmin, request, queryset):
    queryset.update(status="validé")

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "titre",
        "prix",
        "voiture",
        "description",
        "status",
        "prix",
        "date_creation",
    )
    search_fields = ("titre", "status", "prix")

    actions = [valider_annonce]

    


