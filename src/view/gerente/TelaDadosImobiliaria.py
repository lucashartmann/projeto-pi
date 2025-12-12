# Faturamento diario, mensal, anual, semestre
# Quantidade de imoveis vendidos

from textual.screen import Screen
from textual.widgets import Tab, Tabs, Static, Header, Footer
from textual.containers import VerticalGroup, Grid


from model import Init, Usuario


class TelaDadosImobiliaria(Screen):

    CSS_PATH = "css/TelaDadosImobiliaria.tcss"

    def compose(self):
        yield Header()
        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
            yield Tabs(Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"),
                       Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Estoque", id="tab_estoque"))
        yield Grid()
        yield Footer(show_command_palette=False)

    def on_mount(self):
        self.atualizar()

    def atualizar(self):
        container = VerticalGroup()
        self.query_one(Grid).mount(container)
        container.mount(Static("Faturamento Diário:"))
        container.mount(Static("R$ XXXX,XX", classes="valor"))
        container = VerticalGroup()
        self.query_one(Grid).mount(container)
        container.mount(Static("Faturamento Mensal:"))
        container.mount(Static("R$ XXXX,XX", classes="valor"))
        container = VerticalGroup()
        self.query_one(Grid).mount(container)
        container.mount(Static("Faturamento Anual:"))
        container.mount(Static("R$ XXXX,XX", classes="valor"))
        container = VerticalGroup()
        self.query_one(Grid).mount(container)
        container.mount(Static("Faturamento Semestral:"))
        container.mount(Static("R$ XXXX,XX", classes="valor"))
        container = VerticalGroup()
        self.query_one(Grid).mount(container)
        container.mount(Static("Quantidade de imoveis"))
        container.mount(Static("0", classes="valor"))
        container = VerticalGroup()
        self.query_one(Grid).mount(container)
        container.mount(Static("Quantidade de clientes"))
        container.mount(Static("0", classes="valor"))
        container = VerticalGroup()
        self.query_one(Grid).mount(container)
        container.mount(Static("Quantidade de funcionarios"))
        container.mount(Static("0", classes="valor"))

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:
            if event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                self.app.switch_screen("tela_cadastro_pessoa")

            elif event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                self.app.switch_screen("tela_cadastro_imovel")

            elif event.tabs.active == self.query_one("#tab_estoque", Tab).id:
                self.app.switch_screen("tela_estoque")

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
            "#tab_dados_imobiliaria", Tab).id
