import pandas as pd
from pandas import DataFrame

from constantes import FECHA, TIPO


def obtener_tipos_usdeur(ruta: str = "usd.xml") -> DataFrame:
    tipos_bce: DataFrame = pd.read_xml(
        ruta,
        xpath=".//*[local-name()='Obs']",
        names=[FECHA, TIPO, "A", "B"],
        dtype={FECHA: "string", TIPO: "string"},
    )[[FECHA, TIPO]][::-1]

    tipos_bce[FECHA] = pd.to_datetime(
        tipos_bce[FECHA],
        format="%Y-%m-%d",
        errors="coerce",
    ).dt.strftime("%d-%m-%Y")

    return tipos_bce


def leer_xml(ruta: str = "usd.xml") -> DataFrame:
    return obtener_tipos_usdeur(ruta)
