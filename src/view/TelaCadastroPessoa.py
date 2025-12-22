import datetime
from textual.widgets import Button, Tab, Tabs, Select, Footer, Static, TextArea, MaskedInput, Input
from textual.screen import Screen, ModalScreen
from textual.containers import HorizontalGroup, Vertical, Horizontal
from controller import Controller
from model import Init, Usuario, Captador, Cliente, Corretor, Proprietario, Gerente, Endereco
from utils.Widgets import Header, ResponsiveGrid, MyInput
from textual.validation import Length
import requests


class PopUp(ModalScreen):

    TITLE = "Salvar"

    def compose(self):
        yield Header()
        with Vertical(id="dialog"):
            yield Static("Usuário não salvo, deseja continuar?")
            with Horizontal():
                yield Button("Confirmar", id="bt_confirmar")
                yield Button("Cancelar", id="bt_cancelar")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_confirmar":
            self.app.get_screen(
                "tela_cadastro_imovel").confirmar_salvamento = True
            self.app.pop_screen()
        elif evento.button.id == "bt_cancelar":
            self.app.get_screen(
                "tela_cadastro_imovel").confirmar_salvamento = False
            self.app.pop_screen()


class PopUpApagar(ModalScreen):

    TITLE = "Apagar"

    def compose(self):
        yield Header()
        with Vertical(id="dialog"):
            yield Static("Certeza que deseja apagar?")
            with Horizontal():
                yield Button("Confirmar", id="bt_confirmar")
                yield Button("Cancelar", id="bt_cancelar")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_confirmar":
            cpf = self.query_one("#inpt_cpf", MaskedInput)
            if cpf._valid:
                cpf = cpf.value.strip()
                cpf = "".join(cpf.split("."))
                cpf = "".join(cpf.split("-"))
                if cpf == "":
                    self.notify("ERRO. CPF inválido")
                    return
            else:
                self.notify("ERRO. CPF inválido")
                return

            if self.query_one("#select_tabelas", Select).value == "Proprietario":
                remocao = Controller.remover(
                    "id_proprietario", cpf, "proprietario")
            else:
                remocao = Controller.remover(
                    "id_usuario", cpf, "usuario")

            self.app.get_screen("tela_cadastro_pessoa").notify(remocao)
            self.app.get_screen("tela_cadastro_pessoa").acao == True
            self.app.pop_screen()

        elif evento.button.id == "bt_cancelar":
            self.app.pop_screen()


class TelaCadastroPessoa(Screen):

    CSS_PATH = "css/TelaCadastroPessoa.tcss"

    valor_select = ""
    tabela = "products"
    montados = list()
    montou_remover = False
    montou_editar = False
    perfis = None
    perfil_atual = None
    acao = False

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
        with Horizontal(id="h_buttons"):
            yield Button("Apagar", id="bt_apagar_cadastro", variant="warning")
            yield Button("Salvar", id="bt_salvar_alteracoes", variant="success")
        with ResponsiveGrid():
            if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
                yield Static("Username", id="stt_username")
                yield TextArea(placeholder="username aqui", id="inpt_username")
                yield Static("Senha", id="stt_senha")
                yield MyInput(placeholder="senha aqui", id="inpt_senha")
            else:
                yield Static("[red]*[/]Nome", id="stt_nome")
                yield TextArea(placeholder="nome aqui", id="inpt_nome")
                yield Static("[red]*[/]Email", id="stt_email")
                yield TextArea(placeholder="email aqui", id="inpt_email")
                yield Static("Telefone", id="stt_telefone")
                with HorizontalGroup(id="container_telefones"):
                    yield MaskedInput(template="(00) 00000-0000", classes="inpt_telefone")
                    yield Button("+", id="bt_mais_numero")
                    yield Button("X", id="bt_remover_numero")
                yield Static("CEP", id="stt_cep")
                yield MaskedInput(template="00000-000", id="ta_cep", validators=Length(minimum=9, maximum=9), valid_empty=False)
                yield Static("Rua", id="stt_rua")
                yield TextArea(disabled=True, id="ta_rua")
                yield Static("Número do endereço", id="stt_numero")
                yield Input(id="ta_numero", type="integer", valid_empty=True)
                yield Static("Complemento do endereço", id="stt_complemento")
                yield TextArea(id="ta_complemento")
                yield Static("Bloco do endereço", id="stt_bloco")
                yield TextArea(id="ta_bloco")
                yield Static("Bairro", id="stt_bairro")
                yield TextArea(disabled=True, id="ta_bairro")
                yield Static("Cidade", id="stt_cidade")
                yield TextArea(disabled=True, id="ta_cidade")
                yield Static("Estado", id="stt_estado")
                yield MaskedInput(disabled=True, template="XX", id="ta_estado", validators=Length(minimum=2, maximum=2))
                yield Static("Data de nascimento", id="stt_data_nascimento")
                yield MaskedInput(template="00/00/0000", id="inpt_data_nascimento", validators=Length(minimum=10, maximum=10), valid_empty=True)
                yield Static("[red]*[/]CPF", id="stt_cpf")
                yield MaskedInput(template="000.000.000-00", id="inpt_cpf", validators=Length(minimum=11, maximum=14), valid_empty=True)
                yield Static("RG", id="stt_rg")
                yield Input(id="inpt_rg", placeholder="RG aqui", validators=Length(minimum=7, maximum=9), valid_empty=True)
                yield Static("Salário", id="stt_salario")
                yield Input(id="inpt_salario", type="number")
                yield Static("Creci", id="stt_creci")
                yield MaskedInput(
                    id="inpt_creci", template="000000", validators=Length(minimum=6, maximum=6), valid_empty=True)
        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            yield Select([("Cliente", "Cliente"), (
                "Proprietario", "Proprietario"), ("Corretor", "Corretor"), ("Captador", "Captador"), ("Gerente", "Gerente")], allow_blank=False, id="select_tabelas")
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
            yield Select([("Cliente", "Cliente"), (
                "Proprietario", "Proprietario"), ("Corretor", "Corretor"), ("Captador", "Captador")], allow_blank=False, id="select_tabelas")
        else:
            yield Select([("Cliente", "Cliente"), (
                "Proprietario", "Proprietario")], allow_blank=False, id="select_tabelas")

        with Vertical(id="imoveis"):
            pass

            # yield Button("Executar")
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
        if self.pessoa:
            if self.pessoa.get_endereco():
                self.query_one(
                    "#ta_rua", TextArea).text = self.pessoa.get_endereco().get_rua()
                if self.pessoa.get_endereco().get_numero() is not None:
                    self.query_one(
                        "#ta_numero", Input).value = str(self.pessoa.get_endereco().get_numero())
                if self.pessoa.get_complemento() is not None:
                    self.query_one(
                        "#ta_complemento", TextArea).text = self.pessoa.get_complemento()
                if self.pessoa.get_bloco() is not None:
                    self.query_one(
                        "#ta_bloco", TextArea).text = self.pessoa.get_bloco()
                cep = str(self.pessoa.get_endereco().get_cep())
                cep = cep[:5] + "-" + cep[5:]
                self.query_one(
                    "#ta_cep", MaskedInput).value = cep
                self.query_one(
                    "#ta_bairro", TextArea).text = self.pessoa.get_endereco().get_bairro()
                self.query_one(
                    "#ta_cidade", TextArea).text = self.pessoa.get_endereco().get_cidade()
                self.query_one(
                    "#ta_estado", MaskedInput).value = self.pessoa.get_endereco().get_uf()

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

    # def limpar_text_area(self):
    #     if TextArea in self.query():
    #         for tx in self.query(TextArea):
    #             tx.text = ""
    #     if MaskedInput in self.query():
    #         for m_i in self.query(MaskedInput):
    #             m_i.value = ""
    #     if Input in self.query():
    #         for m_i in self.query(MaskedInput):
    #             m_i.value = ""

    def on_select_changed(self, evento: Select.Changed):
        self.query_one("#inpt_salario").styles.display = "none"
        self.query_one("#stt_salario").styles.display = "none"
        self.query_one("#stt_creci").styles.display = "none"
        self.query_one("#inpt_creci").styles.display = "none"

        match evento.select.value:
            case "Cliente":
                pass
            case "Proprietario":
                pass
            case "Corretor":
                self.query_one("#stt_creci").styles.display = "block"
                self.query_one("#inpt_creci").styles.display = "block"
            case "Captador":
                self.query_one("#inpt_salario").styles.display = "block"
                self.query_one("#stt_salario").styles.display = "block"
            case "Gerente":
                self.query_one("#inpt_salario").styles.display = "block"
                self.query_one("#stt_salario").styles.display = "block"

    def on_button_pressed(self, evento: Button.Pressed):

        match evento.button.id:
            case "bt_apagar_cadastro":
                self.app.push_screen(PopUpApagar())

            case "bt_mais_numero":
                valor = self.query_one(
                    "#container_telefones").query_one(MaskedInput).value
                self.query_one("#container_telefones").remove_children(
                    MaskedInput)
                self.query_one("#container_telefones").mount(MaskedInput(template="(00) 00000-0000",
                                                                         classes="inpt_telefone"), before=self.query_one("#container_telefones").query_one(Button))
                self.query_one(ResponsiveGrid).mount(MaskedInput(template="(00) 00000-0000", classes="inpt_telefone",
                                                                 value=valor), after=self.query_one(ResponsiveGrid).query_one("#stt_telefone"))
                self.query_one("#container_telefones").query_one(
                    "#bt_remover_numero").styles.display = "block"

            case "bt_remover_numero":
                lista = list(self.query_one(
                    ResponsiveGrid).query(".inpt_telefone"))

                self.query_one(ResponsiveGrid).remove_children(
                    [lista[-1], lista[-2]])

                self.query_one("#container_telefones").mount(MaskedInput(template="(00) 00000-0000", classes="inpt_telefone",
                                                                         value=lista[-2].value), before=self.query_one("#container_telefones").query_one(Button))

                if len(lista) <= 2:

                    self.query_one("#container_telefones").query_one(
                        "#bt_remover_numero").styles.display = "none"

            case "bt_salvar_alteracoes":
                try:
                    username = self.query_one("#inpt_username", TextArea).text
                    senha = self.query_one("#inpt_senha", MyInput).value
                    creci = self.query_one("#inpt_creci", MaskedInput)
                    salario = self.query_one("#inpt_salario", Input).value
                    if salario != "":
                        salario = float(salario)
                    else:
                        salario = None
                    if creci._valid and creci.value != "":
                        creci = creci.value
                    else:
                        creci = None
                except:
                    pass
                rua = self.query_one("#ta_rua", TextArea).text
                numero = self.query_one(
                    "#ta_numero", Input).value
                if numero != "":
                    numero = int(numero)
                else:
                    self.notify("ERRO! Insira o número do endereço")
                    return
                complemento = self.query_one(
                    "#ta_complemento", TextArea).text.strip()
                bloco = self.query_one("#ta_bloco", TextArea).text.strip()
                cep = self.query_one(
                    "#ta_cep", MaskedInput)
                if not cep._valid or cep == "":
                    cep = None
                else:
                    cep = self.query_one(
                        "#ta_cep", MaskedInput).value.strip()
                    cep = int("".join(cep.split("-")))
                if cep is not None:
                    bairro = self.query_one("#ta_bairro", TextArea).text
                    cidade = self.query_one("#ta_cidade", TextArea).text
                    estado = self.query_one(
                        "#ta_estado", MaskedInput)
                    if estado._valid:
                        estado = self.query_one(
                            "#ta_estado", MaskedInput).value.strip()
                        if estado != "":
                            estado = estado
                        else:
                            estado = None
                    else:
                        estado = None
                nome = self.query_one("#inpt_nome", TextArea).text
                if not nome:
                    nome = None
                email = self.query_one("#inpt_email", TextArea).text
                if not email:
                    email = None
                telefones = []

                for input in self.query_one(ResponsiveGrid).query(".inpt_telefone"):
                    if input._valid and input.value != "":
                        numero = input.value
                        numero = "".join(numero.split("("))
                        numero = "".join(numero.split(")"))
                        numero = "".join(numero.split("-"))
                        numero = numero.strip()
                        telefones.append(numero)

                data_nascimento = self.query_one(
                    "#inpt_data_nascimento", MaskedInput)
                if data_nascimento._valid and data_nascimento.value != "":
                    data_nascimento = self.query_one(
                        "#inpt_data_nascimento", MaskedInput).value.split("/")
                    if "".join(data_nascimento) != "":
                        data_nascimento = datetime.datetime(
                            year=data_nascimento[-1], month=data_nascimento[1], day=data_nascimento[0])
                    else:
                        data_nascimento = None
                else:
                    data_nascimento = None

                cpf = self.query_one("#inpt_cpf", MaskedInput)
                if cpf._valid:
                    cpf = cpf.value.strip()
                    cpf = "".join(cpf.split("."))
                    cpf = "".join(cpf.split("-"))
                    if cpf == "":
                        self.notify("ERRO. CPF inválido")
                        return
                else:
                    self.notify("ERRO. CPF inválido")
                    return

                rg = self.query_one("#inpt_rg", MaskedInput)
                if not rg._valid and rg.value != "":
                    rg = int(rg.value.strip())
                else:
                    rg = None

                if cep is not None:
                    endereco = Endereco.Endereco(rua, bairro,
                                                 cep, cidade, estado)
                    endereco.set_numero(numero)
                else:
                    endereco = None

                if not self.pessoa():
                    match self.query_one("#select_tabelas", Select).value:
                        case "Cliente":
                            pessoa = Cliente.Cliente(
                                username, senha, email, nome, cpf)
                        case "Proprietario":
                            pessoa = Proprietario.Proprietario(
                                email, nome, cpf)
                        case "Corretor":
                            pessoa = Corretor.Corretor(
                                username, senha, email, nome, cpf, creci)
                        case "Captador":
                            pessoa = Captador.Captador(
                                username, senha, email, nome, cpf)
                        case "Administrador":
                            pessoa = Usuario.Usuario(
                                username, senha, email, nome, cpf, tipo=Usuario.Tipo.ADMINISTRADOR)

                    pessoa.set_rg(rg)
                    pessoa.set_data_nascimento(data_nascimento)
                    pessoa.set_telefones(telefones)
                    if endereco:
                        pessoa.set_endereco(endereco)
                    # pessoa.set_username(username)
                    # pessoa.set_senha(senha)

                    atualizacao = Controller.cadastrar_usuario(
                        pessoa)

                    atualizacao = Controller.cadastrar_proprietario(
                        pessoa)
                else:
                    pessoa = self.pessoa
                    # pessoa.set_username(username)
                    # pessoa.set_senha(senha)
                    pessoa.set_email(email)
                    pessoa.set_nome(nome)
                    pessoa.set_cpf_cnpj(cpf)
                    pessoa.set_rg(rg)
                    pessoa.set_data_nascimento(data_nascimento)
                    pessoa.set_email(email)
                    pessoa.set_telefones(telefones)
                    if endereco:
                        pessoa.set_endereco(endereco)

                    if isinstance(self.pessoa, Corretor.Corretor):
                        pessoa.set_creci(creci)
                    elif isinstance(self.pessoa, Gerente.Gerente) or isinstance(self.pessoa, Captador.Captador):
                        pessoa.set_salario(salario)

                    if isinstance(self.pessoa, Proprietario.Proprietario):
                        atualizacao = Controller.editar_proprietario(
                            self.pessoa)
                    else:
                        atualizacao = Controller.editar_usuario(self.pessoa)

                self.notify(atualizacao)

    def on_input_changed(self, evento: MaskedInput.Changed):
        self.salvo = False
        if evento.input.id == "ta_cep" and not self.imovel:
            cep = str(evento.input.value.strip())
            self.query_one("#ta_bairro", TextArea).clear()
            self.query_one("#ta_estado", MaskedInput).clear()
            self.query_one("#ta_rua", TextArea).clear()
            self.query_one("#ta_cidade", TextArea).clear()
            if len(cep) > 8:
                try:
                    link = f"https://viacep.com.br/ws/{cep}/json/"
                    requisicao = requests.get(link)
                    dados = requisicao.json()
                    logradouro = dados["logradouro"]
                    bairro = dados["bairro"]
                    cidade = dados["localidade"]
                    uf = dados["uf"]
                    self.query_one("#ta_bairro", TextArea).text = bairro
                    self.query_one("#ta_estado", MaskedInput).value = uf
                    self.query_one("#ta_rua", TextArea).text = logradouro
                    self.query_one("#ta_cidade", TextArea).text = cidade
                except Exception as e:
                    self.notify("ERRO! CEP inválido")
