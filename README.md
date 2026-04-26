# Calculadora de Ganancias Patrimoniales en el Irpf Español

Esta herramienta simplifica la declaración de la renta para inversores. Automatiza el cálculo de las ganancias y pérdidas patrimoniales derivadas de la compra y venta de acciones cotizadas y ETF. Permite introducir las operaciones en rentaWeb automaticamente usando playwright (Pendiente)
Tambien señala las operaciones que inclumplan la regla antiaplicación (regla de los dos meses) (Pendiente)



## Brokers admitidos
- Degiro


## Características principales
- La aplicación procesa tus informes y determina las ganancias o pérdidas patrimoniales.
- Sigue el metodo FIFO para cumplir con la normativa de la Agencia Tributaria Española.
- Soporta divisas extranjeras, e incluye la propia tributación de la tenencia de divisa extranjera sin AutoFX, puedes leer más sobre esto aquí
   - https://www.filios.app/blog/como-meter-las-operaciones-con-divisas-en-el-irpf/


## Instalación
1. Clona este repositorio o descarga el archivo Zip y descomprímelo:
   ```bash
   git clone https://github.com/srponze/irpfSpain.git
   ```


## Uso
1. Obtén los informes de "Estado de cuenta" y "Transacciones" de tu cuenta de Degiro en formato csv.
   Puedes incluir el rango de fechas que quieras, pero como mínimo que incluya todas las compra-ventas en las que la venta se haya realizado en el año que quieras calcular.

   Ej: Si en 2025 has vendido varias acciones compradas en 2024, aumenta el rango inicial como mínimo hasta el momento de dicha compra, no te preocupes por el resto de acciones que no se hayan vendido en 2025 que incluyas, no se tendrán en cuenta

2. Mueve los archivos Account.csv y Transactions.csv a la raiz del proyecto, tambien si quieres aplicar los tipos de cambio a final del dia del BCE mueve el xml al la    raiz del proyecto y renombralo como tipos_bce.xml

3. Ejecuta el script cliente.py:
   ```bash
   python irpf_spain.py
   ```


## Opciones
usage: irpf_spain.py [-h] [-A ACCOUNT] [-T TRANSACTIONS] [-t TABLA] [-a] [-y YEAR] [-m MONTH] [-d DIVISA] [-p PRODUCTO] [-r] [--all] [--bce]

options:
  -h, --help            show this help message and exit
  -A, --Account ACCOUNT
                        Indica un archivo Account especifico (default: ./Account.csv)
  -T, --Transactions TRANSACTIONS
                        Indica un archivo Transactions especifico (default: ./Transactions.csv)
  -t, --tabla TABLA     TABLA puede ser activos, divisas o posiciones (default: activos)
  -a, --agrupado        Devuelve la tabla agrupada por productos y/o divisa (default: False)
  -y, --year YEAR       Filtra por año los resultados (default: None)
  -m, --month MONTH     Filtra por mes los resultados (default: None)
  -d, --divisa DIVISA   Filtra por divisa los resultados (default: None)
  -p, --producto PRODUCTO
                        Filtra por producto los resultados (default: None)
  -r, --rentaweb        Introduce los resultados que hayas especificado en TABLA (default: False)
  --all                 Muestra todas las filas de la tabla (default: False)
  --bce                 Aplica los tipos de cambio a final del dia del BCE a las transacciones en USD (asegurate de descargar el archivo xml y renombrar a 'tipos_bce.xml' en la raiz
                        del proyecto de aqui https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/usd.xml) (default: False)


## Licencia
Este proyecto está licenciado bajo la Licencia MIT.


## Contacto
Para preguntas o soporte, contacta a [srponze](https://github.com/srponze).
