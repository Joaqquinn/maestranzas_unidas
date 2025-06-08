from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from authentication import models
from .models import HistorialPrecio, Pieza, MovimientoInventario, Lote, Categoria, Proveedor, Ubicacion
from .forms import MovimientoInventarioForm,LoteForm, HistorialPrecioForm, PiezaForm, UbicacionForm,CategoriaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .filters import PiezaFilter
from authentication.decorators import group_required  # ajusta el path según tu estructura
from django.db.models import Count



# Create your views here.   
@group_required('Administrador del Sistema')
def dashboard_admin(request):
    profile = request.user.profile
    piezas_stock_bajo = Pieza.objects.filter(cantidad__lte=models.F('stock_minimo')).count() # type: ignore
    stock_bajo = Pieza.objects.filter(cantidad__lte=models.F("stock_minimo")) # type: ignore
    ubicaciones_distintas = Pieza.objects.values('ubicacion').distinct().count()
    movimientos_totales = MovimientoInventario.objects.count()

    context = {
        'user': request.user,
        'profile': profile,
        'role_display': request.user.groups.first().name if request.user.groups.exists() else "Sin rol",
        'total_piezas': Pieza.objects.count(),
        'piezas_stock_bajo': piezas_stock_bajo,
        'stock_bajo': stock_bajo,
        'ubicaciones_distintas': ubicaciones_distintas,
        'movimientos_totales': movimientos_totales,
    }

    return render(request, 'inventario/admin.html', context)

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



@login_required
def listar_ubicaciones(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'ubicaciones/listar.html', {'ubicaciones': ubicaciones})

@login_required
def crear_ubicacion(request):
    form = UbicacionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_ubicaciones')
    return render(request, 'ubicaciones/form.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_ubicacion(request, pk):
    ubicacion = get_object_or_404(Ubicacion, pk=pk)
    form = UbicacionForm(request.POST or None, instance=ubicacion)
    if form.is_valid():
        form.save()
        return redirect('listar_ubicaciones')
    return render(request, 'inventario/form.html', {'form': form, 'accion': 'Editar'})


@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/listar.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_categorias')
    return render(request, 'categorias/form.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('listar_categorias')
    return render(request, 'categorias/form.html', {'form': form, 'accion': 'Editar'})



@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    # Verifica si hay piezas asociadas
    piezas_asociadas = categoria.pieza_set.count()  # relaciona con el modelo Pieza

    if request.method == 'POST':
        if piezas_asociadas > 0:
            messages.error(request, 'No se puede eliminar la categoría porque hay piezas asociadas.')
            return redirect('listar_categorias')
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('listar_categorias')

    return render(request, 'categorias/eliminar_confirmacion.html', {
        'categoria': categoria,
        'piezas_asociadas': piezas_asociadas
    })


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

def editar_pieza(request, pk):
    pieza = get_object_or_404(Pieza, pk=pk)
    if request.method == 'POST':
        form = PiezaForm(request.POST, request.FILES, instance=pieza)
        if form.is_valid():
            form.save()
            return redirect('pieza_detalle', pk=pieza.pk)
    else:
        form = PiezaForm(instance=pieza)
    return render(request, 'inventario/editar_pieza.html', {'form': form, 'pieza': pieza})

@group_required(['Administrador del Sistema', 'Gestor de Inventario'])
def registrar_pieza(request):
    if request.method == 'POST':
        form = PiezaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pieza registrada correctamente.')
            return redirect('listar_piezas')  # Asegúrate de tener esta vista o cámbiala
    else:
        form = PiezaForm()
    return render(request, 'inventario/registrar_pieza.html', {'form': form})