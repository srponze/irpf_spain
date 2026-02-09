import copy
from typing import Any

from constantes import COMISIONES, NUMERO

from .crear_operacion import crear_operacion
from .recalcular_movimiento import recalcular_movimiento


def operacion_venta_mayor_compra(
    compra: dict[str, Any],
    entrada: dict[str, Any],
    modo: str,
) -> dict[str, Any]:
    transmision: dict[str, Any] = copy.deepcopy(entrada)
    transmision[NUMERO] = -compra[NUMERO]
    transmision[COMISIONES] = (
        transmision[COMISIONES] * transmision[NUMERO] / entrada[NUMERO]
    )
    recalcular_movimiento(transmision)

    entrada[NUMERO] += compra[NUMERO]
    entrada[COMISIONES] -= transmision[COMISIONES]
    recalcular_movimiento(entrada)

    return crear_operacion(compra, transmision, modo)
