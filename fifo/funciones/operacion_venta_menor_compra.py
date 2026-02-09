import copy
from typing import Any

from constantes import COMISIONES, NUMERO

from .crear_operacion import crear_operacion
from .recalcular_movimiento import recalcular_movimiento


def operacion_venta_menor_compra(
    compra: dict[str, Any],
    entrada: dict[str, Any],
    modo: str,
) -> dict[str, Any]:
    adquisicion: dict[str, Any] = copy.deepcopy(compra)
    adquisicion[NUMERO] = -entrada[NUMERO]
    adquisicion[COMISIONES] = (
        adquisicion[COMISIONES] * adquisicion[NUMERO] / compra[NUMERO]
    )
    recalcular_movimiento(adquisicion)

    compra[NUMERO] += entrada[NUMERO]
    compra[COMISIONES] -= adquisicion[COMISIONES]
    recalcular_movimiento(compra)

    return crear_operacion(adquisicion, entrada, modo)
