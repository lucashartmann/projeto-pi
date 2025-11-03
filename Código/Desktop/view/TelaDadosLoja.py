# Faturamento diario, mensal, anual, semestre
# Quantidade de produtos vendidos

from textual.screen import Screen
from textual.widgets import Tab, Tabs
from model.Usuario import TipoUsuario
from model import Init


class TelaDadosLoja(Screen):

    def compose(self):
        if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:

            yield Tabs(Tab("Cadastro Produto", id="tab_cadastro_produto"), Tab("Estoque", id="tab_estoque"), Tab("Cadastro Pessoa", id="tab_cadastro_pessoa"), Tab("Clientela", id="tab_clientela"), Tab("Cadastro Usuario", id="tab_cadastro_usuario"), Tab("Usuarios Cadastrados", id="tab_usuario_cadastrados"), Tab("Dados da Loja", id="tab_dados_loja"), Tab("Servidor", id="tab_servidor"))
        else:
            yield Tabs(Tab("Cadastro Produto", id="tab_cadastro_produto"), Tab("Estoque", id="tab_estoque"), Tab("Cadastro Pessoa", id="tab_cadastro_pessoa"), Tab("Clientela", id="tab_clientela"), Tab("Dados da Loja", id="tab_dados_loja"))

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
            self.app.switch_screen("tela_estoque")
        elif event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
            self.app.switch_screen("tela_pessoa")
        elif event.tabs.active == self.query_one("#tab_clientela", Tab).id:
            self.app.switch_screen("tela_clientela")
        elif event.tabs.active == self.query_one("#tab_cadastro_usuario", Tab).id:
            self.app.switch_screen("tela_usuario")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_dados_loja", Tab).id
