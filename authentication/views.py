from django.utils import timezone
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
from .decorators import group_required

from django.db.models import F 

# Login

def role_to_dashboard(group_name):
    return '/dashboard/'


@group_required('Administrador del Sistema')
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('home')  # Cambia esto según tu vista
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

            group = user.groups.first().name if user.groups.exists() else None # type: ignore
            return redirect(role_to_dashboard(group))  # todos van al mismo, pero puedes cambiar según el rol
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'authentication/login.html', {'form': form})

# Dashboard
@login_required
def dashboard_view(request):
    grupo = request.user.groups.first().name if request.user.groups.exists() else None
    return redirect(role_to_dashboard(grupo))

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')


def sin_permiso(request):
    return render(request, 'authentication/sin_permiso.html')