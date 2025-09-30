from textual.containers import Grid
from textual.widgets import Button, Footer, Header
from textual.screen import Screen


class ScreenInicial(Screen):
    CSS_PATH = "css/TelaInicial.tcss"

    def compose(self):
        yield Header()
        with Grid():
            yield Button("Produto", id="bt_produto")
            yield Button("Pessoa", id="bt_pessoa")
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