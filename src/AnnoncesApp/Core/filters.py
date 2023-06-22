import django_filters
from .models import Annonce


class AnnonceFilterSearch(django_filters.FilterSet):

    class Meta:
        model = Annonce
        fields = {'titre':['icontains'], 
                  'voiture__model__nom':['icontains'], 
                  'voiture__model__marque__nom':['icontains']
        }


class AnnonceFilter(django_filters.FilterSet):
    class Meta:
        model = Annonce
        fields = ['category', 'category__parent']