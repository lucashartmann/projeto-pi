import datetime
from textual.widgets import Button, Tab, Tabs, Select, Header, Footer, SelectionList, Static, TextArea, MaskedInput
from textual.screen import Screen
from textual.containers import Grid, HorizontalGroup

from controller import Controller
from model import Init, Usuario


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

        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.CORRETOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
            yield Tabs(Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"),
                       Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Estoque", id="tab_estoque"))
        else:
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        with Grid():
            if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
                yield Static("Username", id="stt_username")
                yield TextArea(placeholder="username aqui", id="inpt_username")
                yield Static("Senha", id="stt_senha")
            else:
                # yield TextArea(placeholder="senha aqui", id="inpt_senha")
                yield Static("Nome", id="stt_nome")
                yield TextArea(placeholder="nome aqui", id="inpt_nome")
                yield Static("Email", id="stt_email")
                yield TextArea(placeholder="email aqui", id="inpt_email")
                yield Static("Telefone", id="stt_telefone")
                yield MaskedInput(template="(00) 00000-0000", id="inpt_telefone")
                # yield Static("Endereco", id="stt_endereco")
                # yield TextArea(placeholder="endereco aqui", id="inpt_endereco")
                # yield Static("Idade", id="stt_idade")
                # yield TextArea(placeholder="idade aqui", id="inpt_idade")
                yield Static("Data de nascimento", id="stt_data_nascimento")
                yield MaskedInput(template="00/00/0000", id="inpt_data_nascimento")
                yield Static("CPF", id="stt_cpf")
                yield MaskedInput(template="00000000000", id="inpt_cpf")
                yield Static("RG", id="stt_rg")
                yield TextArea(placeholder="rg aqui", id="inpt_rg")
        with HorizontalGroup(id="hg_operacoes"):
            if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
                yield Select([("Usuário", "Usuario")], allow_blank=False, id="select_tabelas")
            elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
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
            if event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                self.app.switch_screen("tela_cadastro_pessoa")

            elif event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                self.app.switch_screen("tela_cadastro_imovel")

            elif event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                self.app.switch_screen("tela_cadastro_imovel")

            elif event.tabs.active == self.query_one("#tab_estoque", Tab).id:
                self.app.switch_screen("tela_estoque")

            elif event.tabs.active == self.query_one("#tab_dados_imobiliaria", Tab).id:
                self.app.switch_screen("tela_dados_imobiliaria")

            elif event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                self.app.switch_screen("tela_servidor")

            elif event.tabs.active == self.query_one("#tab_comprar", Tab).id:
                self.app.switch_screen("tela_estoque_cliente")

            elif event.tabs.active == self.query_one("#tab_dados_cliente", Tab).id:
                self.app.switch_screen("tela_dados_cliente")

            elif event.tabs.active == self.query_one("#tab_atendimento", Tab).id:
                self.app.switch_screen("tela_atendimento")

            elif event.tabs.active == self.query_one("#tab_cadastro_venda_aluguel", Tab).id:
                self.app.switch_screen("tela_cadastro_venda_aluguel")

        except:
            pass

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_cadastro_pessoa", Tab).id

    def on_mount(self):
        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            self.query_one("#select_tabelas", Select).set_options(
                [("Comprador", "Comprador"), (
                    "Proprietário", "Proprietario"), ("Corretor", "Corretor"), ("Captador", "Captador"), ("Administrador", "Administrador"), ("Funcionario", "Funcionario"), ("Gerente", "Gerente")])
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
            self.query_one("#select_tabelas", Select).set_options(
                [("Funcionario", "Funcionario"), ("Gerente", "Gerente")])
        else:
            self.query_one("#select_tabelas", Select).set_options([("Comprador", "Comprador"), (
                "Proprietário", "Proprietario")])

    def on_select_changed(self, evento: Select.Changed):

        match evento.select.value:

            case "Editar":

                if self.montou_editar == False and self.montou_remover == False:
                    self.query_one(Grid).mount(Static("CPF de pesquisa",
                                                      id="stt_id_pesquisa"), before=0)
                    self.query_one(Grid).mount(MaskedInput(template="00000000000",
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
                            "#inpt_id_pesquisa", MaskedInput).remove()
                    except:
                        pass
                    self.montou_editar = False
                    self.montou_remover = False

            case "Remover":
           

                if self.montou_editar and self.montou_remover == False:
                    self.query_one(Grid).remove_children(
                        list(self.query_one(Grid).query_children()[2:]))
                    self.montou_editar = False
                    self.montou_remover = True
                else:
                    self.query_one(Grid).remove_children()
                    self.query_one(Grid).mount(Static("CPF de pesquisa",
                                                      id="stt_id_pesquisa"), before=0)
                    self.query_one(Grid).mount(MaskedInput(template="00000000000",
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
                cpf_pesquisa = self.query_one("#inpt_id_pesquisa", MaskedInput).value
                nome = self.query_one("#inpt_nome", TextArea).text
                email = self.query_one("#inpt_email", TextArea).text
                telefone = self.query_one("#inpt_telefone", MaskedInput).value.strip().strip(
                    "(").strip(")").strip("-")
                data_nascimento = self.query_one(
                    "#inpt_data_nascimento", MaskedInput).value.strip("/")
                cpf = self.query_one("#inpt_cpf", MaskedInput).value.strip()
                rg = TextArea(placeholder="rg aqui", id="inpt_rg").text

                match self.query_one("#select_tabelas", Select).value:
                    case "Comprador":
                        atualizacao = Controller.editar_comprador(cpf_pesquisa,
                            nome, email, telefone, data_nascimento, cpf, rg)
                    case "Proprietario":
                        atualizacao = Controller.editar_proprietario(cpf_pesquisa,
                            nome, email, telefone, data_nascimento, cpf, rg)
                    case "Corretor":
                        atualizacao = Controller.editar_corretor(cpf_pesquisa,
                            nome, email, telefone, data_nascimento, cpf, rg)
                    case "Captador":
                        atualizacao = Controller.editar_captador(cpf_pesquisa,
                            nome, email, telefone, data_nascimento, cpf, rg)
                    case "Administrador":
                        atualizacao = Controller.editar_administrador(cpf_pesquisa,
                            nome, email, telefone, data_nascimento, cpf, rg)

           

                self.notify(atualizacao)
                self.limpar_text_area()
             

            case "Adicionar":
                nome = self.query_one("#inpt_nome", TextArea).text
                email = self.query_one("#inpt_email", TextArea).text
                telefone = self.query_one("#inpt_telefone", MaskedInput).value.strip().strip(
                    "(").strip(")").strip("-")
                data_nascimento = self.query_one(
                    "#inpt_data_nascimento", MaskedInput).value.strip("/")
                cpf = self.query_one("#inpt_cpf", MaskedInput).value.strip()
                rg = TextArea(placeholder="rg aqui", id="inpt_rg").text
           
                match self.query_one("#select_tabelas", Select).value:
                    case "Comprador":
                        cadatro = Controller.cadastrar_comprador(
                            nome, email, telefone, data_nascimento, cpf, rg)
                    case "Proprietario":
                        cadatro = Controller.cadastrar_proprietario(
                            nome, email, telefone, data_nascimento, cpf, rg)
                    case "Corretor":
                        cadatro = Controller.cadastrar_corretor(
                            nome, email, telefone, data_nascimento, cpf, rg)
                    case "Captador":
                        cadatro = Controller.cadastrar_captador(
                            nome, email, telefone, data_nascimento, cpf, rg)
                    case "Administrador":
                        cadatro = Controller.cadastrar_administrador(
                            nome, email, telefone, data_nascimento, cpf, rg)

                self.notify(cadatro)
                self.limpar_text_area()
            case "Remover":
                cpf = self.query_one("#inpt_id_pesquisa", MaskedInput).value

                match self.query_one("#select_tabelas", Select).value:
                    case "Comprador":
                        remocao = Controller.remover_comprador(cpf)
                    case "Proprietario":
                        remocao = Controller.remover_proprietario(cpf)
                    case "Corretor":
                        remocao = Controller.remover_corretor(cpf)
                    case "Captador":
                        remocao = Controller.remover_captador(cpf)
                    # case "Administrador":
                    #     remocao = Controller.remover_administrador(id)
                self.notify(remocao)
                self.limpar_text_area()
             

        self.limpar_text_area()
