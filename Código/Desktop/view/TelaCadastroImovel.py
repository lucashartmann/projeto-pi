from textual.screen import Screen
from textual.widgets import MaskedInput, Static, TextArea, Tab, Tabs, Select, Checkbox, Button, Header, Footer
from textual.containers import Horizontal, Vertical, Grid, Container, VerticalScroll, Center
import requests

from model import Init, Imovel, Administrador, Corretor, Gerente


class PopUp(Container):
    def compose(self):
        yield ("Imovel nao salvo, deseja continuar?")


class PopUp(Container):
    def compose(self):
        yield ("Certeza que deseja apagar?")


class TelaCadastroImovel(Screen):

    CSS_PATH = "css/TelaCadastroImovel.tcss"

    def on_text_area_changed(self, evento: TextArea.Changed):
        if evento.text_area.id == "ta_cep":
            cep = str(evento.text_area.text.strip())
            print(cep)
            print(len(cep))

            self.query_one("#ta_bairro", TextArea).clear()
            self.query_one("#ta_estado", MaskedInput).clear()
            self.query_one("#ta_rua", TextArea).clear()
            self.query_one("#ta_cidade", TextArea).clear()

            if len(cep) > 7:
                try:
                    link = f"https://viacep.com.br/ws/{cep}/json/"

                    requisicao = requests.get(link)
                    dados = requisicao.json()

                    logradouro = dados["logradouro"]
                    bairro = dados["bairro"]
                    cidade = dados["localidade"]
                    uf = dados["uf"]

                    print(logradouro)
                    print(type(logradouro))

                    self.query_one("#ta_bairro", TextArea).text = bairro
                    self.query_one("#ta_estado", MaskedInput).value = uf
                    self.query_one("#ta_rua", TextArea).text = logradouro
                    self.query_one("#ta_cidade", TextArea).text = cidade
                except Exception as e:
                    pass

    def compose(self):
        yield Header()
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"), Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))
        elif isinstance(Init.usuario_atual, Corretor.Corretor):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))
        else:
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))

        with Horizontal(id="h_buttons"):
            yield Button("Apagar")
            yield Button("Salvar")

        with VerticalScroll():
            yield Tabs(Tab("Cadastro", id="tab_imovel"), Tab("Anuncio", id="tab_anuncio"), id="tabs_anuncio")

            with Grid(id="container_cadastro"):
                yield Static("ref:", id="stt_ref")
                yield TextArea(read_only=True, id="ta_ref")
                yield Static("Categoria:", id="stt_categoria")
                yield Select([(valor.value, valor) for valor in Imovel.Categoria], id="select_categoria")
                yield Static("Situação:", id="stt_situacao")
                yield Select([(valor.value, valor) for valor in Imovel.Situacao], id="select_situacao")
                yield Static("Estado:", id="stt_estado_select")
                yield Select([(valor.value, valor) for valor in Imovel.Estado], id="select_estado")
                yield Static("Ocupação:", id="stt_ocupacao")
                yield Select([(valor.value, valor) for valor in Imovel.Ocupacao], id="select_ocupacao")
                yield Static("Status:", id="stt_status")
                yield Select([(valor.value, valor) for valor in Imovel.Status], id="select_status")
                yield Static("Nome do Condomínio", id="stt_nome_condominio")
                yield TextArea(id="ta_nome_condominio")
                yield Static("Rua", id="stt_rua")
                yield TextArea(disabled=True, id="ta_rua")
                yield Static("Número", id="stt_numero")
                yield TextArea(id="ta_numero")
                yield Static("Complemento", id="stt_complemento")
                yield TextArea(id="ta_complemento")
                yield Static("Bloco", id="stt_bloco")
                yield MaskedInput(template="000", id="ta_bloco")
                yield Static("CEP", id="stt_cep")
                yield TextArea(id="ta_cep")
                yield Static("Bairro", id="stt_bairro")
                yield TextArea(disabled=True, id="ta_bairro")
                yield Static("Cidade", id="stt_cidade")
                yield TextArea(disabled=True, id="ta_cidade")
                yield Static("Estado", id="stt_estado")
                yield MaskedInput(template="00", disabled=True, id="ta_estado")
                yield Static("Salas", id="stt_salas")
                yield MaskedInput(template="00", id="ta_salas")
                yield Static("Banheiros", id="stt_banheiros")
                yield MaskedInput(template="00", id="ta_banheiros")
                yield Static("Vagas", id="stt_vagas")
                yield MaskedInput(template="00", id="ta_vagas")
                yield Static("Varandas", id="stt_varandas")
                yield MaskedInput(template="00", id="ta_varandas")
                yield Static("Quartos", id="stt_quartos")
                yield MaskedInput(template="00", id="ta_quartos")
                yield Static("Área Total", id="stt_area_total")
                yield MaskedInput(template="000.000m²", id="ta_area_total")
                yield Static("Área Privativa", id="stt_area_privativa")
                yield MaskedInput(template="000.000m²", id="ta_area_privativa")
                yield Static("Valor Venda:", id="stt_venda")
                yield MaskedInput(template="R$000.000.000", id="ta_venda")
                yield Static("Valor Aluguel:", id="stt_aluguel")
                yield MaskedInput(template="R$000.000.000", id="ta_aluguel")
                yield Static("Valor Condomínio:", id="stt_condominio")
                yield MaskedInput(template="R$000.000.000", id="ta_condominio")
                yield Static("Valor IPTU:", id="stt_iptu")
                yield MaskedInput(template="R$000.000.000", id="ta_iptu")

            with Vertical(id="container_anuncio"):
                yield Static("Titulo")
                with Center():
                    yield TextArea(id="ta_titulo_anuncio")
                yield Static("Descriçao")
                with Center():
                    yield TextArea(id="ta_descricao_anuncio")
                yield Static("Apartamento")

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

                yield Static("Condomínio")
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

            with Grid(id="container_imagens"):
                yield Button("Editar")
                # for i in ....
                #     yield Image()

            with Vertical(id="container_proprietario"):
                yield Static("Proprietario: ", classes="stt_container_titulo")
            with Vertical(id="container_corretor"):
                yield Static("Corretor: ", classes="stt_container_titulo")
            with Vertical(id="container_captador"):
                yield Static("Captador: ", classes="stt_container_titulo")
        yield Footer(show_command_palette=False)

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_cadastro_imovel", Tab).id

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.id == "tabs_anuncio":
            if event.tabs.active == self.query_one("#tab_anuncio", Tab).id:
                self.query_one("#container_cadastro").display = "none"
                self.query_one("#container_anuncio").display = "block"
            else:
                self.query_one("#container_anuncio").display = "none"
                self.query_one("#container_cadastro").display = "block"
        else:
            try:
                if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
                    self.app.switch_screen("tela_estoque")
                elif event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                    self.app.switch_screen("tela_cadastro_pessoa")
                elif isinstance(Init.usuario_atual, Gerente.Gerente):
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
