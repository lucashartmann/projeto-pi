from textual.widgets import Input, TextArea, Button, DataTable, Footer, Header, Tab, Tabs
from textual.containers import HorizontalGroup, HorizontalScroll
from textual import on
from textual.screen import Screen
from model import Init, Produto


class TelaEstoque(Screen):

    produtos = Init.loja.get_estoque().get_lista_produtos()
    produtos_filtrados = []
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    ROWS = []

    def compose(self):
        yield Header()
        # TODO
        yield Tabs(Tab("TelaPerfil", id="tab_perfil"), Tab("TelaCadastrar", id="tab_cadastrar"), Tab("TelaConsultar", id="tab_consultar"))
        with HorizontalGroup(id="hg_pesquisa"):
            yield Input()
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        yield DataTable()
        yield Footer()

    def setup_dados(self):
        if len(self.produtos_filtrados) > 0:
            quant = len(self.produtos_filtrados)
        else:
            quant = len(self.produtos)
        self.query_one(TextArea).text = f"Quantidade de produtos: {quant}"

    def on_button_pressed(self):
        self.screen.app.switch_screen("tela_inicial")

    def atualizar_lista(self):
        self.produtos = Init.loja.get_estoque().get_produtos()

    def on_mount(self):
        self.ROWS = list(Produto.Produto.__dict__.keys())

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        # TODO
        if event.tabs.active == self.query_one("#tab_consultar", Tab).id:
            self.app.switch_screen("tela_consultar")
        elif event.tabs.active == self.query_one("#tab_perfil", Tab).id:
            self.app.switch_screen("tela_perfil")

    def on_screen_resume(self):
        # TODO
        self.query_one(Tabs).active = self.query_one("#tab_cadastrar", Tab).id

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

    def atualizar(self):
        if len(self.produtos_filtrados) > 0:
            lista = self.produtos_filtrados
        else:

            lista = self.produtos

        for produto in lista:
            lista = []
            for valor in produto.__dict__.values():
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

            if len(self.produtos_filtrados) > 0:
                produtos_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.produtos_filtrados:
                            try:
                                if p in produto[filtro_recebido] and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                            except:
                                if p == produto[filtro_recebido] and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                else:
                    for produto in self.produtos_filtrados:
                        try:
                            if filtro in produto[filtro_recebido] and produto not in produtos_temp:
                                produtos_temp.append(produto)
                        except:
                            if filtro == produto[filtro_recebido] and produto not in produtos_temp:
                                produtos_temp.append(produto)

                if len(produtos_temp) > 0:
                    self.produtos_filtrados = produtos_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.produtos:
                            try:
                                if p in produto[filtro_recebido] and produto not in self.produtos_filtrados:
                                    self.produtos_filtrados.append(
                                        produto)
                            except:
                                if p == produto[filtro_recebido] and produto not in self.produtos_filtrados:
                                    self.produtos_filtrados.append(
                                        produto)

                else:
                    for produto in self.produtos:
                        try:
                            if filtro in produto[filtro_recebido] and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)
                        except:
                            if filtro == produto[filtro_recebido] and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)
