from textual.app import App
from textual.containers import Grid
from textual.widgets import Button
from textual.screen import Screen
from view.TelaEstoque import TelaEstoque


class TelaInicial(App):
    MODES = {
        "telaInicial": ScreenInicial
    }

    def on_mount(self):
        self.switch_mode("telaInicial")
        

class ScreenInicial(Screen):
    CSS_PATH = "css/TelaInicial.tcss"

    MODES = {
        "estoque": TelaEstoque
    }

    def compose(self):
        with Grid():
            yield Button("Produto")
            yield Button("Cliente")
            yield Button("Fornecedor")
            yield Button("Funcionario")
            yield Button("Estoque", id="Estoque")

    def on_button_pressed(self):
        self.switch_mode("estoque")