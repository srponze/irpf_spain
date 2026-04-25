from pathlib import Path

import pandas as pd
from pandas import DataFrame

from constantes import (
    COMISIONES,
    DIVISA,
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
from tablas.usdeur import obtener_tipos_usdeur


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

    tipos_bce: DataFrame = obtener_tipos_usdeur()
    tipos_bce[FECHA] = pd.to_datetime(
        tipos_bce[FECHA],
        format="%d-%m-%Y",
        errors="coerce",
    )
    tipos_bce = tipos_bce.dropna(subset=[FECHA]).sort_values(by=FECHA)

    mask_divisa_no_eur = transactions[DIVISA] != "EUR"
    if mask_divisa_no_eur.any():
        trans_fx = transactions.loc[mask_divisa_no_eur, [FECHA]].copy()
        trans_fx["_idx"] = trans_fx.index
        trans_fx["_fecha"] = pd.to_datetime(
            trans_fx[FECHA],
            format="%d-%m-%Y",
            errors="coerce",
        )
        trans_fx = trans_fx.dropna(subset=["_fecha"]).sort_values(by="_fecha")

        tipos_asof = tipos_bce.rename(columns={FECHA: "_fecha", TIPO: "_tipo_bce"})
        trans_fx = pd.merge_asof(
            trans_fx,
            tipos_asof[["_fecha", "_tipo_bce"]],
            on="_fecha",
            direction="backward",
        )

        if trans_fx["_tipo_bce"].isna().any():
            raise ValueError("No hay tipo BCE para alguna fecha de Transactions.csv")

        transactions.loc[trans_fx["_idx"], TIPO] = trans_fx["_tipo_bce"].values

    transactions: DataFrame = fecha_hora(transactions)

    return transactions


def leer_transactions_bce(ruta: Path) -> DataFrame:
    return leer_transactions(ruta)
