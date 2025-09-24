from textual.containers import HorizontalGroup
from textual.widgets import Button, Static, TextArea, Input, DataTable, Select, Tabs, Tab, Header, Footer, SelectionList
from api import API
from controller import Controller
from textual.screen import Screen
from model import Init
from textual import on


class TelaConsulta(Screen):

    CSS_PATH = "css/TelaConsulta.tcss"

    lista_produtos = []
    lista_produtos_filtrados = []
    tabela = "products"
    ROWS = []
    montados = list()
    primeira_vez = True

    def compose(self):
        yield Header()
        yield Tabs(Tab("TelaCadastrar", id="tab_cadastrar"), Tab("TelaConsultar", id="tab_consultar"))
        with HorizontalGroup():
            yield Select([("Products", "Products"), ("Orders", "Orders"), ("Customers", "Customers"), ("Coupons", "Coupons")], allow_blank=False)
            yield Input(placeholder="pesquise aqui")
            yield Button("Remover")
        yield TextArea(read_only=True)
        with HorizontalGroup():
            yield SelectionList[str]()
            yield DataTable()
        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_cadastrar", Tab).id:
            self.app.switch_screen("tela_cadastro")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_consultar", Tab).id
        self.atualizar()

    @on(SelectionList.SelectedChanged)
    def update_selected_view(self):
        lista_selecionados = self.query_one(SelectionList).selected

        for valor in self.montados:
            if valor not in lista_selecionados:
                self.montados.remove(valor)
            if valor in lista_selecionados:
                lista_selecionados.remove(valor)

        if len(lista_selecionados) > 0:
            for valor in lista_selecionados:
                self.montados.append(valor)

        self.atualizar()

    def on_button_pressed(self):
        id_produto = self.query_one(Input).value
        remocao = Controller.remover_item(self.tabela, id_produto)
        self.notify(remocao)
        self.atualizar()
        for input in self.query(Input):
            input.value = ""

    def on_select_changed(self, evento: Select.Changed):
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

            case "Customers":
                self.tabela = "customers"
                self.query_one(SelectionList).clear_options()
                self.query_one(SelectionList).add_options((name, name)
                                                          for name in list(Init.um_cliente.__dict__.keys())[1:])

            case "Coupons":
                self.tabela = "coupons"
                self.query_one(SelectionList).clear_options()
                self.query_one(SelectionList).add_options((name, name)
                                                          for name in list(Init.um_cupom.__dict__.keys())[1:])

            case "Orders":
                self.tabela = "orders"
                self.query_one(SelectionList).clear_options()
                self.query_one(SelectionList).add_options((name, name)
                                                          for name in list(Init.um_pedido.__dict__.keys())[1:])
        self.atualizar()

    def atualizar(self):
        if len(self.lista_produtos_filtrados) > 0:
            lista = self.lista_produtos_filtrados
        else:
            self.lista_produtos, _ = API.get_lista_itens(self.tabela)
            lista = self.lista_produtos

        quant = len(self.lista_produtos)

        self.query_one(
            TextArea).text = f"Exemplo de busca: 'name: camisa - blusa, id: 1' \n\nQuantidade de itens: {quant}"

        self.ROWS = []

        lista_chaves = []
        for produto in lista:
            for chave, dados in produto.items():
                if dados and (chave not in lista_chaves) and (chave in self.montados):
                    if isinstance(dados, dict):
                        dados = "".join(dados.values())
                        if not dados:
                            break
                    lista_chaves.append(chave)
        self.ROWS.append(lista_chaves)

        for produto in lista:
            lista = []
            for chave, valor in produto.items():
                if chave in self.ROWS[0]:
                    if "description" in chave:
                        if valor:
                            valor = " ".join(
                                " ".join(valor.split("<p>")).split("</p>"))
                    elif "price" in chave:
                        if valor:
                            valor = f"${valor}"
                    elif "date" in chave:
                        if valor:
                            valor = " ".join(valor.split("T"))
                    lista.append(valor)
            self.ROWS.append(lista)

        table = self.query_one(DataTable)
        table.clear(columns=True)

        table.add_columns(*self.ROWS[0])

        for row in self.ROWS[1:]:
            table.add_row(*row, height=3)

    def filtro(self, palavras, index, filtro_recebido):
        nova_lista = []

        if index + 1 < len(palavras):
            filtro = " ".join((palavras[index+1:]))

            if "," in filtro:
                filtro = filtro[0:filtro.index(
                    ",")]
            if "-" in filtro.split():
                for palavraa in filtro.split("-"):
                    if filtro.index("-")+1 < len(filtro) and palavraa not in nova_lista:
                        nova_lista.append(palavraa.strip())

            if len(self.lista_produtos_filtrados) > 0:
                produtos_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.lista_produtos_filtrados:
                            try:
                                if p in produto[filtro_recebido] and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                            except:
                                if p == produto[filtro_recebido] and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                else:
                    for produto in self.lista_produtos_filtrados:
                        try:
                            if filtro in produto[filtro_recebido] and produto not in produtos_temp:
                                produtos_temp.append(produto)
                        except:
                            if filtro == produto[filtro_recebido] and produto not in produtos_temp:
                                produtos_temp.append(produto)

                if len(produtos_temp) > 0:
                    self.lista_produtos_filtrados = produtos_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.lista_produtos:
                            try:
                                if p in produto[filtro_recebido] and produto not in self.lista_produtos_filtrados:
                                    self.lista_produtos_filtrados.append(
                                        produto)
                            except:
                                if p == produto[filtro_recebido] and produto not in self.lista_produtos_filtrados:
                                    self.lista_produtos_filtrados.append(
                                        produto)

                else:
                    for produto in self.lista_produtos:
                        try:
                            if filtro in produto[filtro_recebido] and produto not in self.lista_produtos_filtrados:
                                self.lista_produtos_filtrados.append(produto)
                        except:
                            if filtro == produto[filtro_recebido] and produto not in self.lista_produtos_filtrados:
                                self.lista_produtos_filtrados.append(produto)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value
        palavras = texto.split()

        if len(palavras) > 0:
            self.lista_produtos_filtrados = []
            for palavra in palavras:
                if palavra.lower() in self.montados:
                    index = palavras.index(palavra)
                    self.filtro(palavras, index, palavra[:-1].lower())
                    self.atualizar()
        else:
            self.atualizar()
