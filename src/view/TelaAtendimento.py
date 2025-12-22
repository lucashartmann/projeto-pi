from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Footer, Tab, Tabs
from textual.containers import Horizontal
from utils.Widgets import Header
from model import Usuario, Init, Atendimento


class ContainerCliente(Horizontal):
    def compose(self):
        Static("Nome do cliente", id="st_nome")
        Static("Telefone do cliente", id="st_telefone")
        Static("Email do cliente", id="st_email")
        Static("Interessado em:", id="st_interesse")
        Static("Apartamento, 2 quartos, 3 banheiros", id="st_imovel_interesse")


class TelaAtendimento(Screen):
    compradores = []
    atendimentos = Init.imobiliaria.get_lista_atendimentos()
    recem_cadastrados = []
    em_atendimento = []
    pendentes = []
    usuarios = Init.imobiliaria.get_lista_usuarios()
    CSS_PATH = "css/TelaAtendimento.tcss"

    def compose(self):
        yield Header()
        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.CORRETOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
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

        yield Footer(show_command_palette=False)

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_atendimento", Tab).id
        compradores = list(
            usuario for usuario in self.usuarios if self.usuarios and usuario and usuario.get_tipo() == Usuario.Tipo.CLIENTE)
        atendimentos = Init.imobiliaria.get_lista_atendimentos()
        atendimentos_em_andamento = []
        atendimentos_pendentes = []

        if atendimentos != self.atendimentos:
            self.atendimentos = atendimentos
            for atendimento in self.atendimentos:
                if atendimento.get_status() == Atendimento.Status.EM_ANDAMENTO:
                    atendimentos_em_andamento.append(atendimento)

            for atendimento in self.atendimentos:
                if atendimento.get_status() == Atendimento.Status.PENDENTE:
                    atendimentos_pendentes.append(atendimento)

        if atendimentos_em_andamento != self.em_atendimento:
            self.em_atendimento = atendimentos_em_andamento
            self.ataulizar_andamentos()

        if atendimentos_pendentes != self.pendentes:
            self.pendentes = atendimentos_pendentes
            self.atualizar_pendentes()

        if compradores[-1:-6] != self.recem_cadastrados:
            self.recem_cadastrados = compradores[-1:-6]
            self.atualizar_recem_cadastrados()

    def ataulizar_andamentos(self):
        self.query_one("#container_andamento").remove_children
        for atendimento in self.atendimentos:
            if atendimento.get_status() == Atendimento.Status.EM_ANDAMENTO:
                container = ContainerCliente()
                self.query_one("#container_andamento").mount(container)
                container.query_one(
                    "#st_nome").content = atendimento.get_cliente().get_nome()
                container.query_one(
                    "#st_telefone").content = atendimento.get_cliente().get_telefone()
                container.query_one(
                    "#st_email").content = atendimento.get_cliente().get_email()

    def atualizar_pendentes(self):
        self.query_one("#container_esperando").remove_children

        for atendimento in self.atendimentos:
            if atendimento.get_status() == Atendimento.Status.PENDENTE:
                container = ContainerCliente()
                self.query_one("#container_esperando").mount(container)
                container.query_one(
                    "#st_nome").content = atendimento.get_cliente().get_nome()
                container.query_one(
                    "#st_telefone").content = atendimento.get_cliente().get_telefone()
                container.query_one(
                    "#st_email").content = atendimento.get_cliente().get_email()

    def atualizar_recem_cadastrados(self):
        self.query_one("#container_cadastrados").remove_children()
        if self.compradores:
            for cliente in self.recem_cadastrados:
                container = ContainerCliente()

                self.query_one("#container_cadastrados").mount(container)
                container.query_one("#st_nome").content = cliente.get_nome()
                container.query_one(
                    "#st_telefone").content = cliente.get_telefone()
                container.query_one("#st_email").content = cliente.get_email()
                # container.query_one("#st_interesse").content =
                # container.query_one("#st_imovel_interesse").content =

    def on_mount(self):
        compradores = list(
            usuario for usuario in self.usuarios if self.usuarios and usuario and usuario.get_tipo() == Usuario.Tipo.CLIENTE)
        if compradores:
            self.recem_cadastrados = compradores[-1:-6]
        self.em_atendimento = []
        self.pendentes = []

        for atendimento in self.atendimentos:
            if atendimento.get_status() == Atendimento.Status.EM_ANDAMENTO:
                self.em_atendimento.append(atendimento)

        for atendimento in self.atendimentos:
            if atendimento.get_status() == Atendimento.Status.PENDENTE:
                self.pendentes.append(atendimento)

        self.ataulizar_andamentos()
        self.atualizar_pendentes()
        if self.recem_cadastrados:
            self.atualizar_recem_cadastrados()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:
            if event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                self.app.switch_screen("tela_cadastro_pessoa")

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

            elif event.tabs.active == self.query_one("#tab_cadastro_venda_aluguel", Tab).id:
                self.app.switch_screen("tela_cadastro_venda_aluguel")

        except:
            pass
