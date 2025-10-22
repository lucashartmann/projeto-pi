from textual.screen import Screen
from textual.widgets import Input, Button, Select
from textual import on
from controller import Controller
from database import Banco
from model import Init

class TelaLogin(Screen):

    CSS_PATH = "css/TelaLogin.tcss"
    montou = False

    def compose(self):
        yield Input(placeholder="Usuario")
        yield Input(placeholder="Senha")
        yield Select([("Cliente", "Cliente"), ("Gerente", "Gerente"), ("Funcionario", "Funcionario"), ("Administrador", "Administrador")], value="Cliente", allow_blank=False)
        yield Button("Entrar")

    def on_button_pressed(self):
        nome = self.query_one(Input).value
        senha = self.query_all(Input)[1].value
        tipo_usuario = self.query_one(Select).value
        Init.tipo_usuario = Usuario
        
        match self.query_one(Select).value:
            case "Cliente":
                dados.append("Cliente")
            case "Gerente":
                dados.append("Gerente")
            case "Funcionario":
                dados.append("Funcionario")
            case "Administrador":
                dados.append("Administrador")
        login = Controller.salvar_login(dados)
        self.notify(login)
        if "ERRO" not in login:
            self.app.switch_screen("tela_cadastro")

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        valor_select = str(evento.value)


        
