# Generated by Django 5.2.1 on 2025-06-01 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pieza',
            name='cantidad',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
