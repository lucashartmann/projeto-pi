import hashlib
from textual.screen import Screen
from textual.containers import Grid
from textual.widgets import TextArea, Static, Tab, Tabs, Button, Footer, MaskedInput, SelectionList, Input, Switch
from utils.Widgets import Header
from textual.validation import Length
from model import Init, Usuario
from controller import Controller
import datetime


class MyInput(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Switch()

    def on_mount(self):
        self.query_one(Switch).styles.dock = "right"

    def on_switch_changed(self, evento: Switch.Changed):
        if evento.switch.value == True:
            self.password = False
        else:
            self.password = True


class TelaDadosCliente(Screen):

    CSS_PATH = "css/TelaDadosUsuario.tcss"
    TITLE = "Tela de dados"

    def compose(self):
        yield Header()
        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.CLIENTE:
            yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Dados", id="tab_dados_cliente"))

        with Grid():
            yield Static("Username")
            yield TextArea(id="inpt_username")
            yield Static("Nome")
            yield TextArea(id="inpt_nome")
            yield Static("CPF/CNPJ")
            yield MaskedInput(template="000.000.000-00", id="inpt_cpf", validators=Length(minimum=11, maximum=14), valid_empty=True)
            yield Static("RG")
            yield Input(id="inpt_rg", placeholder="RG aqui", validators=Length(minimum=7, maximum=9), valid_empty=True)
            # yield Static("Telefone")
            # yield MaskedInput(template="(00) 00000-0000", id="inpt_telefone")
            # yield Static("Endereco")
            # yield TextArea(Init.usuario_atual.get_endereco())
            yield Static("Email")
            yield TextArea(id="inpt_email")
            yield Static("Senha")
            yield MyInput(placeholder="alterar senha", id="inpt_senha", password=True)
            yield Static("Data de nascimento", id="stt_data_nascimento")
            yield MaskedInput(template="00/00/0000", id="inpt_data_nascimento", validators=Length(minimum=10, maximum=10), valid_empty=True)

        yield Static("Procurando por:")
        with Grid():
            # yield SelectionList([(valor.value, valor.value) for valor in Imovel.Categoria], id="select_categoria")
            yield Static("Quartos")
            yield MaskedInput(template="00")
            yield Static("Banheiros")
            yield MaskedInput(template="00")
            yield Static("CEP desejado")
            yield MaskedInput(template="00000-000")

        yield Button("Salvar")
        # yield Static("Imoveis do usuário", id="stt_compras")
        yield Footer(show_command_palette=False)

    def on_mount(self):
        self.atualizar()

    def atualizar(self):
        if Init.usuario_atual.get_username():
            self.query_one("#inpt_username",
                           TextArea).text = Init.usuario_atual.get_username()
        if Init.usuario_atual.get_nome():
            self.query_one(
                "#inpt_nome", TextArea).text = Init.usuario_atual.get_nome()
        if Init.usuario_atual.get_cpf_cnpj():
            cpf = str(Init.usuario_atual.get_cpf_cnpj())
            cpf_formatado = (
                cpf[:3] + "." +
                cpf[3:6] + "." +
                cpf[6:9] + "-" +
                cpf[9:]
            )
            self.query_one(
                "#inpt_cpf", MaskedInput).value = cpf_formatado
        if Init.usuario_atual.get_rg():
            self.query_one(
                "#inpt_rg", Input).value = Init.usuario_atual.get_rg()

        if Init.usuario_atual.get_email():
            self.query_one(
                "#inpt_email", TextArea).text = Init.usuario_atual.get_email()

        # self.query_one( MaskedInput(value=Init.usuario_atual.get_telefone(), template="(00) 00000-0000", id="inpt_telefone")

        # self.query_one( TextArea(Init.usuario_atual.get_endereco())

        # self.query_one( MyInput(placeholder="mudar senha", id="inpt_senha", password=True)

        # self.query_one( MaskedInput(template="00/00/0000", id="inpt_data_nascimento")

        # self.query_one( MaskedInput(template="00")

        # self.query_one( MaskedInput(template="00")

        # self.query_one( MaskedInput(template="00000-000")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.label == "Salvar":

            username = self.query_one("#inpt_username", TextArea).text.strip()
            nome = self.query_one("#inpt_nome", TextArea).text
            # telefone = self.query_one(
            #     "#inpt_telefone", MaskedInput).value.strip("(").strip(")")
            email = self.query_one("#inpt_email", TextArea).text.strip()
            senha = self.query_one("#inpt_senha", TextArea).text.strip()
            data_nascimento = self.query_one(
                "#inpt_data_nascimento", MaskedInput)
            if data_nascimento._valid:
                data_nascimento = self.query_one(
                    "#inpt_data_nascimento", MaskedInput).value.split("/")
                data_nascimento = datetime.datetime(
                    year=data_nascimento[-1], month=data_nascimento[1], day=data_nascimento[0])
            else:
                data_nascimento = None
            cpf_cnpj = self.query_one("#inpt_cpf", MaskedInput).value.strip()
            if cpf_cnpj._valid:
                cpf_cnpj = self.query_one(
                    "#inpt_cpf", MaskedInput).value.strip()
                if cpf_cnpj != "":
                    cpf_cnpj = "".join(cpf_cnpj.split("."))
                    cpf_cnpj = "".join(cpf_cnpj.split("-"))
                else:
                    cpf_cnpj = None
            else:
                self.notify("ERRO. cpf_cnpj inválido")
                return
            rg = self.query_one("#inpt_rg", Input)
            if not rg._valid:
                rg = self.query_one("#inpt_rg", Input).value.strip()
                if rg != "":
                    rg = int(rg)
                else:
                    rg = None
            else:
                rg = None

            tipo_imoveis_desejados = evento.selection_list.selected
            quant_quartos_desejado = int(self.query_one(
                "", MaskedInput).text.strip())
            quant_banheiros_desejado = int(self.query_one(
                "", MaskedInput).text.strip())
            cep_desejado = int(self.query_one(
                "", MaskedInput).text.strip.strip("-"))

            Init.usuario_atual.set_username(username)

            if senha:
                senha_hash = hashlib.sha256(
                    senha.get_senha().encode('utf-8')).hexdigest()
                Init.usuario_atual.set_senha(senha_hash)

            Init.usuario_atual.set_email(email)
            Init.usuario_atual.set_nome(nome)
            Init.usuario_atual.set_cpf_cnpj(cpf_cnpj)
            Init.usuario_atual.set_rg(rg)

            # Init.usuario_atual.set_telefones(telefones)

            Init.usuario_atual.set_data_nascimento(data_nascimento)

            mensagem = Controller.editar_usuario(Init.usuario_atual)

            self.notify(mensagem, markup=False)

    def on_selection_list_selected_changed(self, evento: SelectionList.SelectedChanged):
        Init.usuario_atual.set_tipos_imoveis_desejados = evento.selection_list.selected

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_dados_cliente", Tab).id
        self.atualizar()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:
            if event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                self.app.switch_screen("tela_cadastro_pessoa")

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

            elif event.tabs.active == self.query_one("#tab_atendimento", Tab).id:
                self.app.switch_screen("tela_atendimento")

            elif event.tabs.active == self.query_one("#tab_cadastro_venda_aluguel", Tab).id:
                self.app.switch_screen("tela_cadastro_venda_aluguel")

        except:
            pass
