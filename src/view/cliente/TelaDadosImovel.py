from textual.widgets import Static, Button, Footer, Checkbox, Tab, Tabs
from textual.screen import Screen
from textual.containers import VerticalScroll, HorizontalGroup
from utils.Widgets import Header, ResponsiveGrid
from utils.textual_image.widget import Image
from model import Init, Usuario, Atendimento
from controller import Controller


class TelaDadosImovel(Screen):

    def __init__(self, name=None, id=None, classes=None, imovel=None):
        super().__init__(name, id, classes)
        self.imovel = imovel

    TITLE = "Dados do Imóvel"

    CSS_PATH = "css/TelaDadosImovel.tcss"

    def compose(self):
        yield Header()
        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.CLIENTE:
            yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Dados", id="tab_dados_cliente"))

        with HorizontalGroup(id="titulo"):
            yield Static(self.imovel.get_anuncio().get_titulo(), classes="titulo")
            yield Static(f"R$ {self.imovel.get_valor():,.2f}", classes="valor")
        yield Static(f"{self.imovel.get_endereco().get_bairro()}, {self.imovel.get_endereco().get_cidade()} - {self.imovel.get_endereco().get_estado()}")

        with HorizontalGroup():
            with VerticalScroll(id="dados_imovel"):
                if self.imovel.get_anuncio() and self.imovel.get_anuncio().get_imagens():
                    yield Image(self.imovel.get_anuncio().get_imagens()[0], id="imagem_imovel")
                    with HorizontalGroup(id="galeria_fotos"):
                        for imagem in self.imovel.get_anuncio().get_imagens():
                            yield Image(imagem, classes="foto_pequena")
                yield Static("Descrição", id="stt_descricao", classes="titulo")
                yield Static(self.imovel.get_anuncio().get_descricao(), id="descricao")
                yield Static("Infraestrutura Apartamento", id="stt_infraestrutura", classes="titulo")
                with ResponsiveGrid(id="container_info_imovel"):
                    lista = self.imovel.get_filtros()
                    if lista:
                        for nome in lista:
                            yield Checkbox(label=nome, value=True, disabled=True)
                yield Static("Infraestrutura Condominio", id="stt_infraestrutura", classes="titulo")

                with ResponsiveGrid(id="container_info_condominio"):
                    lista = []
                    if self.imovel.get_condominio():
                        lista = self.imovel.get_condominio().get_filtros()
                    if lista:
                        for nome in lista:
                            yield Checkbox(label=nome, value=True, disabled=True)

                # yield Static("Mapa", id="mapa", classes="titulo")
            with VerticalScroll(id="entrar_contato"):
                with HorizontalGroup():
                    yield Button("Agendar Visita")
                    yield Button("Whatsapp", id="whatsapp")
                if self.imovel.get_valor_venda():
                    yield Static("Valor Venda:")
                    yield Static(f"R$ {self.imovel.get_valor_venda():.2f}", classes="valor")
                if self.imovel.get_valor_aluguel():
                    yield Static("Valor Aluguel:")
                    yield Static(f"R$ {self.imovel.get_valor_aluguel():.2f}", classes="valor")
                with HorizontalGroup():
                    yield Static("Condominio:")
                    yield Static(f"R$ {self.imovel.get_valor_condominio():.2f}", classes="valor")
                with HorizontalGroup():
                    yield Static("IPTU:")
                    yield Static(f"R$ {self.imovel.get_valor_iptu():.2f}", classes="valor")
                yield Button("Entrar em contato", id="bt_contato")
                yield Static("Um especialista irá entrar em contato por email ou whatsapp")

        yield Footer(show_command_palette=False)

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_contato":
            atendimento = Atendimento.Atendimento()
            atendimento.set_cliente(Init.usuario_atual)
            atendimento.set_imovel(self.imovel)
            atendimento.set_status(Atendimento.Status.PENDENTE)
            mensagem = Controller.cadastrar_atendimento(atendimento)
            self.norify(mensagem)

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

            elif event.tabs.active == self.query_one("#tab_atendimento", Tab).id:
                self.app.switch_screen("tela_atendimento")

            elif event.tabs.active == self.query_one("#tab_cadastro_venda_aluguel", Tab).id:
                self.app.switch_screen("tela_cadastro_venda_aluguel")

        except:
            pass
