from textual.containers import Grid
from textual.widgets import Button, Footer, Header
from textual.screen import Screen

from model import Init

class ScreenInicial(Screen):
    CSS_PATH = "css/TelaInicial.tcss"

    def compose(self):
        yield Header()
        with Grid():
            match Init.usuario.get_tipo():
                case "cliente":
                    yield Button("Comprar", id="bt_produto")
                    yield Button("Dados", id="bt_pessoa")
                case "gerente":
                    yield Button("Produto", id="bt_produto")
                    yield Button("Pessoa", id="bt_pessoa")
                case "administrador":
                    yield Button("Produto", id="bt_produto")
                    yield Button("Pessoa", id="bt_pessoa")
                    yield Button("Usuario", id="bt_usuario")
            yield Button("Sair", id="bt_sair")
        yield Footer()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_pessoa":
                self.screen.app.switch_screen("tela_pessoa")
            case "bt_produto":
                self.screen.app.switch_screen("tela_produto")
            case "bt_sair":
                self.screen.app.exit()