from textual.screen import Screen
from textual.widgets import TextArea, Static, Tab, Tabs, Button, Footer, Header
from textual.containers import Grid

from model import Init, Administrador, Gerente, Cliente
from controller import Controller


class TelaDadosCliente(Screen):

    CSS_PATH = "css/TelaDadosUsuario.tcss"

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

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.label == "Salvar":
            dados = []
            for ta in self.query_one(Grid).query(TextArea):
                texto = ta.text
                dados.append(texto)

            mensagem = Controller.atualizar_dado_cliente(dados)

            self.notify(mensagem, markup=False)

    TITLE = "Tela de dados"

    def compose(self):
        yield Header()
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"), Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))

        else:
            yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Dados", id="tab_dados_cliente"))
        with Grid():
            yield Static("Username")
            yield TextArea(Init.usuario_atual.get_nome())
            yield Static("Nome")
            yield TextArea(Init.usuario_atual.get_nome())
            yield Static("CPF")
            yield TextArea(Init.usuario_atual.get_cpf_cnpj())
            yield Static("RG")
            yield TextArea(Init.usuario_atual.get_rg())
            yield Static("Telefone")
            yield TextArea(Init.usuario_atual.get_telefone())
            yield Static("Endereco")
            yield TextArea(Init.usuario_atual.get_endereco())
            yield Static("Email")
            yield TextArea(Init.usuario_atual.get_email())
            yield Static("Senha")
            yield TextArea(Init.usuario_atual.get_senha())
        yield Button("Salvar")
        # yield Static("Imoveis do usuário", id="stt_compras")
        yield Footer(show_command_palette=False)

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_dados_cliente", Tab).id
