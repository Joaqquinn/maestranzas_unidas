from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Pieza, MovimientoInventario
from .forms import MovimientoInventarioForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.   

def home(request):
    return render(request, 'inventario/home.html')

class PiezaCreateView(CreateView):
    model = Pieza
    fields = ['nombre', 'descripcion', 'numero_serie', 'ubicacion','cantidad', 'stock_minimo']
    template_name = 'inventario/pieza_form.html'
    success_url = reverse_lazy('dashboard')  # o a 'piezas_list' si vas a listar luego

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