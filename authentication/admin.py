from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'

# Extender el UserAdmin para incluir ProfileInline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:  # Solo mostrar el perfil si el usuario ya existe
            return []
        return super().get_inline_instances(request, obj)

# Re-registrar el User con el nuevo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
