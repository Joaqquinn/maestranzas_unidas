from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import HistorialPrecio, Pieza, MovimientoInventario, Lote, Categoria, Proveedor, Ubicacion
from .forms import MovimientoInventarioForm,LoteForm, HistorialPrecioForm, PiezaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .filters import PiezaFilter


# Create your views here.   

def home(request):
    return render(request, 'inventario/home.html')

class PiezaCreateView(CreateView):
    model = Pieza
    form_class = PiezaForm
    template_name = 'inventario/registrar_pieza.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


def lista_piezas(request): # Cambiamos el nombre para reflejar 'Pieza'
    piezas_list = Pieza.objects.all() # Usamos el modelo Pieza
    categorias = Categoria.objects.all()
    ubicaciones = Ubicacion.objects.all()

    # Obtener los parámetros de filtrado de la URL (GET request)
    categoria_id = request.GET.get('categoria')
    ubicacion_id = request.GET.get('ubicacion')

    # Aplicar filtros si los parámetros están presentes
    if categoria_id:
        piezas_list = piezas_list.filter(categoria__id=categoria_id) # Filtra por el ID de la categoría de la Pieza

    if ubicacion_id:
        piezas_list = piezas_list.filter(ubicacion__id=ubicacion_id) # Filtra por el ID de la ubicación de la Pieza

    context = {
        'piezas': piezas_list, # Cambiamos 'productos' por 'piezas'
        'categorias': categorias,
        'ubicaciones': ubicaciones,
        'categoria_seleccionada': categoria_id,
        'ubicacion_seleccionada': ubicacion_id
    }
    return render(request, 'inventario/listar_piezas.html', context) # Ajusta el path a tu template


def pieza_detalle(request, pk):
    pieza = get_object_or_404(Pieza, pk=pk)
    return render(request, 'inventario/detalle_piezas.html', {'pieza': pieza})

@login_required
def registrar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.responsable = request.user

            pieza = movimiento.pieza
            if movimiento.tipo == 'entrada':
                pieza.cantidad += movimiento.cantidad
            elif movimiento.tipo == 'salida':
                if pieza.cantidad >= movimiento.cantidad:
                    pieza.cantidad -= movimiento.cantidad
                else:
                    messages.error(request, 'No hay suficiente stock para esa salida.')
                    return redirect('registrar_movimiento')

            pieza.save()
            movimiento.save()
            messages.success(request, 'Movimiento registrado correctamente.')
            return redirect('dashboard')
    else:
        form = MovimientoInventarioForm()

    return render(request, 'inventario/registrar_movimiento.html', {'form': form})

def registrar_lote(request):
    pieza_id = request.GET.get('pieza_id')
    pieza = get_object_or_404(Pieza, pk=pieza_id) if pieza_id else None

    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pieza_detalle', pk=form.cleaned_data['pieza'].id)
    else:
        form = LoteForm(initial={'pieza': pieza}) if pieza else LoteForm()

    return render(request, 'registrar_lote.html', {'form': form})


def registrar_precio(request):
    pieza_id = request.GET.get('pieza_id')
    pieza = Pieza.objects.filter(pk=pieza_id).first()

    if request.method == 'POST':
        form = HistorialPrecioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pieza_detalle', pk=form.cleaned_data['pieza'].id)
    else:
        form = HistorialPrecioForm(initial={'pieza': pieza}) if pieza else HistorialPrecioForm()

    return render(request, 'registrar_precio.html', {'form': form})




@login_required
def registrar_pieza(request):
    if request.method == 'POST':
        form = PiezaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pieza registrada correctamente.')
            return redirect('listar_piezas')  # Asegúrate de tener esta vista o cámbiala
    else:
        form = PiezaForm()
    return render(request, 'inventario/registrar_pieza.html', {'form': form})