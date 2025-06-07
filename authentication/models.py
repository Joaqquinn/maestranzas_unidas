from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

ROLE_CHOICES = [
    ('admin_sistema', 'Administrador del Sistema'),
    ('gestor_inventario', 'Gestor de Inventario'), 
    ('comprador', 'Comprador'),
    ('almacen_logistica', 'Almacén/Logística'),
    ('jefe_produccion', 'Jefe de Producción'),
    ('auditor_inventario', 'Auditor de Inventario'),
    ('gerente_proyectos', 'Gerente de Proyectos'),
    ('usuario_final', 'Usuario Final'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telefono = models.CharField(max_length=20, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.role})"
    


