# Generated by Django 5.2.1 on 2025-06-08 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0011_alter_historialprecio_proveedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoLote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.lote')),
                ('movimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lotes_afectados', to='inventario.movimientoinventario')),
            ],
        ),
    ]
