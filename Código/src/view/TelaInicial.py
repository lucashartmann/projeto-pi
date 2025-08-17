from textual.containers import Grid
from textual.widgets import Button, Footer, Header
from textual.screen import Screen


class ScreenInicial(Screen):
    CSS_PATH = "css/TelaInicial.tcss"

    def compose(self):
        yield Header()
        with Grid():
            yield Button("Produto", id="bt_produto")
            yield Button("Cliente", id="bt_cliente")
            yield Button("Fornecedor")
            yield Button("Funcionario")
            yield Button("Estoque", id="bt_estoque")
            yield Button("Clientela", id="bt_clientela")
            yield Button("Sair", id="bt_sair")
        yield Footer()

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
            case "bt_clientela":
                self.screen.app.switch_screen("tela_clientela")
