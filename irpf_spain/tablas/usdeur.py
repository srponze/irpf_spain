import pandas as pd
from pandas import DataFrame

from constantes import FECHA, TIPO


def leer_xml(ruta: str = "usd.xml") -> DataFrame:
    xml: DataFrame = pd.read_xml(
        ruta,
        xpath=".//*[local-name()='Obs']",
        names=[FECHA, TIPO, "A", "B"],
        dtype={FECHA: "string", TIPO: "string"},
    )[[FECHA, TIPO]][::-1]

    return xml
