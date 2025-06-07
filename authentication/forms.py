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


class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Crear perfil asociado
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
        return user