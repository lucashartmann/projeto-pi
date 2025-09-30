from textual.app import App
from Desktop.src.view.SQLITE import TelaInicial, TelaPessoa
from Desktop.src.view.SQLITE import TelaProduto


class App(App):
    SCREENS = {
        "tela_inicial": TelaInicial.ScreenInicial,
        "tela_pessoa": TelaPessoa.TelaPessoa,
        "tela_produto": TelaProduto.TelaProduto,
    }

    def on_mount(self):
        self.push_screen("tela_inicial")
