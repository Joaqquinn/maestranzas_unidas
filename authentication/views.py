from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from inventario.models import MovimientoInventario
from .forms import UsuarioForm, UsuarioRegistroForm
from django.contrib.auth.models import User
from inventario.models import Pieza 
from django.db import models
from django.contrib.auth.decorators import login_required
from authentication.decorators import role_required


# Login}

def role_to_dashboard(role):
    dashboards = {
        'admin_sistema': 'dashboard_admin',
        'gestor_inventario': 'dashboard_inventario',
        'comprador': 'dashboard_compras',
        'almacen_logistica': 'dashboard_almacen',
        'jefe_produccion': 'dashboard_produccion',
        'auditor_inventario': 'dashboard_auditor',
        'gerente_proyectos': 'dashboard_gerente',
        'usuario_final': 'dashboard_usuario',
    }
    return dashboards.get(role, 'sin_permiso')


@role_required(['admin_sistema'])
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('dashboard_admin')
    else:
        form = UsuarioRegistroForm()

    return render(request, 'authentication/registrar_usuario.html', {'form': form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # ← crea la sesión

            role = user.profile.role # type: ignore
            return redirect('dashboard')  # todos van al mismo, pero puedes cambiar según el rol
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'authentication/login.html', {'form': form})

# Dashboard
@login_required
def dashboard_view(request):
    role = request.user.profile.role
    return redirect(role_to_dashboard(role))

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

@login_required
def crear_usuario_view(request):
    if not request.user.profile.role == 'admin_sistema':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
          

            messages.success(request, f"Usuario '{username}' creado con éxito.")
            return redirect('crear_usuario')
    else:
        form = UsuarioForm()

    return render(request, 'authentication/crear_usuario.html', {'form': form})

@role_required(['admin_sistema'])
def dashboard_admin(request):
    return render(request, 'dashboards/admin.html')

@role_required(['gestor_inventario'])
def dashboard_inventario(request):
    return render(request, 'dashboards/inventario.html')

@role_required(['comprador'])
def dashboard_compras(request):
    return render(request, 'dashboards/compras.html')

@role_required(['almacen_logistica'])
def dashboard_almacen(request):
    return render(request, 'dashboards/almacen.html')

@role_required(['jefe_produccion'])
def dashboard_produccion(request):
    return render(request, 'dashboards/produccion.html')

@role_required(['auditor_inventario'])
def dashboard_auditor(request):
    return render(request, 'dashboards/auditor.html')

@role_required(['gerente_proyectos'])
def dashboard_gerente(request):
    return render(request, 'dashboards/gerente.html')

@role_required(['usuario_final'])
def dashboard_usuario(request):
    return render(request, 'dashboards/usuario.html')

def sin_permiso(request):
    return render(request, 'authentication/sin_permiso.html')