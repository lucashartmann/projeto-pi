from textual.widgets import Button, Select, Tab, Tabs, Header, Footer, SelectionList, TextArea, Input, Label, Checkbox
from textual.screen import Screen
from textual.containers import HorizontalGroup, VerticalGroup
from database import Shelve
from model import Init


class TelaPerfil(Screen):

    CSS_PATH = "css/TelaPerfil.tcss"

    filtros = {
        "nome_perfil": "",
        "tabelas": [],
        "products": [],
        "orders": [],
        "customers": [],
        "coupons": [],
        "taxes": []
    }

    tabela = "products"
    operacao = "Adicionar"

    def compose(self):
        yield Header()
        yield Tabs(Tab("TelaPerfil", id="tab_perfil"), Tab("TelaCadastrar", id="tab_cadastrar"), Tab("TelaConsultar", id="tab_consultar"))
        with HorizontalGroup(id="hg_checkboxes"):
            yield Checkbox(label="Products", value=True)
            yield Checkbox(label="Orders", value=True)
            yield Checkbox(label="Customers", value=True)
            yield Checkbox(label="Coupons", value=True)
            yield Checkbox(label="Taxes", value=True)
        with HorizontalGroup():
            with VerticalGroup(id="vg_left"):
                yield Select([("Products", "Products"), ("Orders", "Orders"), ("Customers", "Customers"), ("Coupons", "Coupons"), ("Taxes", "Taxes")], allow_blank=False, id="select_tabelas")
                yield SelectionList[str](id="selection_filtros")
            with VerticalGroup(id="vg_right"):
                with HorizontalGroup():
                    yield Label("Nome do perfil:")
                    yield Input()
                yield TextArea(id="tx_products")
                yield TextArea(id="tx_orders")
                yield TextArea(id="tx_customers")
                yield TextArea(id="tx_coupons")
                yield TextArea(id="tx_taxes")
                with HorizontalGroup():
                    yield Select([("Adicionar", "Adicionar"), ("Editar", "Editar"), ("Remover", "Remover")], allow_blank=False, id="select_operacoes")
                    yield Button("Executar")

        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_consultar", Tab).id:
            self.app.switch_screen("tela_consultar")
        elif event.tabs.active == self.query_one("#tab_cadastrar", Tab).id:
            self.app.switch_screen("tela_cadastro")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_perfil", Tab).id

    def on_mount(self):
        self.filtros["tabelas"] = ["products","orders", "customers","coupons", "taxes"]
        self.query_one(
            "#tx_products", TextArea).text = "Filtros da tabela produtos:\n"
        self.query_one(
            "#tx_orders", TextArea).text = "Filtros da tabela orders:\n"
        self.query_one(
            "#tx_customers", TextArea).text = "Filtros da tabela customers:\n"
        self.query_one(
            "#tx_coupons", TextArea).text = "Filtros da tabela coupons:\n"
        self.query_one(
            "#tx_taxes", TextArea).text = "Filtros da tabela taxes:\n"

    def on_selection_list_selected_changed(self, evento: SelectionList.SelectedChanged):

        match self.tabela:
            case "products":

                self.filtros["products"] = evento.selection_list.selected
                self.query_one(
                    "#tx_products", TextArea).text = "Filtros da tabela produtos:\n" + ", ".join(self.filtros["products"])
            case "orders":
                self.filtros["orders"] = evento.selection_list.selected
                self.query_one(
                    "#tx_orders", TextArea).text = "Filtros da tabela orders:\n" + ", ".join(self.filtros["orders"])
            case "customers":
                self.filtros["customers"] = evento.selection_list.selected
                self.query_one(
                    "#tx_customers", TextArea).text = "Filtros da tabela customers:\n" + ", ".join(self.filtros["customers"])
            case "coupons":
                self.filtros["coupons"] = evento.selection_list.selected
                self.query_one(
                    "#tx_coupons", TextArea).text = "Filtros da tabela coupons:\n" + ", ".join(self.filtros["coupons"])
            case "taxes":
                self.filtros["taxes"] = evento.selection_list.selected
                self.query_one(
                    "#tx_taxes", TextArea).text = "Filtros da tabela taxes:\n" + ", ".join(self.filtros["taxes"])

    def on_select_changed(self, evento: Select.Changed):
        if evento.select.id == "select_tabelas":
            self.tabela = evento.select.value.lower()
            self.query_one("#selection_filtros", SelectionList).clear_options()

            self.query_one("#selection_filtros", SelectionList).add_options((name, name)
                                                                            for name in Init.dict_objetos[self.tabela].__dict__.keys() if not name.startswith("_"))

            if self.filtros[self.tabela]:
                for valor in self.filtros[self.tabela]:
                    self.query_one("#selection_filtros",
                                   SelectionList).select(valor)
            else:
                self.query_one("#selection_filtros",
                               SelectionList).deselect_all()
        else:
            self.operacao = evento.select.value

    def on_checkbox_changed(self, evento: Checkbox.Changed):
        tabela = str(evento.checkbox.label).lower()
        if evento.checkbox.value:
            if tabela not in self.filtros["tabelas"]:
                self.filtros["tabelas"].append(tabela)
        else:
            if tabela in self.filtros["tabelas"]:
                self.filtros["tabelas"].remove(tabela)

    def on_button_pressed(self):
        if self.query_one(Input).value == "":
            self.notify("ERRO! Insira um nome de usuário válido")
            return
        
        self.filtros["nome_perfil"] = self.query_one(Input).value
        match self.operacao:
            case "Adicionar":
                dicionario_perfis = Shelve.carregar(
                    "perfis.db", "perfis") or {}
                if self.filtros["nome_perfil"] in dicionario_perfis:
                    self.notify(
                        "Já existe um perfil com esse nome. Escolha outro nome.")
                    return
                else:
                    dicionario_perfis[self.filtros["nome_perfil"]
                                      ] = self.filtros
                    Shelve.salvar("perfis.db", "perfis", dicionario_perfis)
                    self.notify("Perfil salvo com sucesso!")
            case "Editar":
                dicionario_perfis = Shelve.carregar(
                    "perfis.db", "perfis") or {}
                if self.filtros["nome_perfil"] not in dicionario_perfis:
                    self.notify(
                        "Não existe um perfil com esse nome. Escolha outro nome.")
                    return
                else:
                    dicionario_perfis[self.filtros["nome_perfil"]
                                      ] = self.filtros
                    Shelve.salvar("perfis.db", "perfis", dicionario_perfis)
                    self.notify("Perfil atualizado com sucesso!")
            case "Remover":
                dicionario_perfis = Shelve.carregar(
                    "perfis.db", "perfis") or {}
                if self.filtros["nome_perfil"] not in dicionario_perfis:
                    self.notify(
                        "Não existe um perfil com esse nome. Escolha outro nome.")
                    return
                else:
                    del dicionario_perfis[self.filtros["nome_perfil"]]
                    Shelve.salvar("perfis.db", "perfis", dicionario_perfis)
                    self.notify("Perfil removido com sucesso!")
