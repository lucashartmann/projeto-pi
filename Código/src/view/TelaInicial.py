from textual.app import App
from textual.containers import Grid
from textual.widgets import Button
from textual.screen import Screen
from view.TelaEstoque import TelaEstoque
from view.TelaCliente import TelaCliente
from view.TelaProduto import TelaProduto


class ScreenInicial(Screen):
    CSS_PATH = "css/TelaInicial.tcss"

    def compose(self):
        with Grid():
            yield Button("Produto", id="bt_produto")
            yield Button("Cliente", id="bt_cliente")
            yield Button("Fornecedor")
            yield Button("Funcionario")
            yield Button("Estoque", id="bt_estoque")
            yield Button("Sair", id="bt_sair")

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_estoque":
                self.screen.app.switch_screen("tela_estoque")
            case "bt_cliente":
                self.screen.app.switch_screen("tela_cliente")
            case "bt_produto":
                self.screen.app.switch_screen("tela_produto")
            case "bt_sair":
                self.screen.app.exit()


class TelaInicial(App):
    SCREENS = {
        "tela_inicial": ScreenInicial,
        "tela_estoque": TelaEstoque,
        "tela_cliente": TelaCliente,
        "tela_produto": TelaProduto
    }

    def on_mount(self):
        self.push_screen("tela_inicial")
