# Calculadora de Ganancias Patrimoniales en el Irpf Español

Esta herramienta simplifica la declaración de la renta para inversores. Automatiza el cálculo de las ganancias y pérdidas patrimoniales derivadas de la compra y venta de acciones cotizadas y ETF.
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

2. Mueve los archivos Account.csv y Transactions.csv al directorio irpfSpain donde se encuentra el fichero irpf_spain.py

3. Ejecuta el script cliente.py:
   ```bash
   python irpf_spain.py
   ```


## Opciones
(Pendiente)


## Licencia
Este proyecto está licenciado bajo la Licencia MIT.


## Contacto
Para preguntas o soporte, contacta a [srponze](https://github.com/srponze).
