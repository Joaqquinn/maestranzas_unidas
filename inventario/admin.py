from django.contrib import admin
from .models import Pieza

# Register your models here.

@admin.register(Pieza)
class PiezaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_serie', 'ubicacion', 'cantidad')
    search_fields = ('nombre', 'numero_serie')
    list_filter = ('ubicacion',)
