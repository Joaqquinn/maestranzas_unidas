import django_filters
from .models import Pieza, Categoria, Ubicacion
from django import forms

class PiezaFilter(django_filters.FilterSet):
    categoria = django_filters.ModelChoiceFilter(
        queryset=Categoria.objects.all(),
        empty_label="-- Selecciona una categoría --",
        label='Categoría',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_categoria'
        })
    )
    ubicacion = django_filters.ModelChoiceFilter(
        queryset=Ubicacion.objects.all(),
        empty_label="-- Selecciona una ubicación --", 
        label='Ubicación',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_ubicacion'
        })
    )

    class Meta:
        model = Pieza
        fields = ['categoria', 'ubicacion']