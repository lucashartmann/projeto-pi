from textual.widgets import Input, Label, Pretty, Button, TabbedContent, TabPane, Footer, Header
from textual.screen import Screen
from textual.containers import Container
from controller.Controller import Controller
from model import Init


class TelaCadastrar(Container):
    def compose(self):

        yield Label("Nome:")
        yield Input(placeholder="Nome aqui")
        yield Label("CPF:")
        yield Input(placeholder="CPF aqui")
        yield Label("RG:")
        yield Input(placeholder="RG aqui")
        yield Label("Telefone:")
        yield Input(placeholder="Telefone aqui")
        yield Label("Endereço:")
        yield Input(placeholder="Endereço aqui")
        yield Label("Email:")
        yield Input(placeholder="Email aqui")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Cadastrar", id="bt_cadastrar")
        yield Button("Voltar", id="bt_voltar")

    def cadastro(self):
        dados = []
        for input in self.query(Input):
            if input.value == "":
                self.notify(f"{input.placeholder} está vazio, tente novamente")
                return
            dados.append(input.value.upper())
        resultado = Controller.cadastrar_cliente(dados)
        self.notify(resultado)

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_cadastrar":
                self.cadastro()


class TelaRemover(Container):
    def compose(self):
        yield Label("ID do Cliente:")
        yield Input(placeholder="ID aqui", id="input_id")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Remover", id="bt_remover")
        yield Button("Voltar", id="bt_voltar")

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_remover":
                input_cpf = self.query_one("#input_cpf").value
                if len(input_cpf) == 11:
                    cliente = Init.loja.get_cliente_por_cpf(input_cpf)
                    if not cliente:
                        self.notify(
                            f"Cliente com CPF {input_cpf} não encontrado")
                    else:
                        mensagem = Controller.remover_cliente(
                            Controller, cliente)
                        self.notify(mensagem)
                else:
                    self.notify("CPF precisa ter 11 digitos")


class TelaEditar(Container):

    def compose(self):
        yield Label("ID do Cliente:")
        yield Input(placeholder="ID aqui", id="input_id")
        yield Label("Nome:")
        yield Input(placeholder="Nome aqui")
        yield Label("CPF:")
        yield Input(placeholder="CPF aqui", id="input_cpf")
        yield Label("RG:")
        yield Input(placeholder="RG aqui")
        yield Label("Telefone:")
        yield Input(placeholder="Telefone aqui")
        yield Label("Endereço:")
        yield Input(placeholder="Endereço aqui")
        yield Label("Email:")
        yield Input(placeholder="Email aqui")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Editar", id="bt_editar")
        yield Button("Voltar", id="bt_voltar")

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_editar":
                input_cpf = self.query_one("#input_cpf").value
                if len(input_cpf) == 11:
                    cliente = Init.loja.get_cliente_por_cpf(input_cpf)
                    if not cliente:
                        self.notify(
                            f"Cliente com CPF {input_cpf} não encontrado")
                    else:
                        dados = []
                        for input in self.query(Input)[1:]:
                            dados.append(input.value.upper())
                        mensagem = Controller.editar_cliente(
                            Controller, cliente, dados)
                        self.notify(mensagem)
                else:
                    self.notify("CPF precisa ter 11 digitos")


class TelaCliente(Screen):

    CSS_PATH = "css/TelaCliente.tcss"

    def compose(self):
        yield Header()
        with TabbedContent():
            with TabPane("Cadastrar"):
                yield TelaCadastrar()
            with TabPane("Editar"):
                yield TelaEditar()
            with TabPane("Remover"):
                yield TelaRemover()
        yield Footer()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_limpar":
                for input in self.query(Input):
                    input.value = ""
