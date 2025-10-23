from textual.app import App
from textual.widgets import Input, Label, Button, Select

from model import Init, Usuario
from view import TelaClientela, TelaInicial, TelaPessoa, TelaProduto, TelaLogin, TelaEstoque
from controller import Controller

class App(App):

    SCREENS = {
        "tela_inicial": TelaInicial.ScreenInicial,
        "tela_pessoa": TelaPessoa.TelaPessoa,
        "tela_produto": TelaProduto.TelaProduto,
        "tela_login": TelaLogin.TelaLogin,
        "tela_estoque": TelaEstoque.TelaEstoque,
        "tela_clientela": TelaClientela.TelaClientela
    }

    def on_mount(self):
        self.push_screen("tela_login")
        
    def action_cadastro(self):
        email = self.query(Input)[0].value
        nome = self.query(Input)[1].value
        senha = self.query(Input)[2].value
        tipo_usuario = self.query_one(Select).value
        
        tela_login = self.get_screen("tela_login")
        tela_login.query_one(Input).placeholder = "Username"
        tela_login.mount(Input(placeholder="Email"), before=tela_login.query_one(Input))
        tela_login.query_one(Label).display = "none"
        tela_login.query_one(Button).label = "Criar conta"
        Init.usuario = Usuario.Usuario(nome, senha, email, tipo_usuario)
        login = Controller.carregar_login(Init.usuario)
        tela_login.notify(login)
        if "ERRO" not in login:
            self.app.switch_screen("tela_inicial")
