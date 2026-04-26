from pathlib import Path

import pandas as pd
from pandas import DataFrame

from constantes import (
    COMISIONES,
    DIVISA,
    FECHA,
    HORA,
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
from tablas.funciones import fecha, fecha_hora, punto_x_coma
from tablas.usdeur import obtener_tipos_usdeur


def leer_transactions(ruta: Path) -> DataFrame:
    transactions = pd.read_csv(
        ruta,
        header=0,
        names=ORDEN_TRANSACTIONS_CSV,
        usecols=USECOLS_TRANSACTIONS_CSV,
        converters={
            FECHA: fecha,
            NUMERO: punto_x_coma,
            PRECIO: punto_x_coma,
            VALOR_LOCAL: punto_x_coma,
            VALOR_EUR: punto_x_coma,
            TIPO: punto_x_coma,
            COMISIONES: punto_x_coma,
            TOTAL: punto_x_coma,
        },
    )[ORDEN_TRANSACTIONS]
    transactions = transactions.dropna(subset=[HORA]).reset_index(drop=True)

    tipos_bce: DataFrame = obtener_tipos_usdeur()
    tipos_bce = tipos_bce.dropna(subset=[FECHA]).sort_values(by=FECHA)

    mask_usd = transactions[DIVISA] == "USD"
    if mask_usd.any():
        fx = (
            transactions.loc[mask_usd, [FECHA]]
            .assign(
                **{
                    FECHA: pd.to_datetime(
                        transactions.loc[mask_usd, FECHA],
                        format="%Y-%m-%d",
                        errors="coerce",
                    ),
                },
            )
            .merge(tipos_bce, on=FECHA, how="left")
        )

        transactions.loc[mask_usd, TIPO] = fx[TIPO].to_numpy()

    transactions: DataFrame = fecha_hora(transactions)
    return transactions
