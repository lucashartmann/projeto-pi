from textual.app import App
from view import TelaPessoa, TelaProduto, TelaInicial


class App(App):
    SCREENS = {
        "tela_inicial": TelaInicial.ScreenInicial,
        "tela_pessoa": TelaPessoa.TelaPessoa,
        "tela_produto": TelaProduto.TelaProduto,
    }

    def on_mount(self):
        self.push_screen("tela_inicial")
