from textual.containers import HorizontalGroup, Horizontal, VerticalScroll
from textual.widgets import Button, TextArea, Input, DataTable, Select, Tabs, Tab, Header, Footer, SelectionList
from api import Wocommerce
from controller import Controller
from textual.screen import Screen
from model import Init
from textual import on
from database import Shelve


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
        yield Tabs(Tab("TelaPerfil", id="tab_perfil"), Tab("TelaCadastrar", id="tab_cadastrar"), Tab("TelaConsultar", id="tab_consultar"))
        with HorizontalGroup():
            yield Input(placeholder="pesquise aqui")
            yield Button("Remover")
        yield TextArea(read_only=True)
        with Horizontal():
            with VerticalScroll(id="v_left"):
                yield Select([("Complex", "Complex")], allow_blank=False, id="select_perfil")
                yield Select([("Products", "Products"), ("Orders", "Orders"), ("Customers", "Customers"), ("Coupons", "Coupons"), ("Taxes", "Taxes")], allow_blank=False, id="select_tabelas")
                yield SelectionList[str]()
            yield DataTable()
        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_cadastrar", Tab).id:
            self.app.switch_screen("tela_cadastro")
        elif event.tabs.active == self.query_one("#tab_perfil", Tab).id:
            self.app.switch_screen("tela_perfil")

    def on_mount(self):
        self.atualizar()

    def on_screen_resume(self):
        perfis = Shelve.carregar("perfis.db", "perfis") or {}
        if perfis:
            lista = list((chave, chave) for chave in perfis.keys())
            lista.append(("Complex", "Complex"))
            self.query_one("#select_perfil", Select).set_options(lista)
            print(perfis)
            self.perfis = perfis
        else:

            self.query_one("#select_perfil", Select).set_options(
                [("Complex", "Complex")])
        self.query_one(Tabs).active = self.query_one("#tab_consultar", Tab).id

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

    def limpar_nome(self, name):
        if "__" in name:
            return name.split("__", 1)[1]
        return name.lstrip("_")

    def atualizar2(self):
        self.query_one(SelectionList).clear_options()
        if self.perfil_atual == "Complex":
            self.query_one(SelectionList).add_options((self.limpar_nome(name), self.limpar_nome(name))
                                                      for name in list(Init.dict_objetos[self.tabela].__dict__.keys()))
        else:
            dicionario = self.perfis[self.perfil_atual]
            self.query_one(SelectionList).add_options((name, name)
                                                      for name in dicionario[self.tabela])

        self.atualizar()

    def on_select_changed(self, evento: Select.Changed):
        if evento.select.id == "select_tabelas":
            self.tabela = evento.select.value.lower()

        elif evento.select.id == "select_perfil":
            self.perfil_atual = evento.select.value
            if self.perfil_atual == "Complex":
                self.query_one("#select_tabelas", Select).set_options([("Products", "Products"), (
                    "Orders", "Orders"), ("Customers", "Customers"), ("Coupons", "Coupons"), ("Taxes", "Taxes")])
            else:
                dicionario = self.perfis[self.perfil_atual]
                self.query_one("#select_tabelas", Select).set_options(
                    (tabela.cWoocommercetalize(), tabela.cWoocommercetalize()) for tabela in dicionario["tabelas"])
            self.atualizar2()

    def atualizar(self):
        if len(self.lista_produtos_filtrados) > 0:
            lista = self.lista_produtos_filtrados
        else:
            self.lista_produtos, _ = Wocommerce.get_lista_itens(self.tabela)
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
                if palavra[:-1].lower() in self.montados:
                    index = palavras.index(palavra)
                    self.filtro(palavras, index, palavra[:-1].lower())
                    self.atualizar()
        else:
            self.atualizar()
