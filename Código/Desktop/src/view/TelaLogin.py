from textual.screen import Screen
from textual.widgets import Input, Button, Select, Label
from textual import on
from textual.containers import VerticalGroup

from controller import Controller
from model import Init, Usuario



class Login(Screen):

    CSS_PATH = "css/TelaLogin.tcss"
    montou = False

    def compose(self):
        with VerticalGroup():
            yield Input(placeholder="Usuario")
            yield Input(placeholder="Senha")
            yield Select([("Cliente", "Cliente"), ("Gerente", "Gerente"), ("Funcionario", "Funcionario"), ("Administrador", "Administrador")], value="Cliente", allow_blank=False)
            yield Button("Entrar")
            yield Label("Não tem uma conta? [@click=app.cadastro]Cadastre-se[/]", id="bt_criar_conta")

    def on_button_pressed(self):
        nome = self.query(Input)[0].value
        senha = self.query(Input)[1].value
        tipo_usuario = self.query_one(Select).value
        Init.usuario = Usuario.Usuario(nome, senha, tipo_usuario)

        # match self.query_one(Select).value:
        #     case "Cliente":
        #         dados.append("Cliente")
        #     case "Gerente":
        #         dados.append("Gerente")
        #     case "Funcionario":
        #         dados.append("Funcionario")
        #     case "Administrador":
        #         dados.append("Administrador")

        # login = Controller.carregar_login(Init.usuario)
        # self.notify(login)
        # if "ERRO" not in login:
        self.app.switch_screen("tela_inicial")
