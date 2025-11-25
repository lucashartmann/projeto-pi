from textual.app import App
from textual.binding import Binding

from model import Init

from view import TelaCadastroPessoa, TelaLogin, TelaEstoque, TelaCadastroImovel, TelaCadastroVendaAluguel
from view.cliente import TelaDadosCliente, TelaEstoqueCliente, TelaDadosImovel
from view.admin import TelaServidor
from view.gerente import TelaDadosImobiliaria


class App(App):
    CSS_PATH = "css/Base.tcss"

    SCREENS = {
        "tela_cadastro_pessoa": TelaCadastroPessoa.TelaCadastroPessoa,
        "tela_cadastro_imovel": TelaCadastroImovel.TelaCadastroImovel,
        "tela_login": TelaLogin.TelaLogin,
        "tela_estoque": TelaEstoque.TelaEstoque,
        "tela_estoque_cliente": TelaEstoqueCliente.TelaEstoqueCliente,
        "tela_dados_cliente": TelaDadosCliente.TelaDadosCliente,
        "tela_dados_imobiliaria": TelaDadosImobiliaria.TelaDadosImobiliaria,
        "tela_servidor": TelaServidor.TelaServidor,
        "tela_dados_imovel": TelaDadosImovel.TelaDadosImovel,
        "tela_cadastro_venda_aluguel": TelaCadastroVendaAluguel.TelaCadastroVendaAluguel
    }

    BINDINGS = {
        Binding("ctrl+q", "app.quit", "Sair"),
    }

    def on_mount(self):
        Init.inicializar()
        self.push_screen("tela_login")

    def action_cadastro(self):
        tela_login = self.get_screen("tela_login")
        tela_login.montar_cadastro()

    def action_voltar(self):
        tela_login = self.get_screen("tela_login")
        tela_login.voltar()
