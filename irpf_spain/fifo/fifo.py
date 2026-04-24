from collections import deque
from typing import Any

from pandas import DataFrame

from constantes import FECHA_HORA, FECHA_HORA_TRANSMISION, NUMERO
from fifo.funciones.crear_operacion import crear_operacion
from fifo.funciones.obtener_movimientos_x_valor_unico import (
    obtener_movimientos_x_valor_unico,
)
from fifo.funciones.obtener_valores_unicos import obtener_valores_unicos
from fifo.funciones.operacion_venta_mayor_compra import operacion_venta_mayor_compra
from fifo.funciones.operacion_venta_menor_compra import operacion_venta_menor_compra
from fifo.funciones.redondear_decimales import (
    redondear_decimales_movimientos,
    redondear_decimales_operaciones,
)


def fifo(
    _movimientos: DataFrame,
    modo: str = "activos",
) -> tuple[
    DataFrame | None,
    DataFrame | None,
    DataFrame | None,
]:
    movimientos = _movimientos.copy()
    lista_global_operaciones: list[dict[str, Any]] = []
    lista_movimientos_sin_compra: list[dict[str, Any]] = []
    lista_posiciones_actuales: list[dict[str, Any]] = []
    for tupla_valor_unico in obtener_valores_unicos(movimientos, modo):
        cola: deque[dict[str, Any]] = deque()
        lista_operaciones: list[dict[str, Any]] = []
        valor_unico: dict[str, Any] = tupla_valor_unico._asdict()

        for tupla_entrada in obtener_movimientos_x_valor_unico(
            movimientos,
            valor_unico,
            modo,
        ):
            entrada: dict[str, Any] = tupla_entrada._asdict()
            if entrada[NUMERO] > 0:
                cola.appendleft(entrada)
            else:
                while cola:
                    if entrada[NUMERO] + cola[-1][NUMERO] > 0:
                        lista_operaciones.append(
                            operacion_venta_menor_compra(cola[-1], entrada, modo),
                        )
                        break
                    if entrada[NUMERO] + cola[-1][NUMERO] < 0:
                        lista_operaciones.append(
                            operacion_venta_mayor_compra(cola.pop(), entrada, modo),
                        )
                    else:
                        lista_operaciones.append(
                            crear_operacion(cola.pop(), entrada, modo),
                        )
                        break
                else:
                    lista_movimientos_sin_compra.append(entrada)
        lista_posiciones_actuales.extend(list(cola))
        lista_global_operaciones.extend(lista_operaciones)

    dataframe_global_operaciones: DataFrame = (
        redondear_decimales_operaciones(
            DataFrame(lista_global_operaciones)
            .sort_values(by=[FECHA_HORA_TRANSMISION], ascending=False)
            .reset_index(drop=True),
            modo,
        )
        if lista_global_operaciones
        else None
    )

    dataframe_posiciones_actuales: DataFrame = (
        redondear_decimales_movimientos(
            DataFrame(lista_posiciones_actuales)
            .sort_values(
                by=[FECHA_HORA],
                ascending=False,
            )
            .reset_index(drop=True),
        )
        if lista_posiciones_actuales
        else None
    )

    dataframe_movimientos_sin_compra: DataFrame = (
        redondear_decimales_movimientos(
            DataFrame(
                lista_movimientos_sin_compra,
            )
            .sort_values(by=[FECHA_HORA], ascending=False)
            .reset_index(drop=True),
        )
        if lista_movimientos_sin_compra
        else None
    )

    return (
        dataframe_global_operaciones,
        dataframe_posiciones_actuales,
        dataframe_movimientos_sin_compra,
    )
