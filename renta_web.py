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
        page.wait_for_timeout(self.tiempo_espera)
        page.get_by_text("Ganancias y pérdidas").click()
        page.get_by_text("Acciones cotizadas").click()

        anterior_producto: str = ""

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

    def introducir_divisas(
        self,
        fifo_divisas: DataFrame,
    ) -> None:
        page: Page = self.page

        #     ######## Ir al apartado de divisas ########
        page.get_by_role("button", name="Apartados declaración").click()
        page.wait_for_timeout(self.tiempo_espera)
        page.get_by_text("Ganancias y pérdidas").click()
        page.get_by_text("Acciones no cotizadas").click()

        for row in fifo_divisas.itertuples():
            if page.get_by_role(
                "button",
                name="Alta Elemento Patrimonial",
            ).is_visible():
                page.get_by_role("button", name="Alta Elemento Patrimonial").click()
                page.wait_for_timeout(self.tiempo_espera)

            page.locator(".botonLanzaVentana").nth(0).click()
            page.wait_for_timeout(self.tiempo_espera)

            page.get_by_title(
                "Otros elementos patrimoniales (bienes o derechos)",
            ).click()
            page.get_by_role("button", name="Aceptar").click()
            page.wait_for_timeout(self.tiempo_espera)

            page.locator(".botonLanzaVentana").nth(1).click()
            page.wait_for_timeout(self.tiempo_espera)

            page.get_by_title(
                "Transmisión intervivos onerosa (venta, permuta, etc):",
            ).get_by_label("").check()
            page.wait_for_timeout(self.tiempo_espera)

            page.get_by_role("combobox", name="Fecha de transmisión").get_by_role(
                "textbox",
            ).fill(row.fecha_hora_tr.strftime("%d/%m/%Y"))
            page.wait_for_timeout(self.tiempo_espera)

            page.get_by_role("combobox", name="Fecha de adquisición").get_by_role(
                "textbox",
            ).fill(row.fecha_hora_ad.strftime("%d/%m/%Y"))
            page.wait_for_timeout(self.tiempo_espera)

            page.get_by_role("dialog").get_by_role(
                "textbox",
                name="Valor de transmisión",
            ).dblclick()
            page.wait_for_timeout(self.tiempo_espera)

            page.get_by_role(
                "textbox",
                name="Importe de la transmisión",
            ).press_sequentially(str(abs(row.total_tr)))
            page.get_by_role("button", name="Aceptar").nth(1).click()

            page.get_by_role("dialog").get_by_role(
                "textbox",
                name="Valor de adquisición",
            ).dblclick()
            page.wait_for_timeout(self.tiempo_espera)

            page.get_by_role(
                "textbox",
                name="Importe de la adquisición",
            ).press_sequentially(str(abs(row.total_ad)))
            page.get_by_role("button", name="Aceptar").nth(1).click()

            page.get_by_role("button", name="Aceptar").nth(0).click()

        self.esperar()

    def esperar(self) -> None:
        self.page.wait_for_timeout(10000000)

    def close(self) -> None:
        if self.page is not None:
            self.page.close()
        if self.browser is not None:
            self.browser.close()
        if self.p is not None:
            self.p.stop()
