from typing import DefaultDict, Tuple

from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from irpfSpain.constantes.urls import *
from irpfSpain.modelo.entidades.transaccion import Transaccion


class Play:

    p: Playwright
    browser: Browser
    page: Page

    def iniciar(
        self, channel: str, headless: bool, modoSimulador: bool, tiempoDeEspera: int
    ):
        self.TIEMPODEESPERA = tiempoDeEspera
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(channel=channel, headless=headless)
        self.page = self.browser.new_page()
        if modoSimulador:
            self.page.goto(urlSimulador)
            self.introducirDatosGenericos()

    def introducirDatosGenericos(self):
        page = self.page
        page.get_by_role("button", name="Nueva declaración").click()
        page.get_by_role("textbox", name="NIF:").first.fill("01111111G")
        page.get_by_role("textbox", name="Apellidos y nombre:").first.fill(
            "XXXXX XXXXX XXXXXXXX"
        )
        page.get_by_role("combobox", name="Estado Civil (a 31/12/2024)").get_by_role(
            "textbox"
        ).click()
        page.get_by_role("listitem").filter(has_text="SOLTERO/A").click()
        page.get_by_role("combobox", name="Fecha de nacimiento:").get_by_role(
            "textbox"
        ).fill("10/10/2000")
        page.get_by_role("radio", name="Hombre").check()
        page.get_by_role("combobox", name="Comunidad Autónoma").get_by_label(
            "Expand"
        ).click()
        page.get_by_role("listitem").filter(has_text="ANDALUCIA").click()
        page.get_by_role("button", name="Aceptar").click()

    def introducirActivos(
        self, transaccionesAcciones: DefaultDict[Tuple[str, str], list[Transaccion]]
    ):
        page = self.page
        TIEMPOESPERA = self.TIEMPODEESPERA

        ######## Ir al apartado de acciones ########
        page.get_by_role("button", name="Apartados declaración").click()
        if page.get_by_text(
            "Ganancias y pérdidas patrimoniales (Ventas de bienes, subvenciones, premios, etc)"
        ).is_hidden():
            page.get_by_text(
                "Ganancias y pérdidas patrimoniales (Ventas de bienes, subvenciones, premios, etc)"
            ).click()
        page.get_by_text("Acciones cotizadas").click()

        altaNuevaProducto = False
        altaNuevaTransaccion = False

        for key in transaccionesAcciones:
            if altaNuevaProducto != False:
                page.get_by_role("button", name="Alta Entidad Emisora").click()

            page.locator(".botonLanzaVentana").click()

            ######## Introducir nombre del producto ########
            page.get_by_role("textbox", name="Entidad Emisora:").fill(key[0])

            for transaccion in transaccionesAcciones[key]:
                if altaNuevaTransaccion != False:
                    page.get_by_role("button", name="Alta Ganancia/Pérdida").click()

                ####### Valor de transmisión #######
                page.wait_for_timeout(TIEMPOESPERA)
                valorTransmision = str(abs(transaccion.transmision.total))
                page.get_by_role(
                    "textbox", name="Valor de transmisión (*):"
                ).press_sequentially(valorTransmision)

                ####### Valor de adquisición #######
                page.wait_for_timeout(TIEMPOESPERA)
                valorAdquisicion = str(abs(transaccion.adquisicion.total))
                page.get_by_role(
                    "textbox", name="Valor de adquisición (*):"
                ).press_sequentially(valorAdquisicion)

                altaNuevaTransaccion = True

            page.get_by_role("button", name="Aceptar").click()
            altaNuevaProducto = True
            altaNuevaTransaccion = False

    def introducirDivisas(
        self, transaccionesDivisas: DefaultDict[str, list[Transaccion]]
    ):
        page = self.page
        TIEMPOESPERA = self.TIEMPODEESPERA

        ######## Ir al apartado de divisas ########
        page.wait_for_timeout(TIEMPOESPERA)
        page.get_by_role("button", name="Apartados declaración").click()
        if page.get_by_text(
            "Ganancias y pérdidas patrimoniales (Ventas de bienes, subvenciones, premios, etc)"
        ).is_hidden():
            page.get_by_text(
                "Ganancias y pérdidas patrimoniales (Ventas de bienes, subvenciones, premios, etc)"
            ).click()
        page.get_by_text("Acciones no cotizadas").click()

        altaNuevaTransaccion = False

        for divisa in transaccionesDivisas:
            for transaccion in transaccionesDivisas[divisa]:
                if altaNuevaTransaccion != False:
                    page.wait_for_timeout(TIEMPOESPERA)
                    page.get_by_role("button", name="Alta Elemento Patrimonial").click()

                ####### Otros elementos patrimoniales #######
                page.wait_for_timeout(TIEMPOESPERA)
                page.locator(".botonLanzaVentana").nth(0).click()
                page.get_by_title(
                    "Otros elementos patrimoniales (bienes o derechos)"
                ).click()
                page.get_by_role("button", name="Aceptar").click()

                page.locator(".botonLanzaVentana").nth(1).click()

                page.get_by_title(
                    "Transmisión intervivos onerosa (venta, permuta, etc):"
                ).get_by_label("").check()

                ####### Fecha de adquisición #######
                page.wait_for_timeout(TIEMPOESPERA)
                fechaAdquisicion = transaccion.adquisicion.fecha.strftime(
                    "%d/%m" + "/2024"
                )  # Para el simulador del 2024
                page.get_by_role("combobox", name="Fecha de adquisición:").get_by_role(
                    "textbox"
                ).fill(fechaAdquisicion)

                ####### Fecha de transmisión #######
                page.wait_for_timeout(TIEMPOESPERA)
                fechaTransmision = transaccion.transmision.fecha.strftime(
                    "%d/%m" + "/2024"
                )  # Para el simulador del 2024
                page.get_by_role("combobox", name="Fecha de transmisión:").get_by_role(
                    "textbox"
                ).fill(fechaTransmision)

                ####### Valor de adquisición #######
                page.wait_for_timeout(TIEMPOESPERA)
                page.get_by_role("dialog").get_by_role(
                    "textbox", name="Valor de adquisición:"
                ).dblclick()
                valorAdquisicion = str(abs(transaccion.adquisicion.total))
                page.get_by_role(
                    "textbox", name="Importe de la adquisición"
                ).press_sequentially(valorAdquisicion)
                # page.get_by_role("textbox", name="Gastos de la adquisición")
                page.get_by_role("button", name="Aceptar").nth(1).click()

                ####### Valor de transmisión #######
                page.wait_for_timeout(TIEMPOESPERA)
                page.get_by_role("dialog").get_by_role(
                    "textbox", name="Valor de transmisión:"
                ).dblclick()
                valorTransmision = str(abs(transaccion.transmision.total))
                page.get_by_role(
                    "textbox", name="Importe de la transmisión"
                ).press_sequentially(valorTransmision)
                # page.get_by_role("textbox", name="Gastos de la transmisión")
                page.get_by_role("button", name="Aceptar").nth(1).click()

                page.get_by_role("button", name="Aceptar").nth(0).click()

                altaNuevaTransaccion = True

    def esperar(self):
        self.page.wait_for_timeout(10000000)

    def close(self):
        if self.page is not None:
            self.page.close()
        if self.browser is not None:
            self.browser.close()
        if self.p is not None:
            self.p.stop()
