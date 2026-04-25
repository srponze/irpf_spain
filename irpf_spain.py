import argparse
import sys
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from constantes import (
    DIVISA,
    FECHA_HORA_TRANSMISION,
    GANANCIA_PERDIDA,
    PRODUCTO,
    TOTAL_ADQUISICION,
    TOTAL_TRANSMISION,
)
from fifo.fifo import fifo
from renta_web import RentaWeb
from tablas.account import leer_account
from tablas.mov_activos import obtener_mov_activos
from tablas.mov_divisas import obtener_mov_divisas
from tablas.transactions import leer_transactions


def main(args: argparse.Namespace) -> None:  # noqa: C901, PLR0912, PLR0915

    if args.all:
        pd.options.display.max_rows = 10000

    account: DataFrame = leer_account(Path(args.Account))
    transactions: DataFrame = leer_transactions(Path(args.Transactions))

    if account.empty or transactions.empty:
        print("Account o Transaction estan vacios")
        sys.exit()

    mov_activos: DataFrame = obtener_mov_activos(transactions)
    mov_divisas: DataFrame = obtener_mov_divisas(transactions, account)
    fifo_activos, posiciones_activos, mov_sin_compra_activos = fifo(
        mov_activos,
        "activos",
    )
    fifo_divisas, posiciones_divisas, mov_sin_compra_divisas = fifo(
        mov_divisas,
        "divisas",
    )

    if args.divisa:
        fifo_activos = filtro_divisa(
            fifo_activos,
            args.divisa.upper(),
        )
        fifo_divisas = filtro_divisa(
            fifo_divisas,
            args.divisa.upper(),
        )

    if args.producto:
        fifo_activos = filtro_producto(
            fifo_activos,
            args.producto.upper(),
        )
        fifo_divisas = filtro_producto(
            fifo_divisas,
            args.producto.upper(),
        )

    if args.year:
        if args.month:
            fifo_activos = filtro_anno_mes(
                fifo_activos,
                args.year,
                args.month,
            )
            fifo_divisas = filtro_anno_mes(
                fifo_divisas,
                args.year,
                args.month,
            )

        else:
            fifo_activos = filtro_anno(
                fifo_activos,
                args.year,
            )
            fifo_divisas = filtro_anno(
                fifo_divisas,
                args.year,
            )

    if args.tabla in "activos":
        if args.agrupado:
            fifo_activos = filtro_agrupado(fifo_activos, [PRODUCTO])
            print(fifo_activos)
        else:
            print(fifo_activos)
            print(
                mov_sin_compra_activos,
            ) if mov_sin_compra_activos is not None else None

    elif args.tabla in "divisas":
        if args.agrupado:
            fifo_divisas = filtro_agrupado(fifo_divisas, [DIVISA])
            print(fifo_divisas)
        else:
            print(fifo_divisas)
            print(
                mov_sin_compra_divisas,
            ) if mov_sin_compra_divisas is not None else None

    elif args.tabla in "posiciones":
        print(posiciones_activos) if posiciones_activos is not None else None
        print(posiciones_divisas) if posiciones_divisas is not None else None

    if args.rentaweb:
        rentaweb = RentaWeb()
        rentaweb.iniciar()
        rentaweb.login()
        if args.tabla in "activos":
            rentaweb.introducir_activos(fifo_activos.sort_values(by="producto"))
        elif args.tabla in "divisas":
            pass


def filtro_anno(
    df: DataFrame,
    anno: int,
) -> DataFrame:
    return df[df[FECHA_HORA_TRANSMISION].dt.year == anno] if df is not None else None


def filtro_anno_mes(
    df: DataFrame,
    anno: int,
    mes: int,
) -> DataFrame:
    return (
        df[
            (df[FECHA_HORA_TRANSMISION].dt.year == anno)
            & (df[FECHA_HORA_TRANSMISION].dt.month == mes)
        ]
        if df is not None
        else None
    )


def filtro_divisa(
    df: DataFrame,
    divisa: str,
) -> DataFrame:
    return df[df[DIVISA] == divisa] if df is not None else None


def filtro_producto(
    df: DataFrame,
    producto: str,
) -> DataFrame:
    return df[df[PRODUCTO].str.contains(producto)] if df is not None else None


def filtro_agrupado(df: DataFrame, agrupar_por: list[str]) -> DataFrame:
    return df.groupby(by=agrupar_por, as_index=False)[
        [
            TOTAL_ADQUISICION,
            TOTAL_TRANSMISION,
            GANANCIA_PERDIDA,
        ]
    ].sum()


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "-A",
    "--Account",
    help="Indica un archivo Account especifico",
    default="./Account.csv",
)
parser.add_argument(
    "-T",
    "--Transactions",
    help="Indica un archivo Transactions especifico",
    default="./Transactions.csv",
)
parser.add_argument(
    "-t",
    "--tabla",
    help="TABLA puede ser activos, divisas o posiciones",
    default="activos",
)
parser.add_argument(
    "-a",
    "--agrupado",
    help="Devuelve la tabla agrupada por productos y/o divisa",
    action="store_true",
)
parser.add_argument("-y", "--year", type=int, help="Filtra por año los resultados")
parser.add_argument("-m", "--month", type=int, help="Filtra por mes los resultados")
parser.add_argument("-d", "--divisa", help="Filtra por divisa los resultados")
parser.add_argument("-p", "--producto", help="Filtra por producto los resultados")
parser.add_argument(
    "-r",
    "--rentaweb",
    help="Introduce los resultados que hayas especificado en TABLA",
    action="store_true",
)
parser.add_argument(
    "--all",
    help="Muestra todas las filas de la tabla",
    action="store_true",
)
args: argparse.Namespace = parser.parse_args()


main(args)
