from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Pieza(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=1)
   
    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"
    
    def esta_en_stock_bajo(self):
        return self.cantidad <= self.stock_minimo

TIPO_MOVIMIENTO_CHOICES = [
    ('entrada', 'Entrada'),
    ('salida', 'Salida'),
]

class MovimientoInventario(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.pieza.nombre} ({self.cantidad})" # type: ignore