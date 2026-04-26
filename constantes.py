# Orden que busco en la tabla
ORDEN_ACCOUNT: list[str] = [
    FECHA := "fecha",
    HORA := "hora",
    PRODUCTO := "producto",
    DESCRIPCION := "descripcion",
    TIPO := "tipo",
    VARIACION := "variacion",
    SALDO := "saldo",
    DIVISA := "divisa",
]

FECHA_HORA = "fecha_hora"


ORDEN_TRANSACTIONS: list[str] = [
    FECHA,
    HORA,
    PRODUCTO,
    ISIN := "isin",
    BOLSA := "bolsa",
    NUMERO := "numero",
    PRECIO := "precio",
    VALOR_LOCAL := "valor_local",
    DIVISA,
    VALOR_EUR := "valor_eur",
    TIPO,
    COMISIONES := "comisiones",
    TOTAL := "total",
]

ORDEN_OPERACIONES: list[str] = [
    FECHA_HORA_ADQUISICION := "fecha_hora_ad",
    FECHA_HORA_TRANSMISION := "fecha_hora_tr",
    PRODUCTO,
    ISIN,
    BOLSA,
    NUMERO,
    PRECIO_ADQUISICION := "precio_ad",
    PRECIO_TRANSMISION := "precio_tr",
    VALOR_LOCAL_ADQUISICION := "valor_local_ad",
    VALOR_LOCAL_TRANSMISION := "valor_local_tr",
    DIVISA,
    VALOR_EUR_ADQUISICION := "valor_eur_ad",
    VALOR_EUR_TRANSMISION := "valor_eur_tr",
    TIPO_ADQUISICION := "tipo_ad",
    TIPO_TRANSMISION := "tipo_tr",
    COMISIONES_ADQUISICION := "comisiones_ad",
    COMISIONES_TRANSMISION := "comisiones_tr",
    TOTAL_ADQUISICION := "total_ad",
    TOTAL_TRANSMISION := "total_tr",
    GANANCIA_PERDIDA := "ganancia_perdida",
    REGLA_2MESES := "regla_2meses",
]


# Orden que tienen los CSV
ORDEN_ACCOUNT_CSV: list[str] = [
    FECHA,
    HORA,
    PRODUCTO,
    DESCRIPCION,
    TIPO,
    VARIACION,
    DIVISA,
    SALDO,
]
USECOLS_ACCOUNT_CSV: list[int] = [0, 1, 3, 5, 6, 8, 9, 10]


ORDEN_TRANSACTIONS_CSV: list[str] = [
    FECHA,
    HORA,
    PRODUCTO,
    ISIN,
    BOLSA,
    NUMERO,
    PRECIO,
    DIVISA,
    VALOR_LOCAL,
    VALOR_EUR,
    TIPO,
    COMISIONES,
    TOTAL,
]
USECOLS_TRANSACTIONS_CSV: list[int] = [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 14, 15]
