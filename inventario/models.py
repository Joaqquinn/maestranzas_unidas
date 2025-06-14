from datetime import timedelta, timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre


class Pieza(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)
    proveedores = models.ManyToManyField('Proveedor', blank=True)
    cantidad = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=1)
    requiere_vencimiento = models.BooleanField(default=False)
    fecha_vencimiento = models.DateField(null=True, blank=True)  # <- aquí

    imagen = models.ImageField(upload_to='imagenes_piezas/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"
    
    def es_consumible(self):
        return self.categoria.nombre.lower() == "Consumible" # type: ignore


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
        return timezone.now().date() >= self.fecha_vencimiento - timedelta(days=7) # type: ignore

    def __str__(self):
        return f"Lote {self.codigo_lote} - {self.pieza.nombre}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)
    condiciones_pago = models.TextField(blank=True)

    def __str__(self):
        return self.nombre 



class HistorialPrecio(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE, related_name='precios')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.pieza.nombre} - ${self.precio} el {self.fecha}"


class Kit(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    piezas = models.ManyToManyField(Pieza, through='KitItem')

    def __str__(self):
        return self.nombre

class KitItem(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kit.nombre} - {self.pieza.nombre} ({self.cantidad})"

class MovimientoLote(models.Model):
    movimiento = models.ForeignKey(MovimientoInventario, on_delete=models.CASCADE, related_name='lotes_afectados')
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movimiento} - Lote {self.lote.codigo_lote} ({self.cantidad})"