from collections.abc import Iterator
from typing import NamedTuple, cast

from pandas import DataFrame

from constantes import BOLSA, DIVISA, ISIN


def obtener_valores_unicos(movimientos: DataFrame, modo: str) -> Iterator[NamedTuple]:
    result: Iterator[NamedTuple] = iter([])
    match modo:
        case "activos":
            result = cast(
                "Iterator[NamedTuple]",
                movimientos[[ISIN, BOLSA]].drop_duplicates().itertuples(index=False),
            )

        case "divisas":
            result = cast(
                "Iterator[NamedTuple]",
                movimientos[[DIVISA]].drop_duplicates().itertuples(index=False),
            )
    return result
