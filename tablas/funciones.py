from decimal import Decimal

import pandas as pd
from pandas import DataFrame, Series

from constantes import FECHA, FECHA_HORA, HORA


def decimal(serie: Series) -> Series:
    return serie.apply(lambda x: Decimal(x) if x != "" else Decimal(0))


def fecha_hora(df: DataFrame) -> DataFrame:
    return pd.concat(
        [
            pd.to_datetime(
                df[FECHA] + " " + df[HORA],
                format="%d-%m-%Y %H:%M",
            ).rename(FECHA_HORA),
            df.iloc[:, 2:],
        ],
        axis=1,
    )


def punto_x_coma(valor: str) -> str:
    return valor.replace(",", ".")
