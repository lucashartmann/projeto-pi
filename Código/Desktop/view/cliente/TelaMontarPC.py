from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Button, Static, Tab, Tabs


class TelaMontarPC(Screen):
    CSS_PATH = "css/TelaMontarPC.tcss"

    def compose(self):
        yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Carrinho", id="tab_carrinho_compras"), Tab("Dados", id="tab_dados_usuario"), Tab("Montar PC", id="tab_montar_pc"))
        yield Header()
        yield Horizontal(Static("CPU"), Button("Escolher"), id="ct_cpu")
        yield Horizontal(Static("Placa Mãe"), Button("Escolher"), id="ct_motherboard")
        yield Horizontal(Static("Memória RAM"), Button("Escolher"), id="ct_ram")
        yield Horizontal(Static("Armazenamento"), Button("Escolher"), id="ct_storage")
        yield Horizontal(Static("Placa de Vídeo"), Button("Escolher"), id="ct_gpu")
        yield Horizontal(Static("Gabinete"), Button("Escolher"), id="ct_case")
        yield Horizontal(Static("Cooler"), Button("Escolher"), id="ct_fans")
        yield Static("Total: R$ 0,00", id="st_total")
        yield Button("Comprar")
        yield Footer()

    def on_button_pressed(self):
        self.app.switch_screen("tela_estoque")  # TODO: arrumar

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_comprar", Tab).id:
            self.app.switch_screen("tela_estoque_cliente")
        elif event.tabs.active == self.query_one("#tab_dados_usuario", Tab).id:
            self.app.switch_screen("tela_dados_usuario")
        elif event.tabs.active == self.query_one("#tab_carrinho_compras", Tab).id:
            self.app.switch_screen("tela_carrinho_compras")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_montar_pc", Tab).id
