from textual.widgets import Input, TextArea, Button, DataTable, Footer, Header, Tab, Tabs, Select, SelectionList
from textual.containers import HorizontalGroup, VerticalScroll, Horizontal
from textual import on
from textual.screen import Screen

from model import Init
from model.Usuario import TipoUsuario
from model import Init

from controller import Controller


class TelaEstoque(Screen):

    CSS_PATH = "css/TelaEstoque.tcss"

    produtos = Init.loja.get_estoque().get_lista_produtos()
    produtos_filtrados = []
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    ROWS = []

    def compose(self):
        yield Header()
        if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:

            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"))
        elif Init.usuario.get_tipo() == TipoUsuario.GERENTE:
            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"), Tab("Dados da Loja", id="tab_dados_loja"))
        else:
            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"))

        with HorizontalGroup(id="hg_pesquisa"):
            yield Input(placeholder="pesquise aqui")
            yield Button("Remover")
        yield TextArea(read_only=True)
        with Horizontal():
            with VerticalScroll(id="v_left"):
                yield Select([("Produtos", "Produtos"), ("Pedidos", "Pedidos"), ("Clientes", "Clientes"), ("Cupons", "Cupons"), ("Impostos", "Impostos")], allow_blank=False, id="select_tabelas")
                yield SelectionList[str]()
            yield DataTable()
        yield Footer()

    def setup_dados(self):
        if len(self.produtos_filtrados) > 0:
            quant = len(self.produtos_filtrados)
        else:
            quant = len(self.produtos)
        self.query_one(TextArea).text = f"Quantidade de produtos: {quant}"

    def on_button_pressed(self):
        id_produto = self.query_one(Input).value
        # TODO: arrumar
        # remocao = Controller.remover_item(self.tabela, id_produto)
        # self.notify(remocao)
        self.atualizar()
        for input in self.query(Input):
            input.value = ""

    def atualizar_lista(self):
        self.produtos = Init.loja.get_estoque().get_produtos()

    def on_select_changed(self, evento: Select.Changed):
        if evento.select.id == "select_tabelas":
            self.tabela = evento.select.value.lower()


    def on_mount(self):
        self.ROWS = [list(Init.um_produto.__dict__.keys())]
        self.atualizar()
        self.setup_dados()

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

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
            self.app.switch_screen("tela_estoque")
        elif event.tabs.active == self.query_one("#tab_cadastro", Tab).id:
            self.app.switch_screen("tela_cadastro")
        if Init.usuario.get_tipo() == TipoUsuario.GERENTE:
            if event.tabs.active == self.query_one("#tab_dados_loja", Tab).id:
                self.app.switch_screen("tela_dados_loja")
        if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:
            if event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                self.app.switch_screen("tela_servidor")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_estoque", Tab).id

    def atualizar(self):
        self.ROWS = [self.ROWS[0]]

        table = self.query_one(DataTable)
        table.clear(columns=True)

        if len(self.produtos_filtrados) > 0:
            lista_atual = self.produtos_filtrados
        else:
            self.produtos = Init.loja.get_estoque().get_lista_produtos()
            lista_atual = self.produtos

        for produto in lista_atual:
            lista = []
            for valor in produto.__dict__.values():
                lista.append(valor)
            self.ROWS.append(lista)

        table.add_columns(*self.ROWS[0])

        for row in self.ROWS[1:]:
            table.add_row(*row, height=3)

        self.setup_dados()

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value
        palavras = texto.split()

        if len(palavras) > 0:
            self.produtos_filtrados = []
            for palavra in palavras:
                if palavra[:-1].lower() in self.ROWS[0]:
                    index = palavras.index(palavra)
                    self.filtro(palavras, index, palavra[:-1].lower())
                    self.atualizar()
        else:
            self.atualizar()

    def filtro(self, palavras, index, filtro_recebido):
        nova_lista = []
        campo = f"get_{filtro_recebido}"

        if index + 1 < len(palavras):
            filtro = " ".join((palavras[index+1:]))

            if "," in filtro:
                filtro = filtro[0:filtro.index(
                    ",")]
            if "-" in filtro.split():
                for palavraa in filtro.split("-"):
                    if filtro.index("-")+1 < len(filtro) and palavraa not in nova_lista:
                        nova_lista.append(palavraa.strip())

            if len(self.produtos_filtrados) > 0:
                produtos_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.produtos_filtrados:
                            try:
                                if p in getattr(produto, campo)() and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                            except:
                                if p == getattr(produto, campo)() and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                else:
                    for produto in self.produtos_filtrados:
                        try:
                            if filtro in getattr(produto, campo)() and produto not in produtos_temp:
                                produtos_temp.append(produto)
                        except:
                            if filtro == getattr(produto, campo)() and produto not in produtos_temp:
                                produtos_temp.append(produto)

                if len(produtos_temp) > 0:
                    self.produtos_filtrados = produtos_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.produtos:
                            try:
                                if p in getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                    self.produtos_filtrados.append(
                                        produto)
                            except:
                                if p == getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                    self.produtos_filtrados.append(
                                        produto)

                else:
                    for produto in self.produtos:
                        try:
                            if filtro in getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)
                        except:
                            if filtro == getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)
