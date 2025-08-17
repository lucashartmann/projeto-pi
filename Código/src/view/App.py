from textual.app import App
from view import TelaEstoque, TelaCliente, TelaProduto, TelaInicial


class App(App):
    SCREENS = {
        "tela_inicial": TelaInicial.ScreenInicial,
        "tela_estoque": TelaEstoque.TelaEstoque,
        "tela_cliente": TelaCliente.TelaCliente,
        "tela_produto": TelaProduto.TelaProduto
    }

    def on_mount(self):
        self.push_screen("tela_inicial")
