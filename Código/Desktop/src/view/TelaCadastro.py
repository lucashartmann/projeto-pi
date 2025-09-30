from textual.widgets import Button, Static, Input, Select, Tab, Tabs, Header, Footer, SelectionList
from controller import Controller
from unidecode import unidecode
from textual.screen import Screen
from textual.containers import Grid, HorizontalGroup
from textual import on
from model import Init


class TelaCadastro(Screen):

    CSS_PATH = "css/TelaCadastro.tcss"

    montou = False
    valor_select = ""
    tabela = "products"
    montados = list()
    primeira_vez = True

    def compose(self):
        yield Header()
        yield Tabs(Tab("TelaCadastrar", id="tab_cadastrar"), Tab("TelaConsultar", id="tab_consultar"))
        with HorizontalGroup():
            yield SelectionList[str]()
            with Grid():
                yield Static("Name", classes="name")
                yield Input(placeholder="nome aqui", id="stt_nome", classes="name")
                yield Static("Regular_Price", classes="regular_price")
                yield Input(placeholder="preço aqui", classes="regular_price")
                yield Static("Description", classes="description")
                yield Input(placeholder="Descrição aqui", id="input_descricao", classes="description")
                yield Select([("Products", "Products"), ("Orders", "Orders"), ("Customers", "Customers"), ("Coupons", "Coupons")], allow_blank=False)
                yield Select([("Adicionar", "Adicionar"), ("Editar", "Editar"), ("Remover", "Remover")], allow_blank=False, id="select_operacoes")
                yield Button("Executar")
        yield Footer()

    contador = 0

    @on(SelectionList.SelectedChanged)
    def update_selected_view(self):
        lista_selecionados = self.query_one(SelectionList).selected

        for valor in self.montados:
            if valor not in lista_selecionados:
                self.montados.remove(valor)
                self.query(f".{valor}").remove()
            else:
                lista_selecionados.remove(valor)

        if len(lista_selecionados) > 0:
            for valor in lista_selecionados:
                if not self.query(f".{valor}"):
                    self.mount(Static(content=valor.capitalize(),
                            classes=valor), before=self.query_one(Select))
                    self.mount(Input(classes=valor), before=self.query_one(Select))
                    self.montados.append(valor)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_consultar", Tab).id:
            self.app.switch_screen("tela_consultar")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_cadastrar", Tab).id

    def on_select_changed(self, evento: Select.Changed):

        if evento.select.id != "select_operacoes":
            if not self.primeira_vez:
                self.montados = []

            match evento.select.value:

                case "Products":
                    self.tabela = "products"
                    self.query_one(SelectionList).clear_options()

                    self.query_one(SelectionList).add_options((name, name)
                                                              for name in list(Init.um_produto.__dict__.keys())[1:])
                    if self.primeira_vez:
                        self.montados = [
                            "name", "regular_price", "description"]
                        for valor in ["name", "regular_price", "description"]:
                            self.query_one(SelectionList).select(valor)
                        self.primeira_vez = False
                    else:
                        self.query_one(Grid).remove_children(Input)
                        self.query_one(Grid).remove_children(Static)

                case "Customers":
                    self.tabela = "customers"
                    self.query_one(SelectionList).clear_options()
                    self.query_one(Grid).remove_children(Input)
                    self.query_one(Grid).remove_children(Static)
                    self.query_one(SelectionList).add_options((name, name)
                                                              for name in list(Init.um_cliente.__dict__.keys())[1:])

                case "Coupons":
                    self.tabela = "coupons"
                    self.query_one(SelectionList).clear_options()
                    self.query_one(Grid).remove_children(Input)
                    self.query_one(Grid).remove_children(Static)
                    self.query_one(SelectionList).add_options((name, name)
                                                              for name in list(Init.um_cupom.__dict__.keys())[1:])

                case "Orders":
                    self.tabela = "orders"
                    self.query_one(SelectionList).clear_options()
                    self.query_one(Grid).remove_children(Input)
                    self.query_one(Grid).remove_children(Static)
                    self.query_one(SelectionList).add_options((name, name)
                                                              for name in list(Init.um_pedido.__dict__.keys())[1:])

        else:
            match evento.select.value:

                case "Editar":
                    if self.montou == False:
                        self.query_one(Grid).mount(Static("ID de pesquisa",
                                                          id="stt_id_pesquisa"), before=0)
                        self.query_one(Grid).mount(Input(placeholder="id do produto de pesquisa",
                                                         id="inpt_id_pesquisa"), before=1)
                        self.montou = True
                    else:
                        self.query_one(SelectionList).disabled = False
                    self.valor_select = "Editar"

                case "Adicionar":
                    self.valor_select = "Adicionar"
                    if self.montou:
                        self.query_one(SelectionList).disabled = False
                        self.query_one("#stt_id_pesquisa", Static).remove()
                        self.query_one("#inpt_id_pesquisa", Input).remove()
                        self.montou = False

                case "Remover":
                    if self.montou == False:
                        self.montados = []
                        self.query_one(Grid).remove_children(Static)
                        self.query_one(Grid).remove_children(Input)
                        self.query_one(SelectionList).disabled = True
                        self.query_one(Grid).mount(Static("ID de pesquisa",
                                                          id="stt_id_pesquisa"), before=0)
                        self.query_one(Grid).mount(Input(placeholder="id do produto de pesquisa",
                                                         id="inpt_id_pesquisa"), before=1)
                        self.montou = True
                    self.valor_select = "Remover"

    def limpar_inputs(self):
        for input in self.query(Input):
            input.value = ""

    def on_button_pressed(self):
        match self.valor_select:
            case "Editar":
                id_produto = self.query_one("#inpt_id_pesquisa", Input).value
                dados = dict()
                lista_chaves = [static for static in self.query_one(Grid).query(Static)[
                    1:-6]]
                lista_valores = [input for input in self.query_one(Grid).query(Input)[
                    1:]]

                for chave in lista_chaves:
                    string_limpa = unidecode(chave.content.split()[0].lower())
                    dados[string_limpa] = ""

                for i, valor in enumerate(lista_valores):
                    dados[list(dados.keys())[i]] = valor.value

                atualizacao = Controller.atualizar_item(
                    self.tabela, id_produto, dados)
                self.notify(atualizacao)
                self.limpar_inputs()

            case "Adicionar":
                dados = dict()
                lista_chaves = [static for static in self.query_one(Grid).query(Static)[
                    :-6]]
                lista_valores = [
                    input for input in self.query_one(Grid).query(Input)]

                for chave in lista_chaves:
                    string_limpa = unidecode(chave.content.split()[0].lower())
                    dados[string_limpa] = ""

                for i, valor in enumerate(lista_valores):
                    dados[list(dados.keys())[i]] = valor.value

                adicao = Controller.adicionar_item(self.tabela, dados)
                self.notify(adicao)
                self.limpar_inputs()

            case "Remover":
                id_produto = self.query_one(Input).value
                remocao = Controller.remover_item(self.tabela, id_produto)
                self.notify(remocao)
                self.limpar_inputs()
