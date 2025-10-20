from textual.widgets import Button, Static, TextArea, Select, Tab, Tabs, Header, Footer, SelectionList, MaskedInput
from controller import Controller
from unidecode import unidecode
from textual.screen import Screen
from textual.containers import Grid, HorizontalGroup, VerticalGroup
from textual import on
from model import Init
from datetime import datetime
from textual.message import Message
import datetime
from database import Shelve


class CadastroRealizado(Message):
    def __init__(self, sender) -> None:
        super().__init__()
        self.sender = sender


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
        yield Tabs(Tab("TelaPerfil", id="tab_perfil"), Tab("TelaCadastrar", id="tab_cadastrar"), Tab("TelaConsultar", id="tab_consultar"))
        with HorizontalGroup(id="hg_first"):
            with VerticalGroup(id="vg_left"):
                yield Select([("Complex", "Complex")], allow_blank=False, id="select_perfil")
                yield Select([("Products", "Products"), ("Orders", "Orders"), ("Customers", "Customers"), ("Coupons", "Coupons"), ("Taxes", "Taxes")], allow_blank=False, id="select_tabelas")
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

    contador = 0

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
                                # TODO: Tem que lidar com listas, objetos...
                                pass
                                # self.query_one(Grid).mount(
                                #     TextArea(classes=valor))
                    self.montados.append(valor)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_consultar", Tab).id:
            self.app.switch_screen("tela_consultar")
        elif event.tabs.active == self.query_one("#tab_perfil", Tab).id:
            self.app.switch_screen("tela_perfil")

    def on_screen_resume(self):
            perfis = Shelve.carregar("perfis.db", "perfis") or {}
            if perfis:  
                lista = list((chave, chave) for chave in perfis.keys())
                lista.append(("Complex", "Complex"))
                self.query_one("#select_perfil", Select).set_options(lista)
                print(perfis)
                self.perfis = perfis
            else:

                self.query_one("#select_perfil", Select).set_options([("Complex", "Complex")])
            self.query_one(Tabs).active = self.query_one("#tab_cadastrar", Tab).id
            
    def atualizar(self):
        self.query_one(SelectionList).clear_options()

        self.montados = []
        self.query_one(Grid).remove_children()

        if self.perfil_atual == "Complex":
                self.query_one(SelectionList).add_options((name, name)
                                                          for name in Init.dict_objetos[self.tabela].__dict__.keys() if not name.startswith("_"))

        else:
                dicionario = self.perfis[self.perfil_atual]
                self.query_one(SelectionList).add_options((name, name)
                                                          for name in dicionario[self.tabela])

    def on_select_changed(self, evento: Select.Changed):

        if evento.select.id == "select_tabelas":
            self.tabela = evento.select.value.lower()
            self.atualizar()

        elif evento.select.id == "select_perfil":
            self.perfil_atual = evento.select.value
            if self.perfil_atual == "Complex":
                self.query_one("#select_tabelas", Select).set_options([("Products", "Products"), (
                    "Orders", "Orders"), ("Customers", "Customers"), ("Coupons", "Coupons"), ("Taxes", "Taxes")])
            else:
                dicionario = self.perfis[self.perfil_atual]
                self.query_one("#select_tabelas", Select).set_options(
                    (tabela.capitalize(), tabela.capitalize()) for tabela in dicionario["tabelas"])
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
                    string_limpa = unidecode(stt.content.split()[0].lower())
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
                    string_limpa = unidecode(chave.content.split()[0].lower())
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
