from textual.screen import Screen
from textual.widgets import Input, Button, Select, Label
from textual.containers import VerticalGroup
from textual.events import Click

from textual_image.widget import Image
from textual_image.widget.sixel import _ImageSixelImpl


from model.Usuario import TipoUsuario
from model import Init


class MyInput(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Image("assets/olho_fechado.png")

    def on_mount(self):
        self.query_one(Image).styles.dock = "right"

    def on_click(self, evento: Click):
        if isinstance(evento.widget, _ImageSixelImpl):

            if self.password:
                self.password = False
                self.query_one(Image).image = "assets/olho_aberto.png"

            else:
                self.password = True
                self.query_one(Image).image = "assets/olho_fechado.png"


class TelaLogin(Screen):

    CSS_PATH = "css/TelaLogin.tcss"
    montou = False

    def compose(self):
        with VerticalGroup():
            yield Input(placeholder="Usuário")
            yield MyInput(placeholder="Senha", password=True)
            yield Select([("Cliente", "Cliente"), ("Gerente", "Gerente"), ("Funcionario", "Funcionario"), ("Administrador", "Administrador")], value="Cliente", allow_blank=False)
            yield Button("Entrar")
            yield Label("Não tem uma conta? [@click=app.cadastro]Cadastre-se[/]", id="bt_criar_conta")

    def montar_cadastro(self):
        self.query_one(Select).disabled = True
        self.query_one(Input).placeholder = "Username"
        self.mount(Input(placeholder="Email"), before=self.query_one(Input))
        self.query_one(Label).display = "none"
        self.montou = True
        self.query_one(Button).label = "Criar conta"

    def on_button_pressed(self):

        # nome = self.query(Input)[0].value
        # senha = self.query(Input)[1].value
        # tipo_usuario = ""

        # match self.query_one(Select).value:
        #     case "Cliente":
        #         tipo_usuario = TipoUsuario.CLIENTE
        #     case "Gerente":
        #         tipo_usuario = TipoUsuario.GERENTE
        #     case "Funcionario":
        #         tipo_usuario = TipoUsuario.FUNCIONARIO
        #     case "Administrador":
        #         tipo_usuario = TipoUsuario.ADMINISTRADOR

        # if self.montou:
        #     email = self.query(Input)[0].value
        #     dados = [nome, senha, email, TipoUsuario.CLIENTE]
        # else:
        #     dados = [nome, senha, tipo_usuario]

        # login = Controller.verificar_login(dados)
        # self.notify(login)
        # if "ERRO" not in login:
        #     if self.montou:
        #         Init.cliente_atual = Cliente.Cliente(
        #             nome, "", "", "", "", email)
        #     elif tipo_usuario == TipoUsuario.CLIENTE:
        #         # TODO: Arrumar. Podemos não ter o email
        #         consulta = Init.loja.get_cliente_por_email(email)
        #         if consulta:
        #             Init.cliente_atual = consulta
        #         else:
        #             if email:
        #                 Init.cliente_atual = Cliente.Cliente(
        #                     "", "", "", "", "", email)
        #             else:
        #                 Init.cliente_atual = Cliente.Cliente(
        #                     "", "", "", "", "", "")

        match self.query_one(Select).value: # Todo: Isso é só para testes, remover depois
            case "Cliente":
                Init.usuario.set_tipo(TipoUsuario.CLIENTE)
            case "Gerente":
                Init.usuario.set_tipo(TipoUsuario.GERENTE)
            case "Funcionario":
                Init.usuario.set_tipo(TipoUsuario.FUNCIONARIO)
            case "Administrador":
                Init.usuario.set_tipo(TipoUsuario.ADMINISTRADOR)

        if Init.usuario.get_tipo() == TipoUsuario.CLIENTE:
            self.app.switch_screen("tela_estoque_cliente")
        else:
            self.app.switch_screen("tela_cadastro")
