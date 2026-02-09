import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from constantes import DIVISA, FECHA_HORA_TRANSMISION, PRODUCTO
from fifo.fifo import fifo
from tablas.account import leer_account
from tablas.activos import obtener_activos
from tablas.divisas import obtener_divisas
from tablas.transactions import leer_transactions

if TYPE_CHECKING:
    from pandas import DataFrame


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

    if args.año:
        if args.mes:
            fifo_activos = fifo_activos[
                (fifo_activos[FECHA_HORA_TRANSMISION].dt.year == args.año)
                & (fifo_activos[FECHA_HORA_TRANSMISION].dt.month == args.mes)
            ]
            fifo_divisas = fifo_divisas[
                (fifo_divisas[FECHA_HORA_TRANSMISION].dt.year == args.año)
                & (fifo_divisas[FECHA_HORA_TRANSMISION].dt.month == args.mes)
            ]
        else:
            fifo_activos = fifo_activos[
                fifo_activos[FECHA_HORA_TRANSMISION].dt.year == args.año
            ]

    if args.divisa:
        fifo_activos = fifo_activos[
            fifo_activos[DIVISA].str.contains(args.divisa.upper())
        ]
        fifo_divisas = fifo_divisas[
            fifo_divisas[DIVISA].str.contains(args.divisa.upper())
        ]

    if args.valor:
        fifo_activos = fifo_activos[
            fifo_activos[PRODUCTO].str.contains(args.valor.upper())
        ]
        fifo_divisas = fifo_divisas[
            fifo_divisas[PRODUCTO].str.contains(args.valor.upper())
        ]

    if args.tabla:
        if args.tabla in "activos":
            print(fifo_activos) if not fifo_activos.empty else print(
                "No hay operaciones de activos",
            )
            print(mov_sin_compra_activos) if not mov_sin_compra_activos.empty else None
        elif args.tabla in "divisas":
            print(fifo_divisas) if not fifo_divisas.empty else print(
                "No hay operaciones de divisas",
            )
            print(mov_sin_compra_divisas) if not mov_sin_compra_divisas.empty else None
        elif args.tabla in "posiciones":
            if not posiciones_activos.empty:
                print(posiciones_activos)
            if not posiciones_divisas.empty:
                print(posiciones_divisas)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-A", "--Account")
parser.add_argument("-T", "--Transactions")
parser.add_argument(
    "-t",
    "--tabla",
    help="puede ser 'a', 'act' o 'activos' 'd', 'div' o 'divisas' 'p', 'pos' o 'posiciones'",  # noqa: E501
    default="a",
)
parser.add_argument("-a", "--año", type=int)
parser.add_argument("-m", "--mes", type=int)
parser.add_argument("-d", "--divisa")
parser.add_argument("-v", "--valor")
args: argparse.Namespace = parser.parse_args()

main(args)
