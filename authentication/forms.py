from django import forms
from django.contrib.auth.models import User
from .models import Profile, ROLE_CHOICES

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:
        model = Profile
        fields = ['role', 'telefono', 'departamento']
        labels = {
            'role': 'Rol',
            'telefono': 'Teléfono',
            'departamento': 'Departamento',
        }   