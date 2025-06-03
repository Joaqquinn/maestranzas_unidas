from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import HistorialPrecio, Pieza, MovimientoInventario
from .forms import MovimientoInventarioForm,LoteForm, HistorialPrecioForm, PiezaConPrecioForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.   

def home(request):
    return render(request, 'inventario/home.html')

class PiezaCreateView(CreateView):
    model = Pieza
    form_class = PiezaConPrecioForm
    template_name = 'inventario/pieza_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Crear historial de precio automáticamente
        HistorialPrecio.objects.create(
            pieza=self.object,
            precio=form.cleaned_data['precio']
        )

        return response

@login_required
def listar_piezas(request):
    piezas = Pieza.objects.all()
    return render(request, 'inventario/listar_piezas.html', {'piezas': piezas})


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
