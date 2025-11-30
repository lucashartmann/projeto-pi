from textual.screen import Screen
from textual.widgets import Input, Button, Select, Label, Header, Footer, Switch
from textual.containers import VerticalGroup

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
            yield Input(placeholder="Usuário", id="input_username")
            yield MyInput(placeholder="Senha", password=True, id="input_senha")
            yield Select([("Cliente", "Cliente"), ("Corretor", "Corretor"), ("Captador", "Captador"), ("Administrador", "Administrador")], value="Cliente", allow_blank=False)
            yield Button("Entrar")
            yield Label("Não tem uma conta? [@click=app.cadastro]Cadastre-se[/]", id="bt_criar_conta")
            # yield Label("[@click=app.enviar_email]Esqueceu a senha?[/]", id="bt_esqueceu_senha")
        yield Footer(show_command_palette=False)

    def enviar_email(self):
        email = self.query("inpt_email").value.split()

    def voltar(self):
        self.query_one("#bt_esqueceu_senha").styles.display = "block"
        self.query_one(Select).styles.display = "block"
        self.query_one("#input_username").placeholder = "Usuário"
        self.query_one(Button).label = "Entrar"
        self.query_one("#inpt_email").remove()
        self.query_one("#bt_criar_conta").update(
            "Não tem uma conta? [@click=app.cadastro]Cadastre-se[/]")
        self.montou = False

    def montar_cadastro(self):
        self.query_one("#bt_esqueceu_senha").styles.display = "none"
        self.query_one(Select).styles.display = "none"
        self.query_one("#input_username").placeholder = "Username"
        self.mount(Input(placeholder="Email", id="inpt_email"),
                   before=self.query_one("#input_username"))
        self.montou = True
        self.query_one(Button).label = "Criar conta"
        self.query_one("#bt_criar_conta").update(
            "[@click=app.voltar]Voltar[/]")

    def on_button_pressed(self):

        username = self.query("#input_username").value.split()
        senha = self.query("#input_senha").value.split()
        tipo_usuario = self.query_one(Select).value
        login = ""

        if self.montou:
            email = self.query("inpt_email").value.split()
            login = Controller.salvar_login(username, senha, email)
        else:
            login = Controller.verificar_login(username, senha, tipo_usuario)

        self.notify(login)

        if "ERRO" not in login:
            if self.query_one(Select).value == "Cliente":
                self.app.switch_screen("tela_estoque_cliente")
            elif self.query_one(Select).value == "Corretor":
                self.app.switch_screen("tela_atendimento")
            elif self.query_one(Select).value == "Corretor":
                self.app.switch_screen("tela_dados_imovel")
            else:
                self.app.switch_screen("tela_cadastro_imovel")
