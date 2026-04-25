from pandas import DataFrame
from playwright.sync_api import Browser, Page, Playwright, sync_playwright


class RentaWeb:
    p: Playwright
    browser: Browser
    page: Page

    def iniciar(self) -> None:
        self.tiempo_espera: int = 500

        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(channel="chromium", headless=False)
        self.page = self.browser.new_page()
        self.page.goto(
            "https://sede.agenciatributaria.gob.es/static_files/common/html/selector_acceso/SelectorAccesos.html?rep=S&ref=%2Fwlpl%2FDASR-CORE%2FAccesoDR2025RVlt&aut=CPRE",
        )

    def login(self) -> None:
        page: Page = self.page
        page.get_by_role("button", name="Certificado o DNI electrónico").click()
        page.wait_for_timeout(
            2000,
        )  # Pausa para hacer click aceptar usar tu certificado digital
        page.get_by_role("button", name="CONFIRMAR").click()
        with self.page.expect_popup() as page1_info:
            page.get_by_role("link", name="Servicio tramitación de").click()
        page: Page = page1_info.value
        page.get_by_role("button", name="Ir a Renta WEB Ir a Renta WEB").click()
        page.get_by_role("button", name="Continuar sesión").click()
        self.page = page

    def introducir_activos(
        self,
        fifo_activos: DataFrame,
    ) -> None:
        page: Page = self.page

        ######## Ir al apartado de acciones ########
        page.get_by_role("button", name="Apartados declaración").click()
        if page.get_by_text("Ganancias y pérdidas").is_hidden():
            page.get_by_text("Ganancias y pérdidas").click()
        page.get_by_text("Acciones cotizadas").click()

        anterior_producto = ""

        for row in fifo_activos.itertuples():
            if row.producto != anterior_producto:
                if page.get_by_role("button", name="Aceptar").is_visible():
                    page.get_by_role("button", name="Aceptar").click()
                page.wait_for_timeout(self.tiempo_espera)

                if page.get_by_role("button", name="Alta Entidad Emisora").is_enabled():
                    page.get_by_role("button", name="Alta Entidad Emisora").click()
                page.wait_for_timeout(self.tiempo_espera)

                page.locator(".botonLanzaVentana").nth(0).click()
                page.wait_for_timeout(self.tiempo_espera)

                page.get_by_role("textbox", name="Entidad Emisora:").fill(row.producto)
                page.wait_for_timeout(self.tiempo_espera)

            else:
                page.get_by_role("button", name="Alta Ganancia/Pérdida").click()
                page.wait_for_timeout(self.tiempo_espera)

            page.get_by_role(
                "textbox",
                name="Valor de transmisión (*):",
            ).press_sequentially(str(abs(row.total_tr)))
            page.wait_for_timeout(self.tiempo_espera)

            page.get_by_role(
                "textbox",
                name="Valor de adquisición (*):",
            ).press_sequentially(str(abs(row.total_ad)))
            page.wait_for_timeout(self.tiempo_espera)

            anterior_producto = row[3]

        self.esperar()

    # def introducir_divisas(
    #     self,
    #     divisas: DataFrame,
    # ) -> None:
    #     page: Page = self.page

    #     ######## Ir al apartado de divisas ########
    #     page.wait_for_timeout(TIEMPOESPERA)
    #     page.get_by_role("button", name="Apartados declaración").click()
    #     if page.get_by_text(
    #         "Ganancias y pérdidas patrimoniales (Ventas de bienes, subvenciones, premios, etc)",
    #     ).is_hidden():
    #         page.get_by_text(
    #             "Ganancias y pérdidas patrimoniales (Ventas de bienes, subvenciones, premios, etc)",
    #         ).click()
    #     page.get_by_text("Acciones no cotizadas").click()

    #     altaNuevaTransaccion = False

    #     for divisa in transaccionesDivisas:
    #         for transaccion in transaccionesDivisas[divisa]:
    #             if altaNuevaTransaccion != False:
    #                 page.wait_for_timeout(TIEMPOESPERA)
    #                 page.get_by_role("button", name="Alta Elemento Patrimonial").click()

    #             ####### Otros elementos patrimoniales #######
    #             page.wait_for_timeout(TIEMPOESPERA)
    #             page.locator(".botonLanzaVentana").nth(0).click()
    #             page.get_by_title(
    #                 "Otros elementos patrimoniales (bienes o derechos)",
    #             ).click()
    #             page.get_by_role("button", name="Aceptar").click()

    #             page.locator(".botonLanzaVentana").nth(1).click()

    #             page.get_by_title(
    #                 "Transmisión intervivos onerosa (venta, permuta, etc):",
    #             ).get_by_label("").check()

    #             ####### Fecha de adquisición #######
    #             page.wait_for_timeout(TIEMPOESPERA)
    #             fechaAdquisicion = transaccion.adquisicion.fecha.strftime(
    #                 "%d/%m" + "/2024",
    #             )  # Para el simulador del 2024
    #             page.get_by_role("combobox", name="Fecha de adquisición:").get_by_role(
    #                 "textbox",
    #             ).fill(fechaAdquisicion)

    #             ####### Fecha de transmisión #######
    #             page.wait_for_timeout(TIEMPOESPERA)
    #             fechaTransmision = transaccion.transmision.fecha.strftime(
    #                 "%d/%m" + "/2024",
    #             )  # Para el simulador del 2024
    #             page.get_by_role("combobox", name="Fecha de transmisión:").get_by_role(
    #                 "textbox",
    #             ).fill(fechaTransmision)

    #             ####### Valor de adquisición #######
    #             page.wait_for_timeout(TIEMPOESPERA)
    #             page.get_by_role("dialog").get_by_role(
    #                 "textbox",
    #                 name="Valor de adquisición:",
    #             ).dblclick()
    #             valorAdquisicion = str(abs(transaccion.adquisicion.total))
    #             page.get_by_role(
    #                 "textbox",
    #                 name="Importe de la adquisición",
    #             ).press_sequentially(valorAdquisicion)
    #             # page.get_by_role("textbox", name="Gastos de la adquisición")
    #             page.get_by_role("button", name="Aceptar").nth(1).click()

    #             ####### Valor de transmisión #######
    #             page.wait_for_timeout(TIEMPOESPERA)
    #             page.get_by_role("dialog").get_by_role(
    #                 "textbox",
    #                 name="Valor de transmisión:",
    #             ).dblclick()
    #             valorTransmision = str(abs(transaccion.transmision.total))
    #             page.get_by_role(
    #                 "textbox",
    #                 name="Importe de la transmisión",
    #             ).press_sequentially(valorTransmision)
    #             # page.get_by_role("textbox", name="Gastos de la transmisión")
    #             page.get_by_role("button", name="Aceptar").nth(1).click()

    #             page.get_by_role("button", name="Aceptar").nth(0).click()

    #             altaNuevaTransaccion = True

    def esperar(self) -> None:
        self.page.wait_for_timeout(10000000)

    def close(self) -> None:
        if self.page is not None:
            self.page.close()
        if self.browser is not None:
            self.browser.close()
        if self.p is not None:
            self.p.stop()
