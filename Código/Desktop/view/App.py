from textual.app import App
from textual.binding import Binding

from model import Init

from view import TelaClientela, TelaPessoa, TelaProduto, TelaLogin, TelaEstoque, TelaDadosLoja
from view.cliente import TelaEstoqueCliente, TelaCarrinhoCompras, TelaDadosUsuario
from view.admin import TelaUsuario, TelaUsuariosCadastrados


class App(App):
    CSS_PATH = "css/Base.tcss"

    SCREENS = {
        "tela_pessoa": TelaPessoa.TelaPessoa,
        "tela_produto": TelaProduto.TelaProduto,
        "tela_login": TelaLogin.TelaLogin,
        "tela_estoque": TelaEstoque.TelaEstoque,
        "tela_clientela": TelaClientela.TelaClientela,
        "tela_estoque_cliente": TelaEstoqueCliente.TelaEstoqueCliente,
        "tela_carrinho_compras": TelaCarrinhoCompras.TelaCarrinhoCompras,
        "tela_dados_usuario": TelaDadosUsuario.TelaDadosUsuario,
        "tela_dados_loja": TelaDadosLoja.TelaDadosLoja,
        "tela_usuario": TelaUsuario.TelaUsuario,
        "tela_usuarios_cadastrados": TelaUsuariosCadastrados.TelaUsuariosCadastrados
    }

    BINDINGS = {
        Binding("ctrl+l", "switch_screen('tela_estoque_cliente')", "Tela Estoque"),
    }

    def on_mount(self):
        Init.inicializar()
        # self.push_screen("tela_estoque_cliente")
        self.push_screen("tela_login")

    def action_cadastro(self):
        tela_login = self.get_screen("tela_login")
        tela_login.montar_cadastro()
