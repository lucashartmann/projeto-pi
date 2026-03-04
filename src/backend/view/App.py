from textual.app import App
from textual.binding import Binding
from view.cliente import dados_cliente, dados_imovel
from view import atendimento, cadastro_pessoa, estoque, login
from model import Init
from view import cadastro_imovel
from view.cliente import estoque_cliente
from view.corretor import cadastro_venda_aluguel
from view.gerente import dados_imobiliaria
from textual import events


class App(App):
    CSS_PATH = "css/base.tcss"

    SCREENS = {
        "tela_cadastro_pessoa": cadastro_pessoa.TelaCadastroPessoa,
        "tela_cadastro_imovel": cadastro_imovel.TelaCadastroImovel,
        "tela_login": login.TelaLogin,
        "tela_estoque": estoque.TelaEstoque,
        "tela_estoque_cliente": estoque_cliente.TelaEstoqueCliente,
        "tela_dados_cliente": dados_cliente.TelaDadosCliente,
        "tela_dados_imobiliaria": dados_imobiliaria.TelaDadosImobiliaria,
        "tela_dados_imovel": dados_imovel.TelaDadosImovel,
        "tela_cadastro_venda_aluguel": cadastro_venda_aluguel.TelaCadastroVendaAluguel,
        "tela_atendimento": atendimento.TelaAtendimento,
    }

    BINDINGS = {
        Binding("ctrl+q", "app.quit", "Sair"),
    }

    WIDTH_BREAKPOINS = {
        34: "tamanho-34",
        64: "tamanho-64",
        98: "tamanho-98",
        128: "tamanho-128",
        192: "tamanho-192",
    }

    def on_resize(self, event: events.Resize) -> None:
        for cls in self.WIDTH_BREAKPOINS.values():
            self.remove_class(cls)

        print(event.size.width)

        for w in sorted(self.WIDTH_BREAKPOINS, reverse=True):
            if event.size.width > w:
                self.add_class(self.WIDTH_BREAKPOINS[w])
                break

    def on_mount(self):
        self.use_command_palette = False
        # Init.usuario_atual = Init.administrador
        # self.push_screen("tela_atendimento")
        self.push_screen("tela_login")

    def action_enviar_email(self):
        tela_login = self.get_screen("tela_login")
        tela_login.enviar_email()

    def action_cadastro(self):
        tela_login = self.get_screen("tela_login")
        tela_login.montar_cadastro()

    def action_voltar(self):
        tela_login = self.get_screen("tela_login")
        tela_login.voltar()
