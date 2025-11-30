from textual.screen import Screen
from textual.widgets import TextArea, Static, Tab, Tabs, Button, Footer, Header, MaskedInput, Select, SelectionList, Input, Switch
from textual.containers import Grid
from model import Init, Administrador, Gerente, Cliente, Imovel
from controller import Controller
import datetime
import hashlib


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
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif isinstance(Init.usuario_atual, Cliente.Comprador):
            yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Dados", id="tab_dados_cliente"))

        with Grid():
            yield Static("Username")
            yield TextArea(Init.usuario_atual.get_username(), id="inpt_username")
            yield Static("Nome")
            yield TextArea(Init.usuario_atual.get_nome(), id="inpt_nome")
            yield Static("CPF/CNPJ")
            yield MaskedInput(Init.usuario_atual.get_cpf_cnpj(), template="000.000.000-00", id="inpt_cpf")
            yield Static("RG")
            yield TextArea(Init.usuario_atual.get_rg(), id="inpt_rg")
            yield Static("Telefone")
            yield MaskedInput(Init.usuario_atual.get_telefone(), template="(00) 00000-0000", id="inpt_telefone")
            # yield Static("Endereco")
            # yield TextArea(Init.usuario_atual.get_endereco())
            yield Static("Email")
            yield TextArea(Init.usuario_atual.get_email(), id="inpt_email")
            yield Static("Senha")
            yield MyInput(placeholder="mudar senha", id="inpt_senha", password=True)
            yield Static("Data de nascimento", id="stt_data_nascimento")
            yield MaskedInput(template="00/00/0000", id="inpt_data_nascimento")

        yield Static("Procurando por:")
        with Grid():
            yield SelectionList([(valor.value, valor) for valor in Imovel.Categoria], id="select_categoria")
            yield Static("Quartos")
            yield MaskedInput(template=00)
            yield Static("Banheiros")
            yield MaskedInput(template=00)
            yield Static("CEP desejado")
            yield MaskedInput(placeholder="00000-000")

        yield Button("Salvar")
        # yield Static("Imoveis do usuário", id="stt_compras")
        yield Footer(show_command_palette=False)

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.label == "Salvar":

            username = self.query_one("#inpt_username", TextArea).text.strip()
            nome = self.query_one("#inpt_nome", TextArea).text
            cpf = self.query_one(
                "#inpt_cpf", MaskedInput).text.strip().strip(".").strip("-")
            rg = self.query_one("#inpt_rg", TextArea).text.strip()
            telefone = self.query_one(
                "#inpt_telefone", MaskedInput).value.strip("(").strip(")")
            email = self.query_one("#inpt_email", TextArea).text.strip()
            senha = self.query_one("#inpt_senha", TextArea).text.strip()
            data_nascimento = self.query_one(
                "#inpt_cpf", MaskedInput).text.strip().split("/")
            data_nascimento = datetime.datetime(
                year=data_nascimento[-1], day=data_nascimento[0], month=data_nascimento[1])
            tipo_imoveis_desejados = evento.selection_list.selected
            quant_quartos_desejado = int(self.query_one(
                "", MaskedInput).text.strip())
            quant_banheiros_desejado = int(self.query_one(
                "", MaskedInput).text.strip())
            cep_desejado = int(self.query_one(
                "", MaskedInput).text.strip.strip("-"))

            # mensagem = Controller.atualizar_dado_cliente(dados)

            # self.notify(mensagem, markup=False)

    def on_selection_list_selected_changed(self, evento: SelectionList.SelectedChanged):
        Init.usuario_atual.set_tipos_imoveis_desejados = evento.selection_list.selected

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_dados_cliente", Tab).id

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:
            if not isinstance(Init.usuario_atual, Cliente.Comprador):
                if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
                    self.app.switch_screen("tela_estoque")
                elif event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                    self.app.switch_screen("tela_cadastro_imovel")
                elif event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                    self.app.switch_screen("tela_cadastro_pessoa")
                elif isinstance(Init.usuario_atual, Gerente.Gerente):
                    if event.tabs.active == self.query_one("#tab_dados_imobiliaria", Tab).id:
                        self.app.switch_screen("tela_dados_imobiliaria")
                elif isinstance(Init.usuario_atual, Administrador.Administrador):
                    if event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                        self.app.switch_screen("tela_servidor")
                elif event.tabs.active == self.query_one("#tab_comprar", Tab).id:
                    self.app.switch_screen("tela_estoque_cliente")
            else:
                if event.tabs.active == self.query_one("#tab_comprar", Tab).id:
                    self.app.switch_screen("tela_estoque_cliente")
        except:
            pass
