from textual.widgets import Static, Button, Footer, Checkbox, Tab, Tabs
from textual.screen import Screen
from textual.containers import HorizontalGroup, Grid, Vertical, Center
from utils.Widgets import Header
from textual_image.widget import Image
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
            if self.imovel.get_anuncio() and self.imovel.get_anuncio().get_titulo() is not None:
                yield Static(self.imovel.get_anuncio().get_titulo(), classes="titulo")
            if self.imovel.get_valor_venda() is not None:
                yield Static(f"R$ {self.imovel.get_valor_venda():,.2f}", classes="valor")
            if self.imovel.get_valor_aluguel() is not None:
                yield Static(f"R$ {self.imovel.get_valor_aluguel():,.2f}", classes="valor")
        if self.imovel.get_endereco() and self.imovel.get_endereco().get_bairro() is not None and self.imovel.get_endereco().get_cidade() is not None and self.imovel.get_endereco().get_uf() is not None:
            yield Static(f"{self.imovel.get_endereco().get_bairro()}, {self.imovel.get_endereco().get_cidade()} - {self.imovel.get_endereco().get_uf()}")

        with HorizontalGroup():
            with Vertical(id="dados_imovel"):
                if self.imovel.get_anuncio() and self.imovel.get_anuncio().get_imagens():
                    with Center():
                        yield Image(self.imovel.get_anuncio().get_imagens()[0], id="imagem_imovel")
                    with HorizontalGroup(id="galeria_fotos"):
                        for imagem in self.imovel.get_anuncio().get_imagens():
                            yield Image(imagem, classes="foto_pequena")
                
                if self.imovel.get_anuncio() and self.imovel.get_anuncio().get_descricao() is not None:
                    yield Static("Descrição", id="stt_descricao", classes="titulo")
                    yield Static(self.imovel.get_anuncio().get_descricao(), id="descricao")
                lista = self.imovel.get_filtros()
                if lista:
                    yield Static("Infraestrutura Apartamento", id="stt_infraestrutura", classes="titulo")
                    with Grid(id="container_info_imovel"):
                            for nome in lista:
                                yield Checkbox(label=nome, value=True, disabled=True)
                lista = []
                if self.imovel.get_condominio() is not None:
                        lista = self.imovel.get_condominio().get_filtros()
                if lista:
                    yield Static("Infraestrutura Condominio", classes="titulo")
                    with Grid(id="container_info_condominio"):
                            for nome in lista:
                                yield Checkbox(label=nome, value=True, disabled=True)
                # yield Static("Mapa", id="mapa", classes="titulo")
            with Vertical(id="entrar_contato"):
                with HorizontalGroup():
                    yield Button("Agendar Visita")
                    yield Button("Whatsapp", id="whatsapp")
                if self.imovel.get_valor_venda() is not None:
                    yield Static("Valor Venda:")
                    yield Static(f"R$ {self.imovel.get_valor_venda():.2f}", classes="valor")
                if self.imovel.get_valor_aluguel() is not None:
                    yield Static("Valor Aluguel:")
                    yield Static(f"R$ {self.imovel.get_valor_aluguel():.2f}", classes="valor")
                with HorizontalGroup():
                    yield Static("Condominio:")
                    if self.imovel.get_valor_condominio() is not None:
                        yield Static(f"R$ {self.imovel.get_valor_condominio():.2f}", classes="valor")
                with HorizontalGroup():
                    yield Static("IPTU:")
                    if self.imovel.get_iptu() is not None:
                        yield Static(f"R$ {self.imovel.get_iptu():.2f}", classes="valor")
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

   
