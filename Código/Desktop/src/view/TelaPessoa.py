from textual.widgets import Input, Label, Button, TabbedContent, TabPane, Footer, Header, Select
from textual.screen import Screen
from textual.containers import Container
from controller import Controller
from Desktop.src.view.SQLITE import TelaPessoal
from textual import on


class TelaCadastrar(Container):

    valor_select = ""

    def compose(self):
        yield Label("ID da Pessoa:")
        yield Input(placeholder="ID aqui", id="input_id")
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
        yield Select([("Cliente", "Cliente"), ("Funcionario", "Funcionario")])
        yield Button("Limpar", id="bt_limpar")
        yield Button("Cadastrar", id="bt_cadastrar")
        yield Button("Voltar", id="bt_voltar")

    def cadastro(self):
        dados = []
        for input in self.query(Input)[1:]:
            dados.append(input.value.upper())
        dados.append(self.valor_select)
        resultado = Controller.cadastrar_pessoa(dados)
        self.notify(str(resultado), markup=False)

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_cadastrar":
                if self.valor_select:
                    self.cadastro()
                else:
                    self.notify("ERRO! Selecione um valor no select")
            case "bt_remover":
                if self.valor_select:
                    input_cpf = self.query_one("#input_cpf", Input).value
                    mensagem = Controller.remover_pessoa(
                        input_cpf, self.valor_select)
                    self.notify(str(mensagem), markup=False)
                else:
                    self.notify("ERRO! Selecione um valor no select")
            case "bt_editar":
                if self.valor_select:
                    input_cpf = self.query_one("#input_cpf", Input).value
                    dados = []
                    for input in self.query(Input)[1:]:
                        dados.append(input.value.upper())
                    dados.append(self.valor_select)
                    mensagem = Controller.editar_pessoa(input_cpf, dados)
                    self.notify(str(mensagem), markup=False)
                else:
                    self.notify("ERRO! Selecione um valor no select")

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        self.valor_select = str(evento.value)


class TelaPessoa(Screen):

    CSS_PATH = "css/TelaPessoa.tcss"

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
            with TabPane("Pessoas Cadastradas"):
                yield TelaPessoal.TelaPessoal()
        yield Footer()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_limpar":
                for input in self.query(Input):
                    input.value = ""
