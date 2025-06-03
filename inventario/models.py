from datetime import timedelta, timezone
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
    requiere_vencimiento = models.BooleanField(default=False)

    @property
    def cantidad_total(self):
        return sum(lote.cantidad for lote in self.lotes.all())

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
    

class Lote(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE, related_name='lotes')
    codigo_lote = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_emision = models.DateField(auto_now_add=True)

    def esta_vencido(self):
        if not self.pieza.requiere_vencimiento or not self.fecha_vencimiento:
            return False
        return timezone.now().date() > self.fecha_vencimiento

    def proximo_a_vencer(self):
        if not self.pieza.requiere_vencimiento or not self.fecha_vencimiento:
            return False
        return timezone.now().date() >= self.fecha_vencimiento - timedelta(days=7)

    def __str__(self):
        return f"Lote {self.codigo_lote} - {self.pieza.nombre}"
    

class HistorialPrecio(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE, related_name='precios')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.pieza.nombre} - ${self.precio} el {self.fecha}"