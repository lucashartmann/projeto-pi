from textual.app import App
from textual.binding import Binding

from model import Init

from view import TelaCadastro, TelaLogin, TelaEstoque, TelaDadosLoja
from view.cliente import TelaEstoqueCliente, TelaCarrinhoCompras, TelaDadosUsuario, TelaMontarPC
from view.admin import TelaServidor


class App(App):
    CSS_PATH = "css/Base.tcss"

    SCREENS = {
        "tela_cadastro": TelaCadastro.TelaCadastro,
        "tela_login": TelaLogin.TelaLogin,
        "tela_estoque": TelaEstoque.TelaEstoque,
        "tela_estoque_cliente": TelaEstoqueCliente.TelaEstoqueCliente,
        "tela_carrinho_compras": TelaCarrinhoCompras.TelaCarrinhoCompras,
        "tela_dados_usuario": TelaDadosUsuario.TelaDadosUsuario,
        "tela_dados_loja": TelaDadosLoja.TelaDadosLoja,
        "tela_servidor": TelaServidor.TelaServidor,
        "tela_montar_pc": TelaMontarPC.TelaMontarPC,
    }

    BINDINGS = {
        Binding("ctrl+q", "app.quit", "Sair"),
    }

    def on_mount(self):
        Init.inicializar()
        self.push_screen("tela_login")

    def action_cadastro(self):
        tela_login = self.get_screen("tela_login")
        tela_login.montar_cadastro()
