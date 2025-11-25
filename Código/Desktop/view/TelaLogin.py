from textual.screen import Screen
from textual.widgets import Input, Button, Select, Label, Header, Footer, Switch
from textual.containers import VerticalGroup
from textual.app import SystemCommand

from model import Init
from controller import Controller


class MyInput(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Switch()

    def on_mount(self):
        self.query_one(Switch).styles.dock = "right"

    def on_switch_changed(self, evento: Switch.Changed):
        if evento.switch.value == True:
            self.password = False
        else:
            self.password = True


class TelaLogin(Screen):

    CSS_PATH = "css/TelaLogin.tcss"
    montou = False
    TITLE = "Login"
   
    def compose(self):
        yield Header()
        with VerticalGroup():
            yield Input(placeholder="Usuário")
            yield MyInput(placeholder="Senha", password=True)
            yield Select([("Cliente", "Cliente"), ("Corretor", "Corretor"), ("Captador", "Captador"), ("Administrador", "Administrador")], value="Cliente", allow_blank=False)
            yield Button("Entrar")
            yield Label("Não tem uma conta? [@click=app.cadastro]Cadastre-se[/]", id="bt_criar_conta")
        yield Footer(show_command_palette=False)

    def voltar(self):
        self.query_one(Select).styles.display = "block"
        self.query_one(Input).placeholder = "Usuário"
        self.query_one(Button).label = "Entrar"
        self.query_one("#inpt_email").remove()
        self.query_one(Label).update(
            "Não tem uma conta? [@click=app.cadastro]Cadastre-se[/]")
        self.montou = False

    def montar_cadastro(self):
        self.query_one(Select).styles.display = "none"
        self.query_one(Input).placeholder = "Username"
        self.mount(Input(placeholder="Email", id="inpt_email"),
                   before=self.query_one(Input))
        self.montou = True
        self.query_one(Button).label = "Criar conta"
        self.query_one(Label).update("[@click=app.voltar]Voltar[/]")

    def on_button_pressed(self):

        nome = self.query(Input)[0].value
        senha = self.query(Input)[1].value
        tipo_usuario = ""
        dados = [nome, senha, tipo_usuario]
        if self.montou:
            email = self.query(Input)[0].value
            dados.append(email)
            Controller.salvar_login(dados)

        # Todo: Isso é só para testes, remover depois
        match self.query_one(Select).value:
            case "Cliente":
                Init.usuario_atual = Init.comprador
            case "Corretor":
                Init.usuario_atual = Init.corretor
            case "Captador":
                Init.usuario_atual = Init.captador
            case "Administrador":
                Init.usuario_atual = Init.administrador

            # login = Controller.verificar_login(dados)
            # self.notify(login)
            # if "ERRO" not in login:

            # Init.imobiliaria.cadastrar(Init.usuario_atual)

        if self.query_one(Select).value == "Cliente":
            self.app.switch_screen("tela_estoque_cliente")
        else:
            self.app.switch_screen("tela_cadastro_imovel")
