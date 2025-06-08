from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

ROLES = [
    'Administrador del Sistema',
    'Gestor de Inventario',
    'Comprador',
    'Almacén',
    'Jefe de Producción',
    'Auditor de Inventario',
    'Gerente de Proyectos',
    'Usuario Final',
]

class Command(BaseCommand):
    help = 'Crea los grupos de roles necesarios para el sistema'

    def handle(self, *args, **kwargs):
        for rol in ROLES:
            group, created = Group.objects.get_or_create(name=rol)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo creado: {rol}'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo ya existe: {rol}'))
