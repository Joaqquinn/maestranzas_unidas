from .models import MovimientoLote
from django.db import transaction
from django.core.exceptions import ValidationError

def descontar_lotes_para_pieza(pieza, cantidad_requerida, movimiento):
    lotes_disponibles = pieza.lotes.filter(cantidad__gt=0).order_by('fecha_vencimiento', 'fecha_emision')

    cantidad_restante = cantidad_requerida

    with transaction.atomic():
        for lote in lotes_disponibles:
            if cantidad_restante == 0:
                break

            cantidad_a_descontar = min(lote.cantidad, cantidad_restante)
            lote.cantidad -= cantidad_a_descontar
            lote.save()

            # Registrar trazabilidad
            MovimientoLote.objects.create(
                movimiento=movimiento,
                lote=lote,
                cantidad=cantidad_a_descontar
            )

            cantidad_restante -= cantidad_a_descontar

        if cantidad_restante > 0:
            raise ValidationError(f"No hay stock suficiente en los lotes para la pieza {pieza.nombre}.")
