from textual.app import App
from textual.binding import Binding

from model import Init

from view import TelaClientela, TelaInicial, TelaPessoa, TelaProduto, TelaLogin, TelaEstoque, TelaEstoqueCliente


class App(App):
    CSS_PATH = "css/Base.tcss"
    
    SCREENS = {
        "tela_inicial": TelaInicial.ScreenInicial,
        "tela_pessoa": TelaPessoa.TelaPessoa,
        "tela_produto": TelaProduto.TelaProduto,
        "tela_login": TelaLogin.TelaLogin,
        "tela_estoque": TelaEstoque.TelaEstoque,
        "tela_clientela": TelaClientela.TelaClientela,
        "tela_estoque_cliente": TelaEstoqueCliente.TelaEstoqueCliente
    }
    
    
    BINDINGS = {
        Binding("ctrl+l", "switch_screen('tela_estoque_cliente')", "Tela Estoque"),
    }


    def on_mount(self):
        Init.inicializar()
        self.push_screen("tela_inicial")
        # self.push_screen("tela_login")
        
    def action_cadastro(self):
        tela_login = self.get_screen("tela_login")
        tela_login.montar_cadastro()