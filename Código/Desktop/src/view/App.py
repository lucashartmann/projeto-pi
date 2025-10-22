from textual.app import App
from view import TelaInicial, TelaPessoa, TelaProduto, TelaLogin, TelaEstoque, TelaPessoal


class App(App):
    SCREENS = {
        "tela_inicial": TelaInicial.ScreenInicial,
        "tela_pessoa": TelaPessoa.TelaPessoa,
        "tela_produto": TelaProduto.TelaProduto,
        "tela_login": TelaLogin.TelaLogin,
        "tela_estoque": TelaEstoque.TelaEstoque,
        "tela_pessoal": TelaPessoal.TelaPessoal
    }

    def on_mount(self):
        self.push_screen("tela_inicial")
