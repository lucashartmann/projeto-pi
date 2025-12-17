import datetime
from textual.widgets import Button, Tab, Tabs, Select, Footer, SelectionList, Static, TextArea, MaskedInput, Input
from textual.screen import Screen
from textual.containers import Grid, HorizontalGroup
from controller import Controller
from model import Init, Usuario, Captador, Cliente, Corretor, Proprietario
from utils.Widgets import Header
from textual.validation import Length


class TelaCadastroPessoa(Screen):

    CSS_PATH = "css/TelaCadastroPessoa.tcss"

    valor_select = ""
    tabela = "products"
    montados = list()
    montou_remover = False
    montou_editar = False
    perfis = None
    perfil_atual = None

    def __init__(self, name=None, id=None, classes=None, pessoa=None):
        super().__init__(name, id, classes)
        self.pessoa = pessoa

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
                yield TextArea(placeholder="senha aqui", id="inpt_senha")
            else:
                yield Static("[red]*[/]Nome", id="stt_nome")
                yield TextArea(placeholder="nome aqui", id="inpt_nome")
                yield Static("[red]*[/]Email", id="stt_email")
                yield TextArea(placeholder="email aqui", id="inpt_email")
                # yield Static("Telefone", id="stt_telefone")
                # yield MaskedInput(template="(00) 00000-0000", id="inpt_telefone")
                # yield Static("Endereco", id="stt_endereco")
                # yield TextArea(placeholder="endereco aqui", id="inpt_endereco")
                yield Static("Data de nascimento", id="stt_data_nascimento")
                yield MaskedInput(template="00/00/0000", id="inpt_data_nascimento", validators=Length(minimum=10, maximum=10), valid_empty=True)
                yield Static("[red]*[/]CPF", id="stt_cpf")
                yield MaskedInput(template="000.000.000-00", id="inpt_cpf", validators=Length(minimum=11, maximum=14), valid_empty=True)
                yield Static("RG", id="stt_rg")
                yield Input(id="inpt_rg", placeholder="RG aqui", validators=Length(minimum=7, maximum=9), valid_empty=True)
        with HorizontalGroup(id="hg_operacoes"):
            if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
                yield Select([("Usuário", "Usuario")], allow_blank=False, id="select_tabelas")
            elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
                yield Select([("Cliente", "Cliente"), (
                    "Proprietario", "Proprietario"), ("Corretor", "Corretor"), ("Captador", "Captador")], allow_blank=False, id="select_tabelas")
            else:
                yield Select([("Cliente", "Cliente"), (
                    "Proprietario", "Proprietario")], allow_blank=False, id="select_tabelas")

            yield Select([("Adicionar", "Adicionar"), ("Editar", "Editar"), ("Remover", "Remover")], allow_blank=False, id="select_operacoes")
            yield Button("Executar")
        yield Footer(show_command_palette=False)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:

            if event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
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
                [("Usuário", "Usuário")])
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
            self.query_one("#select_tabelas", Select).set_options(
                [("Funcionario", "Funcionario"), ("Gerente", "Gerente")])
        else:
            self.query_one("#select_tabelas", Select).set_options([("Comprador", "Comprador"), (
                "Proprietário", "Proprietario")])

        if self.pessoa:
            self.query_one(
                "#inpt_nome", TextArea).text = self.pessoa.get_nome()
            if self.pessoa.get_email():
                self.query_one(
                    "#inpt_email", TextArea).text = self.pessoa.get_email()
            if self.pessoa.get_data_nascimento():
                self.query_one(
                    "#inpt_data_nascimento", MaskedInput).value = self.pessoa.get_data_nascimento().strftime("%d/%m/%Y")
            if self.pessoa.get_cpf_cnpj():
                cpf = str(self.pessoa.get_cpf_cnpj())
                cpf_formatado = (
                    cpf[:3] + "." +
                    cpf[3:6] + "." +
                    cpf[6:9] + "-" +
                    cpf[9:]
                )
                self.query_one("#inpt_cpf", MaskedInput).value = cpf_formatado
            if self.pessoa.get_rg():
                self.query_one("#inpt_rg", Input).value = str(
                    self.pessoa.get_rg())
            try:
                if self.pessoa.get_tipo():
                    self.query_one("#select_tabelas", Select).value = self.pessoa.get_tipo(
                    ).value.lower().capitalize()
            except Exception as e:
                print(e)

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
        if TextArea in self.query():
            for tx in self.query(TextArea):
                tx.text = ""
        if MaskedInput in self.query():
            for m_i in self.query(MaskedInput):
                m_i.value = ""
        if Input in self.query():
            for m_i in self.query(MaskedInput):
                m_i.value = ""

    def on_button_pressed(self):
        nome = self.query_one("#inpt_nome", TextArea).text
        email = self.query_one("#inpt_email", TextArea).text
        telefone = None
        data_nascimento = self.query_one(
            "#inpt_data_nascimento", MaskedInput)
        if data_nascimento._valid:
            data_nascimento = self.query_one(
                "#inpt_data_nascimento", MaskedInput).value.split("/")
            data_nascimento = datetime.datetime(
                year=data_nascimento[-1], month=data_nascimento[1], day=data_nascimento[0])
        else:
            data_nascimento = None
        cpf = self.query_one("#inpt_cpf", MaskedInput).value.strip()
        if cpf._valid:
            cpf = self.query_one("#inpt_cpf", MaskedInput).value.strip()
            if cpf != "":
                cpf = "".join(cpf.split("."))
                cpf = "".join(cpf.split("-"))
            else: 
                cpf = None
        else:
            self.notify("ERRO. CPF inválido")
            return
        rg = self.query_one("#inpt_rg", MaskedInput)
        if not rg._valid:
            rg = self.query_one("#inpt_rg", Input).value.strip()
            if rg != "":
                rg = int(rg)
            else: 
                rg = None
        else:
            rg = None

        match self.valor_select:
            case "Editar":
                cpf_pesquisa = self.query_one("#inpt_id_pesquisa", MaskedInput)
                if cpf_pesquisa._valid:
                    cpf = self.query_one(
                        "#inpt_id_pesquisa", MaskedInput).value
                else:
                    self.notify("ERRO. CPF inválido")
                    return

                if not self.pessoa():
                    match self.query_one("#select_tabelas", Select).value:
                        case "Cliente":
                            comprador = Cliente.Cliente(cpf_pesquisa,
                                                        nome, email, telefone, data_nascimento, cpf, rg)
                            atualizacao = Controller.editar_usuario(comprador)
                        case "Proprietario":
                            comprador = Proprietario.Proprietario(cpf_pesquisa,
                                                                  nome, email, telefone, data_nascimento, cpf, rg)
                            atualizacao = Controller.editar_proprietario(
                                comprador)
                        case "Corretor":
                            comprador = Corretor.Corretor(cpf_pesquisa,
                                                          nome, email, telefone, data_nascimento, cpf, rg)
                            atualizacao = Controller.editar_usuario(comprador)
                        case "Captador":
                            comprador = Captador.Captador(cpf_pesquisa,
                                                          nome, email, telefone, data_nascimento, cpf, rg)
                            atualizacao = Controller.editar_usuario(comprador)
                        case "Administrador":
                            comprador = Usuario.Usuario(cpf_pesquisa,
                                                        nome, email, telefone, data_nascimento, cpf, rg, tipo=Usuario.Tipo.ADMINISTRADOR)
                            atualizacao = Controller.editar_usuario(comprador)
                else:
                    self.pessoa.set_email(email)
                    self.pessoa.set_nome(nome)
                    self.pessoa.set_cpf_cnpj(cpf)
                    self.pessoa.set_rg(rg)
                    self.pessoa.set_data_nascimento(data_nascimento)
            
                    if isinstance(self.pessoa, Proprietario.Proprietario):
                        atualizacao = Controller.editar_proprietario(
                            self.pessoa)
                    else:
                        atualizacao = Controller.editar_usuario(self.pessoa)

                self.notify(atualizacao)
                self.limpar_text_area()

            case "Adicionar":
                if not self.pessoa():
                    match self.query_one("#select_tabelas", Select).value:
                        case "Comprador":
                            comprador = Cliente.Cliente(cpf_pesquisa,
                                                        nome, email, telefone, data_nascimento, cpf, rg)
                            atualizacao = Controller.cadastrar_usuario(
                                comprador)
                        case "Proprietario":
                            comprador = Proprietario.Proprietario(cpf_pesquisa,
                                                                  nome, email, telefone, data_nascimento, cpf, rg)
                            atualizacao = Controller.cadastrar_proprietario(
                                comprador)
                        case "Corretor":
                            comprador = Corretor.Corretor(cpf_pesquisa,
                                                          nome, email, telefone, data_nascimento, cpf, rg)
                            atualizacao = Controller.cadastrar_usuario(
                                comprador)
                        case "Captador":
                            comprador = Captador.Captador(cpf_pesquisa,
                                                          nome, email, telefone, data_nascimento, cpf, rg)
                            atualizacao = Controller.cadastrar_usuario(
                                comprador)
                        case "Administrador":
                            comprador = Usuario.Usuario(cpf_pesquisa,
                                                        nome, email, telefone, data_nascimento, cpf, rg, tipo=Usuario.Tipo.ADMINISTRADOR)
                            atualizacao = Controller.cadastrar_usuario(
                                comprador)
                else:
                    self.pessoa.set_email(email)
                    self.pessoa.set_nome(nome)
                    self.pessoa.set_cpf_cnpj(cpf)
                    self.pessoa.set_rg(rg)
                    self.pessoa.set_data_nascimento(data_nascimento)
                    
                    if isinstance(self.pessoa, Proprietario.Proprietario):
                        atualizacao = Controller.editar_proprietario(
                            self.pessoa)
                    else:
                        atualizacao = Controller.editar_usuario(self.pessoa)
                self.notify(atualizacao)
                self.limpar_text_area()

            case "Remover":
                cpf_pesquisa = self.query_one("#inpt_id_pesquisa", MaskedInput)
                if cpf_pesquisa._valid:
                    cpf_pesquisa = self.query_one(
                        "#inpt_id_pesquisa", MaskedInput).value
                else:
                    self.notify("ERRO. CPF inválido")
                    return

                if self.query_one("#select_tabelas", Select).value == "Proprietario":
                    remocao = Controller.remover(
                        "id_proprietario", cpf_pesquisa, "proprietario")
                else:
                    remocao = Controller.remover(
                        "id_usuario", cpf_pesquisa, "usuario")

                self.notify(remocao)
                self.limpar_text_area()

        self.limpar_text_area()
