from textual.widgets import Input, Label, Button, TabbedContent, TabPane, Footer, Header
from textual.screen import Screen
from textual.containers import Container
from controller import Controller


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
            dados.append(input.value.upper())
        resultado = Controller.cadastrar_cliente(dados)
        self.notify(str(resultado), markup=False)

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
                input_cpf = self.query_one("#input_cpf", Input).value
                mensagem = Controller.remover_cliente(input_cpf)
                self.notify(str(mensagem), markup=False)


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
                input_cpf = self.query_one("#input_cpf", Input).value
                dados = []
                for input in self.query(Input)[1:]:
                    dados.append(input.value.upper())
                mensagem = Controller.editar_cliente(input_cpf, dados)
                self.notify(str(mensagem), markup=False)


class TelaCliente(Screen):

    CSS_PATH = "css/TelaCliente.tcss"

    # def montar(self):
    #     lero = HorizontalGroup()
    #     self.mount(lero)
    #     lero1 = HorizontalGroup()
    #     self.mount(lero1)
    #     lero2 = HorizontalGroup()
    #     self.mount(lero2)

    #     lero.mount(Label("Nome:"))
    #     lero.mount(Input(placeholder="Nome aqui"))
    #     lero.mount(Label("CPF:"))
    #     lero.mount(Input(placeholder="CPF aqui"))

    #     lero1.mount(Label("RG:"))
    #     lero1.mount(Input(placeholder="RG aqui"))
    #     lero1.mount(Label("Telefone:"))
    #     lero1.mount(Input(placeholder="Telefone aqui"))

    #     lero2.mount(Label("Endereço:"))
    #     lero2.mount(Input(placeholder="Endereço aqui"))
    #     lero2.mount(Label("Email:"))
    #     lero2.mount(Input(placeholder="Email aqui"))

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
