import argparse
import sys
from pathlib import Path

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
from tablas.account import leer_account
from tablas.activos import obtener_activos
from tablas.divisas import obtener_divisas
from tablas.transactions import leer_transactions


def main(args: argparse.Namespace) -> None:  # noqa: C901, PLR0912

    if args.Account:
        account: DataFrame = leer_account(Path(args.Account))
    else:
        account: DataFrame = leer_account("Account.csv")

    if args.Transactions:
        transactions: DataFrame = leer_transactions(Path(args.Transactions))
    else:
        transactions: DataFrame = leer_transactions("Transactions.csv")

    if account.empty or transactions.empty:
        print("Account o Transaction estan vacios")
        sys.exit()

    activos: DataFrame = obtener_activos(transactions)
    divisas: DataFrame = obtener_divisas(transactions, account)
    fifo_activos, posiciones_activos, mov_sin_compra_activos = fifo(activos, "activos")
    fifo_divisas, posiciones_divisas, mov_sin_compra_divisas = fifo(divisas, "divisas")

    lista: list[DataFrame | None] = [fifo_activos, fifo_divisas]

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
            print(
                fifo_activos.groupby(by=[PRODUCTO, DIVISA], as_index=False)[
                    [
                        TOTAL_ADQUISICION,
                        TOTAL_TRANSMISION,
                        GANANCIA_PERDIDA,
                    ]
                ].sum(),
            ) if fifo_activos is not None else print("No hay operaciones de activos")
        else:
            print(fifo_activos) if fifo_activos is not None else print(
                "No hay operaciones de activos",
            )
            print(
                mov_sin_compra_activos,
            ) if mov_sin_compra_activos is not None else None

    elif args.tabla in "divisas":
        if args.agrupado:
            print(
                fifo_divisas.groupby(by=[DIVISA], as_index=False)[
                    [
                        TOTAL_ADQUISICION,
                        TOTAL_TRANSMISION,
                        GANANCIA_PERDIDA,
                    ]
                ].sum(),
            ) if fifo_divisas is not None else print("No hay operaciones de divisas")
        else:
            print(fifo_divisas) if fifo_divisas is not None else print(
                "No hay operaciones de divisas",
            )
            print(
                mov_sin_compra_divisas,
            ) if mov_sin_compra_divisas is not None else None

    elif args.tabla in "posiciones":
        print(posiciones_activos) if posiciones_activos is not None else None
        print(posiciones_divisas) if posiciones_divisas is not None else None


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-A", "--Account")
parser.add_argument("-T", "--Transactions")
parser.add_argument(
    "-t",
    "--tabla",
    help="puede ser 'a', 'act' o 'activos' 'd', 'div' o 'divisas' 'p', 'pos' o 'posiciones'",  # noqa: E501
    default="activos",
)
parser.add_argument("-a", "--agrupado", action="store_true")
parser.add_argument("-y", "--year", type=int)
parser.add_argument("-m", "--month", type=int)
parser.add_argument("-d", "--divisa")
parser.add_argument("-p", "--producto")
args: argparse.Namespace = parser.parse_args()


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


main(args)
