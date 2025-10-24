from textual.widgets import Input, Label, Button, Tab, Tabs, Select
from textual.screen import Screen
from textual.containers import Grid, HorizontalGroup
from textual import on

from controller import Controller


class TelaPessoa(Screen):

    CSS_PATH = "css/TelaPessoa.tcss"

    valor_select = ""

    def compose(self):
        yield Tabs(Tab("Cadastro", id="tab_cadastrar"), Tab("Consulta", id="tab_consultar"))
        with Grid():
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
        with HorizontalGroup():
            yield Button("Limpar", id="bt_limpar")
            yield Button("Cadastrar", id="bt_cadastrar")
            yield Button("Voltar", id="bt_voltar")

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_consultar", Tab).id:
            self.app.switch_screen("tela_clientela")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_cadastrar", Tab).id

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
