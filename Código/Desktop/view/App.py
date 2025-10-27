from textual.app import App
from textual.widgets import Input, Label, Button, Select
from textual.binding import Binding

from model import Init
from controller import Controller

from view import TelaClientela, TelaInicial, TelaPessoa, TelaProduto, TelaLogin, TelaEstoque, TelaDadosLoja
from view.cliente import TelaEstoqueCliente, TelaCarrinhoCompras, TelaDadosUsuario
from view.admin import TelaUsuario, TelaUsuariosCadastrados


class App(App):
    CSS_PATH = "css/Base.tcss"

    SCREENS = {
        "tela_inicial": TelaInicial.ScreenInicial,
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
        self.push_screen("tela_inicial")
        # self.push_screen("tela_login")

    def action_cadastro(self):
        email = self.query(Input)[0].value
        nome = self.query(Input)[1].value
        senha = self.query(Input)[2].value
        tipo_usuario = self.query_one(Select).value

        tela_login = self.get_screen("tela_login")
        tela_login.query_one(Input).placeholder = "Username"
        tela_login.mount(Input(placeholder="Email"),
                         before=tela_login.query_one(Input))
        tela_login.query_one(Label).display = "none"
        tela_login.query_one(Button).label = "Criar conta"
        dados = [nome, senha, email, tipo_usuario]
        login = Controller.salvar_login(dados)
        tela_login.notify(login)
        if "ERRO" not in login:
            self.app.switch_screen("tela_inicial")
