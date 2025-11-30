import datetime
from textual.widgets import Button, Tab, Tabs, Select, Header, Footer, SelectionList, Static, TextArea, MaskedInput
from textual.screen import Screen
from textual.containers import Grid, HorizontalGroup

from controller import Controller
from model import Init, Corretor, Administrador, Gerente


class TelaCadastroPessoa(Screen):

    CSS_PATH = "css/TelaCadastroPessoa.tcss"

    valor_select = ""
    tabela = "products"
    montados = list()
    montou_remover = False
    montou_editar = False
    perfis = None
    perfil_atual = None

    def compose(self):

        yield Header()

        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif isinstance(Init.usuario_atual, Corretor.Corretor):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        elif isinstance(Init.usuario_atual, Gerente.Gerente):
            yield Tabs(Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"),
                       Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Estoque", id="tab_estoque"))
        else:
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        with Grid():
            yield Static("Username", id="stt_username")
            yield TextArea(placeholder="username aqui", id="inpt_username")
            yield Static("Senha", id="stt_senha")
            yield TextArea(placeholder="senha aqui", id="inpt_senha")
            yield Static("Nome", id="stt_nome")
            yield TextArea(placeholder="nome aqui", id="inpt_nome")
            yield Static("Email", id="stt_email")
            yield TextArea(placeholder="email aqui", id="inpt_email")
            yield Static("Telefone", id="stt_telefone")
            yield MaskedInput(template="(00) 00000-0000", id="inpt_telefone")
            yield Static("Endereco", id="stt_endereco")
            yield TextArea(placeholder="endereco aqui", id="inpt_endereco")
            yield Static("Idade", id="stt_idade")
            yield TextArea(placeholder="idade aqui", id="inpt_idade")
            yield Static("Data de nascimento", id="stt_data_nascimento")
            yield MaskedInput(template="00/00/0000", id="inpt_data_nascimento")
            yield Static("CPF", id="stt_cpf")
            yield MaskedInput(template="000.000.000-00", id="inpt_cpf")
            yield Static("RG", id="stt_rg")
            yield TextArea(placeholder="rg aqui", id="inpt_rg")
        with HorizontalGroup(id="hg_operacoes"):
            if isinstance(Init.usuario_atual, Administrador.Administrador):
                yield Select([("Comprador", "Comprador"), (
                    "Proprietario", "Proprietario"), ("Corretor", "Corretor"), ("Captador", "Captador"), ("Administrador", "Administrador")], allow_blank=False, id="select_tabelas")
            else:
                yield Select([("Comprador", "Comprador"), (
                    "Proprietario", "Proprietario")], allow_blank=False, id="select_tabelas")

            yield Select([("Adicionar", "Adicionar"), ("Editar", "Editar"), ("Remover", "Remover")], allow_blank=False, id="select_operacoes")
            yield Button("Executar")
        yield Footer(show_command_palette=False)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:
            if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
                self.app.switch_screen("tela_estoque")
            elif event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                self.app.switch_screen("tela_cadastro_imovel")
            elif isinstance(Init.usuario_atual, Gerente.Gerente):
                if event.tabs.active == self.query_one("#tab_dados_imobiliaria", Tab).id:
                    self.app.switch_screen("tela_dados_imobiliaria")
            elif isinstance(Init.usuario_atual, Administrador.Administrador):
                if event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                    self.app.switch_screen("tela_servidor")
            elif event.tabs.active == self.query_one("#tab_comprar", Tab).id:
                self.app.switch_screen("tela_estoque_cliente")
            elif event.tabs.active == self.query_one("#tab_dados_cliente", Tab).id:
                self.app.switch_screen("tela_dados_cliente")
        except:
            pass

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_cadastro_pessoa", Tab).id

    def on_mount(self):
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            self.query_one("#select_tabelas", Select).set_options(
                [("Comprador", "Comprador"), (
                    "Proprietário", "Proprietario"), ("Corretor", "Corretor"), ("Captador", "Captador"), ("Administrador", "Administrador"), ("Funcionario", "Funcionario"), ("Gerente", "Gerente")])
        elif isinstance(Init.usuario_atual, Gerente.Gerente):
            self.query_one("#select_tabelas", Select).set_options(
                [("Funcionario", "Funcionario"), ("Gerente", "Gerente")])
        else:
            self.query_one("#select_tabelas", Select).set_options([("Comprador", "Comprador"), (
                "Proprietário", "Proprietario")])

    def on_select_changed(self, evento: Select.Changed):

        if evento.select.id == "select_tabelas":

            if evento.select.value.lower() == "proprietario":
                self.query_one(Grid).query_one(
                    "#stt_username").styles.display = "none"
                self.query_one(Grid).query_one(
                    "#inpt_username").styles.display = "none"
                self.query_one(Grid).query_one(
                    "#stt_senha").styles.display = "none"
                self.query_one(Grid).query_one(
                    "#inpt_senha").styles.display = "none"
            else:
                self.query_one(Grid).query_one(
                    "#stt_username").styles.display = "block"
                self.query_one(Grid).query_one(
                    "#inpt_username").styles.display = "block"
                self.query_one(Grid).query_one(
                    "#stt_senha").styles.display = "block"
                self.query_one(Grid).query_one(
                    "#inpt_senha").styles.display = "block"

        else:
            match evento.select.value:

                case "Editar":
                    self.query_one(SelectionList).disabled = False

                    if self.montou_editar == False and self.montou_remover == False:
                        self.query_one(Grid).mount(Static("ID de pesquisa",
                                                          id="stt_id_pesquisa"), before=0)
                        self.query_one(Grid).mount(TextArea(placeholder="id do imovel de pesquisa",
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
                        self.query_one(Grid).mount(TextArea(placeholder="id do imovel de pesquisa",
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
                id_imovel = self.query_one("#inpt_id_pesquisa", TextArea).text
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
                    self.tabela, id_imovel, dados)

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
                id_imovel = self.query_one(TextArea).text
                remocao = Controller.remover_item(self.tabela, id_imovel)
                self.notify(remocao)
                self.limpar_text_area()
                try:
                    self.app.get_screen("tela_consultar").atualizar()
                except:
                    pass

        self.limpar_text_area()
