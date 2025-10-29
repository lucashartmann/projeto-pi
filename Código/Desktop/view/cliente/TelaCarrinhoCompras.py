from textual.screen import Screen
from textual.widgets import Static, Checkbox, Select, Tab, Tabs
from textual.containers import HorizontalGroup, VerticalGroup

from textual_image.widget import Image


class TelaCarrinhoCompras(Screen):
    CSS_PATH = "css/TelaCarrinhoCompras.tcss"

    def compose(self):
        yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Carrinho", id="tab_carrinho_compras"), Tab("Dados", id="tab_dados_usuario"))
        with HorizontalGroup():
            with VerticalGroup(id="produtos"):
                pass
            with VerticalGroup(id="pagamento"):
                yield Static("Total: [green]R$ 0,00 [/]")
                yield Static("Forma de Pagamento:")
                yield Checkbox("Cartão de Débito")
                yield Checkbox("Cartão de Crédito", id="chx_cartao_credito")
                yield Checkbox("Boleto")
                yield Checkbox("Pix")

    def on_checkbox_changed(self, evento: Checkbox.Changed):
        if evento.checkbox.id == "#chx_cartao_credito" and evento.checkbox.value == True:
            self.mount(Static("Parcelamento:"))
            self.mount(Select([("1x", "1x"), ("2x", "2x"), ("3x", "3x"), ("4x", "4x"), ("5x", "5x"), ("6x", "6x"), (
                "7x", "7x"), ("8x", "8x"), ("9x", "9x"), ("10x", "10x"), ("11x", "11x"), ("12x", "12x")]))

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_comprar", Tab).id:
            self.app.switch_screen("tela_estoque_cliente")
        elif event.tabs.active == self.query_one("#tab_dados_usuario", Tab).id:
            self.app.switch_screen("tela_dados_usuario")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_carrinho_compras", Tab).id
