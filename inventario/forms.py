from django import forms
from .models import MovimientoInventario, Pieza


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['pieza', 'tipo', 'cantidad', 'observacion']

class PiezaForm(forms.ModelForm):
    class Meta:
        model = Pieza
        fields = ['nombre', 'descripcion', 'numero_serie', 'ubicacion', 'cantidad', 'stock_minimo']