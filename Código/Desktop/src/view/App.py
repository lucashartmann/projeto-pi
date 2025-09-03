from textual.app import App
from view import TelaClientela, TelaEstoque, TelaCliente, TelaProduto, TelaInicial


class App(App):
    SCREENS = {
        "tela_inicial": TelaInicial.ScreenInicial,
        "tela_estoque": TelaEstoque.TelaEstoque,
        "tela_cliente": TelaCliente.TelaCliente,
        "tela_produto": TelaProduto.TelaProduto,
        "tela_clientela": TelaClientela.TelaClientela
    }

    def on_mount(self):
        self.push_screen("tela_inicial")
