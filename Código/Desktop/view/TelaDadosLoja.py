# Faturamento diario, mensal, anual, semestre
# Quantidade de produtos vendidos

from textual.screen import Screen
from textual.widgets import Tab, Tabs, Static
from textual.containers import VerticalGroup


from model.Usuario import TipoUsuario
from model import Init


class TelaDadosLoja(Screen):

    def compose(self):
        if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:
            yield Tabs(Tab("Cadastro Produto", id="tab_cadastro_produto"), Tab("Estoque", id="tab_estoque"),  Tab("Servidor", id="tab_servidor"))
        else:
            yield Tabs(Tab("Cadastro Produto", id="tab_cadastro_produto"), Tab("Estoque", id="tab_estoque"), Tab("Cadastro Pessoa", id="tab_cadastro_pessoa"), Tab("Dados da Loja", id="tab_dados_loja"))

    def on_mount(self):
        self.atualizar()

    def atualizar(self):
        container = VerticalGroup()
        self.mount(container)
        container.mount(Static("Faturamento Diário:"))
        container.mount(Static("R$ XXXX,XX"))
        container = VerticalGroup()
        self.mount(container)
        container.mount(Static("Faturamento Mensal:"))
        container.mount(Static("R$ XXXX,XX"))
        container = VerticalGroup()
        self.mount(container)
        container.mount(Static("Faturamento Anual:"))
        container.mount(Static("R$ XXXX,XX"))
        container = VerticalGroup()
        self.mount(container)
        container.mount(Static("Faturamento Semestral:"))
        container.mount(Static("R$ XXXX,XX"))
        container = VerticalGroup()
        self.mount(container)
        container.mount(Static("Quantidade de produtos"))
        container.mount(Static("0"))
        container = VerticalGroup()
        self.mount(container)
        container.mount(Static("Quantidade de clientes"))
        container.mount(Static("0"))
        container = VerticalGroup()
        self.mount(container)
        container.mount(Static("Quantidade de funcionarios"))
        container.mount(Static("0"))
        container = VerticalGroup()
        self.mount(container)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
            self.app.switch_screen("tela_estoque")
        elif event.tabs.active == self.query_one("#tab_cadastro", Tab).id:
            self.app.switch_screen("tela_cadastro")
        
        if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:
            if event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                self.app.switch_screen("tela_servidor")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_dados_loja", Tab).id
