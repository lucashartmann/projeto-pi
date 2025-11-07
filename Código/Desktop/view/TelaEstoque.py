from textual.widgets import Input, TextArea, Button, DataTable, Footer, Header, Tab, Tabs, Select, SelectionList
from textual.containers import HorizontalGroup, VerticalScroll, Horizontal
from textual import on
from textual.screen import Screen

from model import Init

from controller import Controller
from model import Init, Cliente, Corretor, Captador


class TelaEstoque(Screen):

    CSS_PATH = "css/TelaEstoque.tcss"

    imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()
    imoveis_filtrados = []
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    ROWS = []

    def is_admin(self):
        if not isinstance(Init.usuario_atual, Cliente.Comprador) and not isinstance(Init.usuario_atual, Cliente.Proprietario) and not isinstance(Init.usuario_atual, Captador.Captador) and not isinstance(Init.usuario_atual, Corretor.Corretor):
            return True
        return False

    def compose(self):
        yield Header()
        if self.is_admin:

            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"))
        elif isinstance(Init.usuario_atual, Corretor.Corretor):
            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))
        else:
            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"))

        with HorizontalGroup(id="hg_pesquisa"):
            yield Input(placeholder="pesquise aqui")
            yield Button("Remover")
        yield TextArea(read_only=True)
        with Horizontal():
            with VerticalScroll(id="v_left"):
                yield Select([("Imoveis", "Imovel"), ("Compradores", "Comprador"), ("Proprietários", "Proprietario"), ("Corretores", "Corretor"), ("Captadores", "Captador"), ("Vendas", "Venda"), ("Alugueis", "Aluguel")], allow_blank=False, id="select_tabelas")
                yield SelectionList[str]()
            yield DataTable()
        yield Footer()

    def setup_dados(self):
        if len(self.imoveis_filtrados) > 0:
            quant = len(self.imoveis_filtrados)
        else:
            quant = len(self.imoveis)
        self.query_one(TextArea).text = f"Quantidade de imoveis: {quant}"

    def on_button_pressed(self):
        codigo = self.query_one(Input).value

        match self.tabela:
            case "Imovel":
                remocao = Controller.remover_imovel(codigo)
            case "Comprador":
                remocao = Controller.remover_comprador(codigo)
            case "Proprietario":
                remocao = Controller.remover_proprietario(codigo)
            case "Corretor":
                remocao = Controller.remover_corretor(codigo)
            case "Captador":
                remocao = Controller.remover_captador(codigo)
            case "Aluguel" | "venda":
                remocao = Controller.remover_venda_aluguel(codigo)
                
        self.notify(remocao)
        
        if "ERRO" not in remocao:
            self.atualizar()
            for input in self.query(Input):
                input.value = ""

    def on_select_changed(self, evento: Select.Changed):
        if evento.select.id == "select_tabelas":
            self.tabela = evento.select.value.lower()

            match evento.value:
                case "Imovel":
                    self.ROWS = [list(Init.um_imovel.__dict__.keys())]
                    self.imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()
                case  "Comprador":
                    self.ROWS = [list(Init.comprador.__dict__.keys())]
                    Init.imobiliaria.get_estoque().get_lista_imoveis()
                case "Proprietario":
                    self.ROWS = [list(Init.proprietario.__dict__.keys())]
                    Init.imobiliaria.get_estoque().get_lista_imoveis()
                case "Corretor":
                    self.ROWS = [list(Init.corretor.__dict__.keys())]
                    Init.imobiliaria.get_estoque().get_lista_imoveis()
                case "Captador":
                    self.ROWS = [list(Init.captador.__dict__.keys())]
                    Init.imobiliaria.get_estoque().get_lista_imoveis()
                case "Venda":
                    self.ROWS = [list(Init.uma_venda_aluguel.__dict__.keys())]
                    Init.imobiliaria.get_estoque().get_lista_imoveis()
                case "Aluguel":
                    self.ROWS = [list(Init.uma_venda_aluguel.__dict__.keys())]
                    Init.imobiliaria.get_estoque().get_lista_imoveis()

            self.imoveis_filtrados = []
            self.atualizar()

    def on_mount(self):
        self.ROWS = [list(Init.um_imovel.__dict__.keys())]
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
        if isinstance(Init.usuario_atual, Corretor.Corretor):
            if event.tabs.active == self.query_one("#tab_dados_imobiliaria", Tab).id:
                self.app.switch_screen("tela_dados_imobiliaria")
        if self.is_admin:
            if event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                self.app.switch_screen("tela_servidor")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_estoque", Tab).id

    def atualizar(self):
        self.ROWS = [self.ROWS[0]]
        self.query_one(SelectionList).clear_options()
        self.query_one(SelectionList).add_options((name, name)
                                                  for name in Init.dict_objetos[self.tabela.lower()].__dict__.keys() if not name.startswith("_"))

        table = self.query_one(DataTable)
        table.clear(columns=True)

        if len(self.imoveis_filtrados) > 0:
            lista_atual = self.imoveis_filtrados
        else:
            self.imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()
            lista_atual = self.imoveis

        for imovel in lista_atual:
            lista = []
            for valor in imovel.__dict__.values():
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
            self.imoveis_filtrados = []
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

            if len(self.imoveis_filtrados) > 0:
                imoveis_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for imovel in self.imoveis_filtrados:
                            try:
                                if p in getattr(imovel, campo)() and imovel not in imoveis_temp:
                                    imoveis_temp.append(
                                        imovel)
                            except:
                                if p == getattr(imovel, campo)() and imovel not in imoveis_temp:
                                    imoveis_temp.append(
                                        imovel)
                else:
                    for imovel in self.imoveis_filtrados:
                        try:
                            if filtro in getattr(imovel, campo)() and imovel not in imoveis_temp:
                                imoveis_temp.append(imovel)
                        except:
                            if filtro == getattr(imovel, campo)() and imovel not in imoveis_temp:
                                imoveis_temp.append(imovel)

                if len(imoveis_temp) > 0:
                    self.imoveis_filtrados = imoveis_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for imovel in self.imoveis:
                            try:
                                if p in getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                    self.imoveis_filtrados.append(
                                        imovel)
                            except:
                                if p == getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                    self.imoveis_filtrados.append(
                                        imovel)

                else:
                    for imovel in self.imoveis:
                        try:
                            if filtro in getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                self.imoveis_filtrados.append(imovel)
                        except:
                            if filtro == getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                self.imoveis_filtrados.append(imovel)
