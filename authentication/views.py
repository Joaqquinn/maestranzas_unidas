from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UsuarioForm
from django.contrib.auth.models import User
from inventario.models import Pieza  
from django.db import models

# Login
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
    try:
        profile = request.user.profile
        piezas_stock_bajo = Pieza.objects.filter(cantidad__lte=models.F('stock_minimo')).count()
            
    except Profile.DoesNotExist:
        # Si el perfil no existe, desconectamos al usuario
        logout(request)
        messages.error(request, "Tu cuenta no tiene perfil asignado.")
        return redirect('login')

    context = {
        'user': request.user,
        'profile': profile,
        'role': profile.role,
        'role_display': profile.get_role_display(),
        'total_piezas': Pieza.objects.count(),
        'piezas_stock_bajo': piezas_stock_bajo,

    }
    return render(request, 'authentication/dashboard.html', context)
# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

# Vista opcional para crear usuarios si eres admin
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
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, f"Usuario '{username}' creado con éxito.")
            return redirect('crear_usuario')
    else:
        form = UsuarioForm()

    return render(request, 'authentication/crear_usuario.html', {'form': form})
