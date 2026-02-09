from pathlib import Path

import pandas as pd
from pandas import DataFrame

from constantes import (
    COMISIONES,
    FECHA,
    NUMERO,
    ORDEN_TRANSACTIONS,
    ORDEN_TRANSACTIONS_CSV,
    PRECIO,
    TIPO,
    TOTAL,
    USECOLS_TRANSACTIONS_CSV,
    VALOR_EUR,
    VALOR_LOCAL,
)
from tablas.funciones import fecha_hora, punto_x_coma


def leer_transactions(ruta: Path) -> DataFrame:
    transactions = pd.read_csv(
        ruta,
        header=0,
        names=ORDEN_TRANSACTIONS_CSV,
        usecols=USECOLS_TRANSACTIONS_CSV,
        converters={
            NUMERO: punto_x_coma,
            PRECIO: punto_x_coma,
            VALOR_LOCAL: punto_x_coma,
            VALOR_EUR: punto_x_coma,
            TIPO: punto_x_coma,
            COMISIONES: punto_x_coma,
            TOTAL: punto_x_coma,
        },
    )[ORDEN_TRANSACTIONS]
    transactions = transactions.dropna(subset=[FECHA]).reset_index(drop=True)
    transactions: DataFrame = fecha_hora(transactions)

    return transactions
