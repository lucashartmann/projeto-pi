from textual.widgets import Input, Label, Button, Footer, Header
from textual.screen import Screen
from textual.containers import HorizontalGroup
from controller.Controller import Controller


class TelaCliente(Screen):

    CSS_PATH = "css/TelaCliente.tcss"

    def compose(self):
        yield Header()
        with HorizontalGroup():
            yield Label("Nome:")
            yield Input(placeholder="Nome aqui")
        with HorizontalGroup():
            yield Label("CPF:")
            yield Input(placeholder="CPF aqui")
        with HorizontalGroup():
            yield Label("RG:")
            yield Input(placeholder="RG aqui")
        with HorizontalGroup():
            yield Label("Telefone:")
            yield Input(placeholder="Telefone aqui")
        with HorizontalGroup():
            yield Label("Endereço:")
            yield Input(placeholder="Endereço aqui")
        with HorizontalGroup():
            yield Label("Email:")
            yield Input(placeholder="Email aqui")
        yield Button("Cadastrar")
        yield Button("Voltar", id="bt_voltar")
        yield Footer()
        
    def on_button_pressed(self):
        self.screen.app.switch_screen("tela_inicial")

    def cadastro(self):
        dados = []
        for input in self.query(Input):
            dados.append(input.value)
        resultado = Controller.cadastrar_cliente(
            dados[0], dados[1], dados[2], dados[3], dados[4], dados[5])
        self.notify(resultado)
