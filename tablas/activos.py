from decimal import Decimal

from pandas import DataFrame

from constantes import COMISIONES, NUMERO, PRECIO, TIPO, TOTAL, VALOR_EUR, VALOR_LOCAL
from tablas.funciones import decimal


def obtener_activos(_transactions: DataFrame) -> DataFrame:

    transactions: DataFrame = _transactions.copy()
    transactions[NUMERO] = transactions[NUMERO].astype(int)
    transactions[PRECIO] = decimal(transactions[PRECIO])
    transactions[VALOR_LOCAL] = decimal(transactions[VALOR_LOCAL])
    transactions[COMISIONES] = decimal(transactions[COMISIONES])
    transactions[VALOR_EUR] = decimal(transactions[VALOR_EUR])
    transactions[TIPO] = transactions[TIPO].apply(
        lambda x: Decimal(1) / Decimal(x) if x != "" else Decimal(1),
    )
    transactions[TOTAL] = decimal(transactions[TOTAL])
    return transactions
