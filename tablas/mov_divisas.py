from decimal import Decimal

import pandas as pd
from pandas import DataFrame

from constantes import (
    COMISIONES,
    DIVISA,
    FECHA_HORA,
    NUMERO,
    PRECIO,
    PRODUCTO,
    TIPO,
    TOTAL,
    VALOR_EUR,
    VALOR_LOCAL,
    VARIACION,
)
from tablas.funciones import decimal


def obtener_mov_divisas(
    _transactions: DataFrame,
    _account: DataFrame,
) -> DataFrame:

    transactions: DataFrame = _transactions.copy()
    account: DataFrame = _account.copy()
    transactions = transactions[(transactions[DIVISA] != "EUR")]
    transactions[NUMERO] = transactions[VALOR_LOCAL] = decimal(
        transactions[VALOR_LOCAL],
    )
    transactions[PRECIO] = Decimal(1)
    transactions[VALOR_LOCAL] = -transactions[VALOR_LOCAL]
    transactions[VALOR_EUR] = -decimal(transactions[VALOR_EUR])
    transactions[TIPO] = transactions[TIPO].apply(
        lambda x: Decimal(1) / Decimal(x) if x != "" else Decimal(1),
    )
    transactions[COMISIONES] = Decimal(0)
    transactions[TOTAL] = -decimal(transactions[TOTAL])
    transactions: DataFrame = pd.concat(
        [transactions[FECHA_HORA], transactions.iloc[:, 1], transactions.iloc[:, 4:]],
        axis=1,
    )

    account: DataFrame = account[
        (account[PRODUCTO].str.startswith("EUR/")) & (account[DIVISA] != "EUR")
    ]
    account: DataFrame = account[
        [FECHA_HORA, PRODUCTO, VARIACION, TIPO, DIVISA]
    ].rename(columns={VARIACION: VALOR_LOCAL})
    account[NUMERO] = account[VALOR_LOCAL] = decimal(account[VALOR_LOCAL])
    account[VALOR_LOCAL] = -account[VALOR_LOCAL]
    account[PRECIO] = Decimal(1)
    account[TIPO] = account[TIPO].apply(
        lambda x: Decimal(1) / Decimal(x) if x != "" else Decimal(0),
    )
    account[VALOR_EUR] = account[VALOR_LOCAL] * account[TIPO]
    account[COMISIONES] = Decimal(0)
    account[TOTAL] = account[VALOR_EUR]
    return (
        pd.concat([transactions, account], axis=0)
        .sort_values(by=FECHA_HORA, ascending=False)
        .reset_index(drop=True)
    )
