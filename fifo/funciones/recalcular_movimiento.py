from typing import Any

from constantes import COMISIONES, NUMERO, PRECIO, TIPO, TOTAL, VALOR_EUR, VALOR_LOCAL


def recalcular_movimiento(movimiento: dict[str, Any]) -> None:
    movimiento[VALOR_LOCAL] = -movimiento[NUMERO] * movimiento[PRECIO]
    movimiento[VALOR_EUR] = movimiento[VALOR_LOCAL] * movimiento[TIPO]
    movimiento[TOTAL] = movimiento[VALOR_EUR] + movimiento[COMISIONES]
