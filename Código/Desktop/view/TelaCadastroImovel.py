from textual.screen import Screen
from textual.widgets import MaskedInput, Static, TextArea, Tab, Tabs, Select, Checkbox, Button, Header, Footer
from textual.containers import Horizontal, Vertical, Grid, Container, VerticalScroll

from textual_image.widget import Image

from model import Init, Imovel, Administrador, Corretor


class PopUp(Container):
    def compose(self):
        yield ("Imovel nao salvo, deseja continuar?")


class PopUp(Container):
    def compose(self):
        yield ("Certeza que deseja apagar?")


class TelaCadastroImovel(Screen):

    CSS_PATH = "css/TelaCadastroImovel.tcss"

    def compose(self):
        yield Header()
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"), Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))

        elif isinstance(Init.usuario_atual, Corretor.Corretor):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))
        else:
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))

        with VerticalScroll():
            yield Tabs(Tab("Cadastro"), Tab("Anuncio"), Tab("Imagens"))
            with Horizontal(id="h_buttons"):
                yield Button("Apagar")
                yield Button("Salvar")
            with Grid(id="container_cadastro"):
                yield Tabs(Tab("Imovel"), Tab("Info+"))
                yield Static("ref:")
                yield TextArea(read_only=True)
                yield Static("Categoria:")
                yield Select([(valor, valor) for valor in Imovel.Categoria._member_names_])
                yield Static("Situação:")
                yield Select([(valor, valor) for valor in Imovel.Situacao._member_names_])
                yield Static("Estado:")
                yield Select([(valor, valor) for valor in Imovel.Estado._member_names_])
                yield Static("Ocupacao:")
                yield Select([(valor, valor) for valor in Imovel.Ocupacao._member_names_])
                yield Static("Status:")
                yield Select([(valor, valor) for valor in Imovel.Status._member_names_])
                yield Static("Nome do Condominio")
                yield TextArea()
                yield Static("Rua")
                yield TextArea()
                yield Static("Bairro")
                yield TextArea()
                yield Static("Cidade")
                yield TextArea()
                yield Static("Estado(sigla)")
                yield MaskedInput(template="00")
                yield Static("Complemento")
                yield TextArea()
                yield Static("CEP")
                yield TextArea()
                yield Static("Salas")
                yield MaskedInput(template="00")
                yield Static("Banheiros")
                yield MaskedInput(template="00")
                yield Static("Vagas")
                yield MaskedInput(template="00")
                yield Static("Varandas")
                yield MaskedInput(template="00")
                yield Static("Quartos")
                yield MaskedInput(template="00")
                yield Static("Area Total")
                yield MaskedInput(template="000.000m²")
                yield Static("Area Privativa")
                yield MaskedInput(template="000.000m²")
                yield Static("Bloco")
                yield MaskedInput(template="000")
                yield Static("Cor:")
                yield TextArea()
                yield Static("Valor Venda:")
                yield MaskedInput(template="R$000.000.000")
                yield Static("Valor Aluguel:")
                yield MaskedInput(template="R$000.000.000")
                yield Static("Valor Condominio:")
                yield MaskedInput(template="R$000.000.000")
                yield Static("Valor IPTU:")
                yield MaskedInput(template="R$000.000.000")

            with Vertical(id="container_info"):
                with Grid(id="container_info_imovel"):
                    yield Checkbox("Aceita Pet")
                    yield Checkbox("Churrasqueira")
                    yield Checkbox("Armarios Embutidos")
                    yield Checkbox("Cozinha Americana")
                    yield Checkbox("Area de Servico")
                    yield Checkbox("Suite Master")
                    yield Checkbox("Banheiro com janela")
                    yield Checkbox("Piscina")
                    yield Checkbox("Lareira")
                    yield Checkbox("Ar-condicionado")
                    yield Checkbox("Semi-Mobiliado")
                    yield Checkbox("Mobiliado")
                    yield Checkbox("Dependencia de Empregada")
                    yield Checkbox("Dispensa")
                    yield Checkbox("Deposito")

                with Grid(id="container_info_condominio"):
                    yield Checkbox("Churrasqueira Coletiva")
                    yield Checkbox("Piscina")
                    yield Checkbox("Piscina Infantil")
                    yield Checkbox("Piscina Aquecida")
                    yield Checkbox("Quiosque")
                    yield Checkbox("Sauna")
                    yield Checkbox("Quadra de Esportes")
                    yield Checkbox("Jardim")
                    yield Checkbox("Salão de Festas")
                    yield Checkbox("Academia")
                    yield Checkbox("Sala de Jogos")
                    yield Checkbox("Playground")
                    yield Checkbox("Brinquedoteca")
                    yield Checkbox("Vaga Coberta")
                    yield Checkbox("Estacionamento")
                    yield Checkbox("Vaga para Visitantes")
                    yield Checkbox("Mercado")
                    yield Checkbox("Mesa de Sinuca")
                    yield Checkbox("Mesa de Ping-Pong")
                    yield Checkbox("Mesa de Pebolim")
                    yield Checkbox("Quadra de Tenis")
                    yield Checkbox("Quadra de Futebol")
                    yield Checkbox("Quadra de Basquete")
                    yield Checkbox("Quadra de Volei")
                    yield Checkbox("Quadra de Areia")
                    yield Checkbox("Bicicletario")
                    yield Checkbox("Heliponto")
                    yield Checkbox("Elevador de Serviço")

            with Vertical(id="container_anuncio"):
                yield Static("Titulo")
                yield TextArea()
                yield Static("Descriçao")
                yield TextArea()

            with Grid(id="container_imagens"):
                yield Button("Editar")
                # for i in ....
                #     yield Image()

            yield Static("Proprietario: ")
            yield Static("Corretor: ")
            yield Static("Captador: ")
        yield Footer(show_command_palette=False)
    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_cadastro_imovel", Tab).id

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:
            if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
                self.app.switch_screen("tela_estoque")
            elif event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                self.app.switch_screen("tela_cadastro_imovel")
            elif event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                self.app.switch_screen("tela_cadastro_pessoa")
            elif isinstance(Init.usuario_atual, Corretor.Corretor):
                if event.tabs.active == self.query_one("#tab_dados_imobiliaria", Tab).id:
                    self.app.switch_screen("tela_dados_imobiliaria")
            elif isinstance(Init.usuario_atual, Administrador.Administrador):
                if event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                    self.app.switch_screen("tela_servidor")
            elif event.tabs.active == self.query_one("#tab_comprar", Tab).id:
                self.app.switch_screen("tela_estoque_cliente")
            elif event.tabs.active == self.query_one("#tab_dados_cliente", Tab).id:
                self.app.switch_screen("tela_dados_cliente")
        except:
            pass
