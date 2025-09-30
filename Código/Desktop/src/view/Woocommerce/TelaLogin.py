from textual.screen import Screen
from textual.widgets import Input, Button, Select
from textual import on
from controller import Controller


class Login(Screen):

    CSS_PATH = "css/TelaLogin.tcss"
    montou = False

    def compose(self):
        yield Select([("WoocommerceAPI", "WoocommerceAPI"), ("MYSQL", "MYSQL")], value="WoocommerceAPI", allow_blank=False)
        yield Input(placeholder="url")
        yield Input(placeholder="consumer_key")
        yield Input(placeholder="cosumer_secret")
        yield Button("Entrar")

    def on_button_pressed(self):
        dados = []
        for input in self.query(Input):
            dados.append(input.value)
        login = Controller.salvar_login(dados)
        self.notify(login)
        if "ERRO!" not in login:
            self.app.switch_screen("tela_cadastro")

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        valor_select = str(evento.value)

        lista_inputs = self.query(Input)

        if valor_select == "SQLITE":
            lista_inputs[0].placeholder = "host"
            lista_inputs[1].placeholder = "user"
            lista_inputs[2].placeholder = "password"
            self.mount(Input(placeholder="database", id="input_database"))

            lista_inputs = self.query(Input)

            lista_valores = []

            for input in lista_inputs:
                lista_valores.append(input.value)

            self.montou = True

            # Shelve.salvar("dados.db", "login", lista_valores)

        else:
            if self.montou:
                self.query_one("#input_database", Input).remove()
                lista_inputs = self.query(Input)
                lista_inputs[0].placeholder = "url"
                lista_inputs[1].placeholder = "consumer_key"
                lista_inputs[2].placeholder = "cosumer_secret"
                self.montou = False
