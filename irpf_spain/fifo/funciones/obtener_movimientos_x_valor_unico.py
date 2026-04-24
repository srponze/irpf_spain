from collections.abc import Iterator
from typing import Any, NamedTuple, cast

from pandas import DataFrame

from constantes import BOLSA, DIVISA, ISIN


def obtener_movimientos_x_valor_unico(
    movimientos: DataFrame,
    valor_unico: dict[str, Any],
    modo: str,
) -> Iterator[NamedTuple]:
    result: Iterator[NamedTuple] = iter([])
    match modo:
        case "activos":
            result = cast(
                "Iterator[NamedTuple]",
                movimientos[
                    (movimientos[ISIN] == valor_unico[ISIN])
                    & (movimientos[BOLSA] == valor_unico[BOLSA])
                ][::-1].itertuples(index=False),
            )
        case "divisas":
            result = cast(
                "Iterator[NamedTuple]",
                movimientos[
                    (movimientos[DIVISA] == valor_unico[DIVISA])
                    & (movimientos[DIVISA] != "EUR")
                ][::-1].itertuples(index=False),
            )
    return result
