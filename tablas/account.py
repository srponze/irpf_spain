from pathlib import Path

import pandas as pd
from pandas import DataFrame

from constantes import (
    FECHA,
    ORDEN_ACCOUNT,
    ORDEN_ACCOUNT_CSV,
    SALDO,
    TIPO,
    USECOLS_ACCOUNT_CSV,
    VARIACION,
)
from tablas.funciones import fecha_hora, punto_x_coma


def leer_account(ruta: Path) -> DataFrame:

    account: DataFrame = pd.read_csv(
        ruta,
        header=0,
        names=ORDEN_ACCOUNT_CSV,
        usecols=USECOLS_ACCOUNT_CSV,
        converters={
            TIPO: punto_x_coma,
            VARIACION: punto_x_coma,
            SALDO: punto_x_coma,
        },
    )[ORDEN_ACCOUNT]

    account: DataFrame = account.dropna(subset=[FECHA]).reset_index(drop=True)
    account: DataFrame = fecha_hora(account)

    return account
