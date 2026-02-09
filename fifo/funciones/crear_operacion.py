from typing import Any

from constantes import (
    BOLSA,
    COMISIONES,
    COMISIONES_ADQUISICION,
    COMISIONES_TRANSMISION,
    DIVISA,
    FECHA_HORA,
    FECHA_HORA_ADQUISICION,
    FECHA_HORA_TRANSMISION,
    GANANCIA_PERDIDA,
    ISIN,
    NUMERO,
    PRECIO,
    PRECIO_ADQUISICION,
    PRECIO_TRANSMISION,
    PRODUCTO,
    REGLA_2MESES,
    TIPO,
    TIPO_ADQUISICION,
    TIPO_TRANSMISION,
    TOTAL,
    TOTAL_ADQUISICION,
    TOTAL_TRANSMISION,
    VALOR_EUR,
    VALOR_EUR_ADQUISICION,
    VALOR_EUR_TRANSMISION,
    VALOR_LOCAL,
    VALOR_LOCAL_ADQUISICION,
    VALOR_LOCAL_TRANSMISION,
)


def crear_operacion(
    adquisicion: dict[str, Any],
    transmision: dict[str, Any],
    modo: str,
) -> dict[str, Any]:
    operacion = {}
    match modo:
        case "activos":
            operacion: dict[str, Any] = {
                FECHA_HORA_ADQUISICION: adquisicion[FECHA_HORA],
                FECHA_HORA_TRANSMISION: transmision[FECHA_HORA],
                PRODUCTO: adquisicion[PRODUCTO],
                ISIN: adquisicion[ISIN],
                BOLSA: adquisicion[BOLSA],
                NUMERO: adquisicion[NUMERO],
                PRECIO_ADQUISICION: adquisicion[PRECIO],
                PRECIO_TRANSMISION: transmision[PRECIO],
                VALOR_LOCAL_ADQUISICION: adquisicion[VALOR_LOCAL],
                VALOR_LOCAL_TRANSMISION: transmision[VALOR_LOCAL],
                DIVISA: adquisicion[DIVISA],
                VALOR_EUR_ADQUISICION: adquisicion[VALOR_EUR],
                VALOR_EUR_TRANSMISION: transmision[VALOR_EUR],
                TIPO_ADQUISICION: adquisicion[TIPO],
                TIPO_TRANSMISION: transmision[TIPO],
                COMISIONES_ADQUISICION: adquisicion[COMISIONES],
                COMISIONES_TRANSMISION: transmision[COMISIONES],
                TOTAL_ADQUISICION: adquisicion[TOTAL],
                TOTAL_TRANSMISION: transmision[TOTAL],
                GANANCIA_PERDIDA: transmision[TOTAL] + adquisicion[TOTAL],
                REGLA_2MESES: True,
            }
        case "divisas":
            operacion: dict[str, Any] = {
                FECHA_HORA_ADQUISICION: adquisicion[FECHA_HORA],
                FECHA_HORA_TRANSMISION: transmision[FECHA_HORA],
                PRODUCTO: transmision[PRODUCTO],
                VALOR_LOCAL_ADQUISICION: adquisicion[VALOR_LOCAL],
                VALOR_LOCAL_TRANSMISION: transmision[VALOR_LOCAL],
                DIVISA: adquisicion[DIVISA],
                VALOR_EUR_ADQUISICION: adquisicion[VALOR_EUR],
                VALOR_EUR_TRANSMISION: transmision[VALOR_EUR],
                TIPO_ADQUISICION: adquisicion[TIPO],
                TIPO_TRANSMISION: transmision[TIPO],
                COMISIONES_ADQUISICION: adquisicion[COMISIONES],
                COMISIONES_TRANSMISION: transmision[COMISIONES],
                TOTAL_ADQUISICION: adquisicion[TOTAL],
                TOTAL_TRANSMISION: transmision[TOTAL],
                GANANCIA_PERDIDA: transmision[TOTAL] + adquisicion[TOTAL],
            }

    return operacion
