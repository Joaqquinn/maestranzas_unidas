from django import forms
from .models import MovimientoInventario, Pieza,Lote, HistorialPrecio


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['pieza', 'tipo', 'cantidad', 'observacion']

class PiezaForm(forms.ModelForm):

    class Meta:
        model = Pieza
        fields = [
            'nombre', 'descripcion', 'numero_serie', 'ubicacion', 
            'categoria', 'proveedores', 'cantidad', 'stock_minimo', 
            'requiere_vencimiento'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
       
                                                                                                                                                                                                                                                     
class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['pieza', 'codigo_lote', 'cantidad', 'fecha_vencimiento']

    def clean(self):
        cleaned_data = super().clean()
        pieza = cleaned_data.get("pieza")
        fecha_vencimiento = cleaned_data.get("fecha_vencimiento")

        if pieza and pieza.requiere_vencimiento and not fecha_vencimiento:
            raise forms.ValidationError("Esta pieza requiere una fecha de vencimiento.")
        
class HistorialPrecioForm(forms.ModelForm):
    class Meta:
        model = HistorialPrecio
        fields = ['pieza', 'precio', 'proveedor']