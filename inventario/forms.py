from django import forms
from .models import MovimientoInventario, Pieza,Lote, HistorialPrecio, Ubicacion, Categoria, Proveedor, Kit, KitItem

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
            'requiere_vencimiento', 'fecha_vencimiento', 'imagen'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Solo ocultar si ya existe el campo
        if 'fecha_vencimiento' in self.fields:
            if 'categoria' in self.data:
                cat_id = self.data.get('categoria')
                try:
                    from .models import Categoria
                    cat = Categoria.objects.get(id=cat_id)
                    if cat.nombre.lower() != 'consumible':
                        self.fields['fecha_vencimiento'].widget = forms.HiddenInput()
                except Categoria.DoesNotExist:
                    pass
            elif self.instance.pk:
                if self.instance.categoria and self.instance.categoria.nombre.lower() != 'consumible':
                    self.fields['fecha_vencimiento'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')

        if categoria and categoria.nombre.lower() == 'consumible' and not fecha_vencimiento:
            self.add_error('fecha_vencimiento', 'Este campo es obligatorio para piezas consumibles.')

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
       
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'condiciones_pago']
        widgets = {
            'condiciones_pago': forms.Textarea(attrs={'rows': 3}),
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


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ['nombre', 'descripcion']

# Formset para agregar piezas a un kit
KitItemFormSet = forms.inlineformset_factory(
    Kit, KitItem,
    fields=['pieza', 'cantidad'],
    extra=1,
    can_delete=True
)