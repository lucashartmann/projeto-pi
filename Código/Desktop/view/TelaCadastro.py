import datetime
from textual.widgets import Button, Tab, Tabs, Select, Header, Footer, SelectionList, Static, TextArea, MaskedInput
from textual.screen import Screen
from textual.containers import Grid, HorizontalGroup, VerticalGroup
from textual import on

from controller import Controller
from model import Init


class TelaCadastro(Screen):

    CSS_PATH = "css/TelaCadastro.tcss"

    valor_select = ""
    tabela = "products"
    montados = list()
    montou_remover = False
    montou_editar = False
    perfis = None
    perfil_atual = None

    def compose(self):
        yield Header()
        if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:
            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"))
        elif Init.usuario.get_tipo() == TipoUsuario.GERENTE:
            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"), Tab("Dados da Loja", id="tab_dados_loja"))
        else:
            yield Tabs(Tab("Cadastro", id="tab_cadastro"), Tab("Estoque", id="tab_estoque"))

        with HorizontalGroup(id="hg_first"):
            with VerticalGroup(id="vg_left"):

                if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:
                    yield Select([("Usuario", "Usuario")], allow_blank=False, id="select_tabelas")
                elif Init.usuario.get_tipo() == TipoUsuario.GERENTE:
                    yield Select([("Cliente", "Cliente"), ("Funcionario", "Funcionario"), ("Fornecedor", "Fornecedor"), ("Produto", "Produto")], allow_blank=False, id="select_tabelas")
                else:
                    yield Select([("Cliente", "Cliente"), ("Produto", "Produto")], allow_blank=False, id="select_tabelas")
                yield SelectionList[str]()
            with VerticalGroup(id="vg_right"):
                with Grid():
                    yield Static("Name", classes="name")
                    yield TextArea(placeholder="nome aqui", id="stt_nome", classes="name")
                    yield Static("Regular_Price", classes="regular_price")
                    yield TextArea(placeholder="preço aqui", classes="regular_price")
                    yield Static("Description", classes="description")
                    yield TextArea(placeholder="Descrição aqui", classes="description")
                with HorizontalGroup(id="hg_operacoes"):
                    yield Select([("Adicionar", "Adicionar"), ("Editar", "Editar"), ("Remover", "Remover")], allow_blank=False, id="select_operacoes")
                    yield Button("Executar")
        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
            self.app.switch_screen("tela_estoque")
        if Init.usuario.get_tipo() == TipoUsuario.GERENTE:
            if event.tabs.active == self.query_one("#tab_dados_loja", Tab).id:
                self.app.switch_screen("tela_dados_loja")
        if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:
            if event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                self.app.switch_screen("tela_servidor")

    @on(SelectionList.SelectedChanged)
    def update_selected_view(self):
        lista_selecionados = self.query_one(SelectionList).selected

        for valor in self.montados:
            if valor not in lista_selecionados:
                self.montados.remove(valor)
                self.query_one(Grid).query(f".{valor}").remove()
            else:
                lista_selecionados.remove(valor)

        if len(lista_selecionados) > 0:
            for valor in lista_selecionados:
                if not self.query(f".{valor}"):

                    for key, valor_construtor in Init.dict_objetos[self.tabela].__dict__.items():
                        if key == valor:
                            if isinstance(valor_construtor, str):
                                self.query_one(Grid).mount(Static(content=valor.capitalize(),
                                                                  classes=valor))
                                self.query_one(Grid).mount(
                                    TextArea(classes=valor))
                            elif isinstance(valor_construtor, bool):
                                self.query_one(Grid).mount(Static(content=valor.capitalize(),
                                                                  classes=valor))
                                self.query_one(Grid).mount(
                                    Select([("True", True), ("False", False)], classes=valor, allow_blank=False))
                            elif isinstance(valor_construtor, datetime.datetime):
                                self.query_one(Grid).mount(Static(content=valor.capitalize(),
                                                                  classes=valor))
                                self.query_one(Grid).mount(MaskedInput(
                                    template='00/00/0000 00:00', placeholder="dd/mm/yyyy hh:mm", classes=valor))
                            else:
                                pass
                    self.montados.append(valor)

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_cadastro", Tab).id

    def atualizar(self):
        self.query_one(SelectionList).clear_options()

        self.montados = []
        self.query_one(Grid).remove_children()

        self.query_one(SelectionList).add_options((name, name)
                                                  for name in Init.dict_objetos[self.tabela.lower()].__dict__.keys() if not name.startswith("_"))

    def on_select_changed(self, evento: Select.Changed):

        if evento.select.id == "select_tabelas":
            self.tabela = evento.select.value.lower()

            if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:
                self.query_one("#select_tabelas", Select).set_options(
                    [("Usuario", "Usuario")])
            elif Init.usuario.get_tipo() == TipoUsuario.GERENTE:
                self.query_one("#select_tabelas", Select).set_options([("Cliente", "Cliente"), (
                    "Funcionario", "Funcionario"), ("Fornecedor", "Fornecedor"), ("Produto", "Produto")])
            else:
                self.query_one("#select_tabelas", Select).set_options(
                    [("Cliente", "Cliente"), ("Produto", "Produto")])

            self.atualizar()

        else:
            match evento.select.value:

                case "Editar":
                    self.query_one(SelectionList).disabled = False

                    if self.montou_editar == False and self.montou_remover == False:
                        self.query_one(Grid).mount(Static("ID de pesquisa",
                                                          id="stt_id_pesquisa"), before=0)
                        self.query_one(Grid).mount(TextArea(placeholder="id do produto de pesquisa",
                                                            id="inpt_id_pesquisa"), before=1)
                        self.montou_editar = True

                    self.valor_select = "Editar"

                case "Adicionar":
                    self.valor_select = "Adicionar"
                    if self.montou_editar or self.montou_remover:
                        self.query_one(SelectionList).disabled = False
                        try:
                            self.query_one(Grid).query_one(
                                "#stt_id_pesquisa", Static).remove()
                            self.query_one(Grid).query_one(
                                "#inpt_id_pesquisa", TextArea).remove()
                        except:
                            pass
                        self.montou_editar = False
                        self.montou_remover = False

                case "Remover":
                    self.montados = []
                    self.query_one(SelectionList).disabled = True

                    if self.montou_editar and self.montou_remover == False:
                        self.query_one(Grid).remove_children(
                            list(self.query_one(Grid).query_children()[2:]))
                        self.montou_editar = False
                        self.montou_remover = True
                    else:
                        self.query_one(Grid).remove_children()
                        self.query_one(Grid).mount(Static("ID de pesquisa",
                                                          id="stt_id_pesquisa"), before=0)
                        self.query_one(Grid).mount(TextArea(placeholder="id do produto de pesquisa",
                                                            id="inpt_id_pesquisa"), before=1)
                        self.montou_remover = True

                    self.valor_select = "Remover"

    def limpar_text_area(self):
        for tx in self.query(TextArea):
            tx.text = ""
        if MaskedInput in self.query():
            for m_i in self.query(MaskedInput):
                m_i.value = ""

    def on_button_pressed(self):
        lista_valores = [widget for widget in self.query_one(
            Grid).query() if not isinstance(widget, Static)]
        lista_chaves = [
            static for static in self.query_one(Grid).query(Static)]

        match self.valor_select:
            case "Editar":
                id_produto = self.query_one("#inpt_id_pesquisa", TextArea).text
                dados = dict()
                lista_chaves = lista_chaves[1:]

                for stt in lista_chaves:
                    string_limpa = (stt.content.split()[0].lower())
                    dados[string_limpa] = ""

                for i, valor in enumerate(lista_valores):
                    if isinstance(valor, TextArea):
                        dados[list(dados.keys())[i]] = valor.text
                    elif isinstance(valor, MaskedInput):
                        data_split = valor.value.split()
                        data = data_split[1].split("/")
                        dia = int(data[0])
                        mes = int(data[1])
                        ano = int(data[2])
                        horario = data_split[1].split(":")
                        hora = horario[0]
                        minuto = horario[1]
                        try:
                            datahora = datetime.datetime(
                                year=ano, month=mes, day=dia, hour=hora, minute=minuto)
                        except Exception as e:
                            self.notify(f"ERRO! Problema com data. {e}")
                            return
                        dados[list(dados.keys())[i]] = str(datahora)
                    else:
                        dados[list(dados.keys())[i]] = valor.value

                atualizacao = Controller.atualizar_item(
                    self.tabela, id_produto, dados)

                self.notify(atualizacao)
                try:
                    self.app.get_screen("tela_consultar").atualizar()
                except:
                    pass

            case "Adicionar":
                dados = dict()

                for chave in lista_chaves:
                    string_limpa = (chave.content.split()[0].lower())
                    dados[string_limpa] = ""

                for i, valor in enumerate(lista_valores):
                    if isinstance(valor, TextArea):
                        dados[list(dados.keys())[i]] = valor.text
                    elif isinstance(valor, MaskedInput):
                        data_split = valor.value.split()
                        data = data_split[1].split("/")
                        dia = int(data[0])
                        mes = int(data[1])
                        ano = int(data[2])
                        horario = data_split[1].split(":")
                        hora = horario[0]
                        minuto = horario[1]
                        try:
                            datahora = datetime.datetime(
                                year=ano, month=mes, day=dia, hour=hora, minute=minuto)
                        except Exception as e:
                            self.notify(f"ERRO! Problema com data. {e}")
                            return
                        dados[list(dados.keys())[i]] = str(datahora)
                    else:
                        dados[list(dados.keys())[i]] = valor.value

                adicao = Controller.adicionar_item(self.tabela, dados)
                self.notify(adicao)
                self.limpar_text_area()
                try:
                    self.app.get_screen("tela_consultar").atualizar()
                except:
                    pass

            case "Remover":
                id_produto = self.query_one(TextArea).text
                remocao = Controller.remover_item(self.tabela, id_produto)
                self.notify(remocao)
                self.limpar_text_area()
                try:
                    self.app.get_screen("tela_consultar").atualizar()
                except:
                    pass

        self.limpar_text_area()
