from decimal import Decimal

from pandas import DataFrame, Series

from constantes import (
    COMISIONES_ADQUISICION,
    COMISIONES_TRANSMISION,
    GANANCIA_PERDIDA,
    PRECIO_ADQUISICION,
    PRECIO_TRANSMISION,
    TIPO,
    TIPO_ADQUISICION,
    TIPO_TRANSMISION,
    TOTAL,
    TOTAL_ADQUISICION,
    TOTAL_TRANSMISION,
    VALOR_EUR,
    VALOR_EUR_ADQUISICION,
    VALOR_EUR_TRANSMISION,
    VALOR_LOCAL_ADQUISICION,
    VALOR_LOCAL_TRANSMISION,
)


def redondear_decimales_operaciones(operaciones: DataFrame, modo: str) -> DataFrame:
    dos = Decimal("0.01")
    cuatro = Decimal("0.0001")
    if modo == "activos":
        operaciones[PRECIO_ADQUISICION] = redondear(
            operaciones[PRECIO_ADQUISICION],
            cuatro,
        )
        operaciones[PRECIO_TRANSMISION] = redondear(
            operaciones[PRECIO_TRANSMISION],
            cuatro,
        )
    operaciones[VALOR_LOCAL_ADQUISICION] = redondear(
        operaciones[VALOR_LOCAL_ADQUISICION],
        dos,
    )
    operaciones[VALOR_LOCAL_TRANSMISION] = redondear(
        operaciones[VALOR_LOCAL_TRANSMISION],
        dos,
    )
    operaciones[VALOR_EUR_ADQUISICION] = redondear(
        operaciones[VALOR_EUR_ADQUISICION],
        dos,
    )
    operaciones[VALOR_EUR_TRANSMISION] = redondear(
        operaciones[VALOR_EUR_TRANSMISION],
        dos,
    )
    operaciones[TIPO_ADQUISICION] = redondear(operaciones[TIPO_ADQUISICION], cuatro)
    operaciones[TIPO_TRANSMISION] = redondear(operaciones[TIPO_TRANSMISION], cuatro)
    operaciones[COMISIONES_ADQUISICION] = redondear(
        operaciones[COMISIONES_ADQUISICION],
        dos,
    )
    operaciones[COMISIONES_TRANSMISION] = redondear(
        operaciones[COMISIONES_TRANSMISION],
        dos,
    )
    operaciones[TOTAL_ADQUISICION] = redondear(operaciones[TOTAL_ADQUISICION], dos)
    operaciones[TOTAL_TRANSMISION] = redondear(operaciones[TOTAL_TRANSMISION], dos)
    operaciones[GANANCIA_PERDIDA] = redondear(operaciones[GANANCIA_PERDIDA], dos)

    return operaciones


def redondear_decimales_movimientos(movimientos: DataFrame) -> DataFrame:
    dos = Decimal("0.01")
    cuatro = Decimal("0.0001")
    movimientos[VALOR_EUR] = redondear(movimientos[VALOR_EUR], dos)
    movimientos[TIPO] = redondear(movimientos[TIPO], cuatro)
    movimientos[TOTAL] = redondear(movimientos[TOTAL], dos)

    return movimientos


def redondear(series: Series, num: Decimal) -> Series:
    return series.apply(lambda x: x.quantize(num))
