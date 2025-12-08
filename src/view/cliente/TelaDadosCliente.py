import hashlib
from textual.screen import Screen
from textual.widgets import TextArea, Static, Tab, Tabs, Button, Footer, Header, MaskedInput, SelectionList, Input, Switch
from textual.containers import Grid

from model import Init, Usuario
from database.Banco import Banco

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
            yield TextArea(Init.usuario_atual.get_username(), id="inpt_username")
            yield Static("Nome")
            yield TextArea(Init.usuario_atual.get_nome(), id="inpt_nome")
            yield Static("CPF/CNPJ")
            yield MaskedInput(value=Init.usuario_atual.get_cpf_cnpj(), template="000.000.000-00", id="inpt_cpf")
            yield Static("RG")
            yield TextArea(Init.usuario_atual.get_rg(), id="inpt_rg")
            yield Static("Telefone")
            yield MaskedInput(value=Init.usuario_atual.get_telefone(), template="(00) 00000-0000", id="inpt_telefone")
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

    def on_screen_resume(self):
        pass

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.label == "Salvar":

            username = self.query_one("#inpt_username", TextArea).text.strip()
            nome = self.query_one("#inpt_nome", TextArea).text
            cpf_cnpj = self.query_one(
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

            if username != Init.usuario_atual.get_username() and username:
                alteracao = Banco.atualizar_comprador(
                    "username", username, Init.usuario_atual.get_cpf_cnpj())
                if alteracao:
                    Init.usuario_atual.set_username(username)
                else:
                    self.query_one("#stt_username", Static).content += "[red]X"

            if senha:
                senha_hash = hashlib.sha256(
                    senha.get_senha().encode('utf-8')).hexdigest()
                if senha_hash != Init.usuario_atual.get_senha():
                    alteracao = Banco.atualizar_comprador(
                        "senha", senha_hash, Init.usuario_atual.get_cpf_cnpj())
                    if alteracao:
                        Init.usuario_atual.set_senha(senha_hash)
                    else:
                        self.query_one(
                            "#stt_senha", Static).content += "[red]X"

            if email != Init.usuario_atual.get_email() and email:
                alteracao = Banco.atualizar_comprador(
                    "email", email, Init.usuario_atual.get_cpf_cnpj())
                if alteracao:
                    Init.usuario_atual.set_email(email)
                else:
                    self.query_one("#stt_email", Static).content += "[red]X"

            if nome != Init.usuario_atual.get_nome() and nome:
                alteracao = Banco.atualizar_comprador(
                    "nome", nome, Init.usuario_atual.get_cpf_cnpj())
                if alteracao:
                    Init.usuario_atual.set_nome(nome)
                else:
                    self.query_one("#stt_nome", Static).content += "[red]X"

            if cpf_cnpj != Init.usuario_atual.get_cpf_cnpj() and cpf_cnpj:
                alteracao = Banco.atualizar_comprador(
                    "cpf_cnpj", cpf_cnpj, Init.usuario_atual.get_cpf_cnpj())
                if alteracao:
                    Init.usuario_atual.set_cpf_cnpj(cpf_cnpj)
                else:
                    self.query_one("#stt_cpf_cnpj", Static).content += "[red]X"

            if rg != Init.usuario_atual.get_rg() and rg:
                alteracao = Banco.atualizar_comprador(
                    "rg", rg, Init.usuario_atual.get_cpf_cnpj())
                if alteracao:
                    Init.usuario_atual.set_rg(rg)
                else:
                    self.query_one("#stt_rg", Static).content += "[red]X"

            if telefone != Init.usuario_atual.get_telefone() and telefone:
                alteracao = Banco.atualizar_comprador(
                    "telefone", telefone, Init.usuario_atual.get_cpf_cnpj())
                if alteracao:
                    Init.usuario_atual.set_telefone(telefone)
                else:
                    self.query_one("#stt_telefone", Static).content += "[red]X"

            # if username != Init.usuario_atual.get_username() and username:
            # alteracao = Banco.atualizar_comprador("endereco")
            if data_nascimento != Init.usuario_atual.get_data_nascimento() and data_nascimento:
                alteracao = Banco.atualizar_comprador(
                    "data_nascimento", data_nascimento, Init.usuario_atual.get_cpf_cnpj())
                if alteracao:
                    Init.usuario_atual.set_data_nascimento(data_nascimento)
                else:
                    self.query_one("#stt_data_nascimento",
                                   Static).content += "[red]X"

            # mensagem = Controller.atualizar_dado_cliente(dados)

            # self.notify(mensagem, markup=False)

    def on_selection_list_selected_changed(self, evento: SelectionList.SelectedChanged):
        Init.usuario_atual.set_tipos_imoveis_desejados = evento.selection_list.selected

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_dados_cliente", Tab).id

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
