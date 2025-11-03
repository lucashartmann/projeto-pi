# Compras recentes de usuario
# Dados de login

from textual.screen import Screen
from textual.widgets import TextArea, Pretty, Static, Tab, Tabs, Button
from textual.containers import HorizontalGroup, Grid

from textual_image.widget import Image

from model import Init
from controller import Controller


class TelaDadosUsuario(Screen):

    CSS_PATH = "css/TelaDadosUsuario.tcss"

    compras = Init.loja.get_compras_usuario_por_cpf(
        Init.cliente_atual.get_cpf())

    def dados_compra(self):
        if self.compras:
            for chave, valor in self.compras.items():
                dados = ''

                dados += f"Data da Compra: {chave}\n"
                for produto in valor:
                    dados += f"{produto}\n"

                if dados:
                    self.mount(Pretty(dados))

    def atualizar_compras(self):
        self.compras = Init.loja.get_compras_usuario_por_cpf(
            Init.cliente_atual.get_cpf())

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_comprar", Tab).id:
            self.app.switch_screen("tela_estoque_cliente")
        elif event.tabs.active == self.query_one("#tab_carrinho_compras", Tab).id:
            self.app.switch_screen("tela_carrinho_compras")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.label == "Salvar":
            dados = []
            for ta in self.query_one(Grid).query(TextArea):
                texto = ta.text
                dados.append(texto)

            mensagem = Controller.editar_pessoa(
                Init.cliente_atual.get_cpf(), dados)

            self.notify(mensagem, markup=False)

    def atualizar_dados(self):
        grid = self.query_one(Grid)
        if Init.usuario:
            grid.mount(Static("Username"))
            grid.mount(TextArea(Init.usuario.get_nome()))
            grid.mount(Static("Nome"))
            grid.mount(TextArea(Init.cliente_atual.get_nome()))
            grid.mount(Static("CPF"))
            grid.mount(TextArea(Init.cliente_atual.get_cpf()))
            grid.mount(Static("RG"))
            grid.mount(TextArea(Init.cliente_atual.get_rg()))
            grid.mount(Static("Telefone"))
            grid.mount(TextArea(Init.cliente_atual.get_telefone()))
            grid.mount(Static("Endereco"))
            grid.mount(TextArea(Init.cliente_atual.get_endereco()))
            grid.mount(Static("Email"))
            grid.mount(TextArea(Init.cliente_atual.get_email()))
            grid.mount(Static("Senha"))
            grid.mount(TextArea(Init.usuario.get_senha()))

    def compose(self):
        yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Carrinho", id="tab_carrinho_compras"), Tab("Dados", id="tab_dados_usuario"))
        with HorizontalGroup():

            yield Image("assets/usuario2.png")
            with Grid():
                yield Static("Username")
                yield TextArea(Init.usuario.get_nome())
                yield Static("Nome")
                yield TextArea(Init.cliente_atual.get_nome())
                yield Static("CPF")
                yield TextArea(Init.cliente_atual.get_cpf())
                yield Static("RG")
                yield TextArea(Init.cliente_atual.get_rg())
                yield Static("Telefone")
                yield TextArea(Init.cliente_atual.get_telefone())
                yield Static("Endereco")
                yield TextArea(Init.cliente_atual.get_endereco())
                yield Static("Email")
                yield TextArea(Init.cliente_atual.get_email())
                yield Static("Senha")
                yield TextArea("*******")
        yield Button("Salvar")
        yield Static("Compras recentes do usuário", id="stt_compras")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_dados_usuario", Tab).id
