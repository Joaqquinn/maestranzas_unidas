from email.headerregistry import Group
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.models import Group

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

     


class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    role = forms.ChoiceField(label="Rol del usuario")  # ✅ Declaración explícita

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Asigna dinámicamente los grupos disponibles como choices
        self.fields['role'].choices = [(g.name, g.name) for g in Group.objects.all()]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # ✅ Asignación al grupo seleccionado
            grupo = Group.objects.get(name=self.cleaned_data['role'])
            user.groups.add(grupo)
        return user


