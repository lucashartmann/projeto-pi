from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Footer, Header, Tab, Tabs
from textual.containers import Horizontal

from model import Corretor, Administrador, Init, Gerente


class ContainerCliente(Horizontal):
    def compose(self):
        Static("Nome do cliente", id="st_nome")
        Static("Telefone do cliente", id="st_telefone")
        Static("Email do cliente", id="st_email")
        Static("Interessado em:", id="st_interesse")
        Static("Apartamento, 2 quartos, 3 banheiros", id="st_imovel_interesse")


class TelaAtendimento(Screen):
    compradores = Init.imobiliaria.get_lista_compradores()

    def compose(self):
        yield Header()
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif isinstance(Init.usuario_atual, Corretor.Corretor):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        elif isinstance(Init.usuario_atual, Gerente.Gerente):
            yield Tabs(Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"),
                       Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Estoque", id="tab_estoque"))
        else:
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))

        with Horizontal():
            with Vertical():
                yield Static("Recém Cadastrados")
                yield Vertical(id="container_cadastrados")
            with Vertical():
                yield Static("Esperando Atendimento")
                yield Vertical(id="container_esperando")
            with Vertical():
                yield Static("Atendimento em andamento")
                yield Vertical(id="container_andamento")

        yield Footer()

    def on_mount(self):
        if self.compradores:
            for cliente in self.compradores[-1:-6]:
                container = ContainerCliente()

                self.query_one("#container_cadastrados").mount(container)
                container.query_one("#st_nome").content = cliente.get_nome()
                container.query_one(
                    "#st_telefone").content = cliente.get_telefone()
                container.query_one("#st_email").content = cliente.get_email()
                # container.query_one("#st_interesse").content =
                # container.query_one("#st_imovel_interesse").content =
