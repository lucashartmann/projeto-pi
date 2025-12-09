from textual.widgets import Static, Button, ListItem, ListView, Footer, Header, Select, Input, Tab, Tabs, SelectionList, MaskedInput
from textual import on
from textual.screen import Screen
from textual.containers import VerticalScroll, Container, Grid

from textual_image.widget import Image

from model import Init, Usuario, Imovel
from database.Banco import Banco
from io import BytesIO
from view.cliente import TelaDadosImovel


class ContainerImovel(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_imovel = ""

    def compose(self):
        yield Image(r"", id="ti_imagem")
        yield Static("Sala Comercial a venda no Centro de Porto Alegre", id="tx_nome")
        yield Static("R$ 255.000,00", id="tx_preco")
        yield Button("Ver mais", id="bt_comprar")

    def on_button_pressed(self, evento: Button.Pressed):
        banco = Banco()
        imovel = banco.get_imovel_por_id(self.id_imovel)
        if imovel:
            self.app.switch_screen(
                TelaDadosImovel.TelaDadosImovel(imovel=imovel))
        else:
            self.screen.notify("ERRO. Imóvel não encontrado.")


class TelaEstoqueCliente(Screen):
    TITLE = "Imovéis"

    CSS_PATH = "css/TelaEstoqueCliente.tcss"

    imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis_disponiveis()
    imoveis_filtrados = []

    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    montou = False

    def compose(self):
        yield Header()
        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.CLIENTE:
            yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Dados", id="tab_dados_cliente"))
            
        with VerticalScroll():
            with Grid(id="hg_pesquisa"):
                    yield Select([("Venda", "Venda"), ("Aluguel", "Aluguel")])
                    yield Select([(valor.value, valor) for valor in Imovel.Categoria])
                    yield Static("CEP desejado")
                    yield MaskedInput(template="00000-000")
                    yield Static("Apartamento:")
                    yield SelectionList(("Aceita Pet", "aceita_pet"), ("Churrasqueira", "churrasqueira"), ("Armarios Embutidos", "armarios_embutidos"), ("Cozinha Americana", "cozinha_americana"), ("Area de Servico", "area_de_servico"), ("Suite Master", "suite_master"), ("Banheiro com janela", "banheiro_com_janela"), ("Piscina", "piscina"), ("Lareira", "lareira"), ("Ar-condicionado", "ar_condicionado"), ("Semi-Mobiliado", "semi_mobiliado"), ("Mobiliado", "mobiliado"), ("Dependencia de Empregada", "dependencia_de_empregada"), ("Dispensa", "dispensa"), ("Deposito", "deposito"), id="filtro_apartamento", compact=True)
                    yield Static("Condominio:")
                    yield SelectionList(("Churrasqueira Coletiva", "churrasqueira_coletiva"), ("Piscina", "piscina"), ("Piscina Infantil", "piscina_infantil"), ("Piscina Aquecida", "piscina_aquecida"), ("Quiosque", "quiosque"), ("Sauna", "sauna"), ("Quadra de Esportes", "quadra_de_esportes"), ("Jardim", "jardim"), ("Salão de Festas", "salao_de_festas"), ("Academia", "academia"), ("Sala de Jogos", "sala_de_jogos"), ("Playground", "playground"), ("Brinquedoteca", "brinquedoteca"), ("Vaga Coberta", "vaga_coberta"), ("Estacionamento", "estacionamento"), ("Vaga para Visitantes", "vaga_para_visitantes"), ("Mercado", "mercado"), ("Mesa de Sinuca", "mesa_de_sinuca"), ("Mesa de Ping-Pong", "mesa_de_ping_pong"), ("Mesa de Pebolim", "mesa_de_pebolim"), ("Quadra de Tenis", "quadra_de_tenis"), ("Quadra de Futebol", "quadra_de_futebol"), ("Quadra de Basquete", "quadra_de_basquete"), ("Quadra de Volei", "quadra_de_volei"), ("Quadra de Areia", "quadra_de_areia"), ("Bicicletario", "bicicletario"), ("Heliponto", "heliponto"), ("Elevador de Serviço", "elevador_de_servico"), id="filtro_condominio", compact=True)
            yield ListView(id="lst_item")
            yield Footer(show_command_palette=False)

    def atualizar_imagens(self):

        list_view = self.query_one("#lst_item", ListView)
        list_view.clear()

        if self.imoveis_filtrados:
            lista = self.imoveis_filtrados
        else:
            lista = self.imoveis
            
        if not lista:
            stt = Static("Nenhum imóvel encontrado", id="tx_status")
            self.query_one("#lst_item").mount(stt)
            stt.styles.align = ("center", "middle")
            self.query_one("#lst_item").styles.content_align = ("center", "middle")
        # else:
        #     self.query_one("#lst_item").styles.content_align = None

        for imovel in lista:
            if imovel.get_anuncio() and imovel.get_anuncio().get_imagens():
                container = ContainerImovel()
                list_item = ListItem(name=imovel.get_nome())
                list_view.append(list_item)
                list_item.mount(container)

                container.query_one("#ti_imagem").image = BytesIO(
                    imovel.get_anuncio().get_imagens()[0])

                container.query_one("#ti_imagem").styles.width = 40
                container.query_one("#ti_imagem").styles.height = 15

                if imovel.get_titulo(
                ):
                    container.query_one("#tx_nome").content = imovel.get_titulo(
                    )
                else:
                    container.query_one("#tx_nome").styles.display = "none"

                if imovel.get_valor_venda():
                    container.query_one(
                        "#tx_preco").content = f"R$ {imovel.get_valor_venda():.2f}"
                else:
                    container.query_one(
                        "#tx_preco").styles.display = "none"

                if imovel.get_valor_aluguel():
                    container.query_one(
                        "#tx_preco").content = f"R$ {imovel.get_valor_aluguel():.2f}"
                else:
                    container.query_one(
                        "#tx_preco").styles.display = "none"

                container.id_imovel = imovel.get_id()

                list_item.styles.width = 30
                list_item.styles.height = 30

    def on_screen_resume(self):

        self.query_one(Tabs).active = self.query_one("#tab_comprar", Tab).id

        imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis_disponiveis()

        if imoveis != self.imoveis:
            self.imoveis = imoveis
            self.atualizar_imagens()

    def on_mount(self):
        self.atualizar_imagens()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
            
            if event.tabs.active == self.query_one("#tab_dados_cliente", Tab).id:
                self.app.switch_screen("tela_dados_cliente")


    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_remover":
                input_id = self.query_one(Input).value
                self.atualizar_imagens()

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        if evento.select.id == "#select_categoria":
            if evento.select.is_blank():
                if self.filtrou_input == False and self.filtrou_select:
                    self.imoveis_filtrados = []
                self.filtrou_select = False
                self.atualizar_imagens()
            else:
                valor_select = str(evento.value)
                valor_antigo = ""
                if valor_select != valor_antigo and self.filtrou_input == False and self.filtrou_select:
                    self.imoveis_filtrados = []
                    valor_antigo = valor_select
                if len(self.imoveis_filtrados) == 0:
                    for imovel in self.imoveis:
                        if imovel.get_categoria() == valor_select:
                            self.imoveis_filtrados.append(imovel)
                else:
                    imoveis_temp = []
                    for imovel in self.imoveis_filtrados:
                        if imovel.get_categoria() == valor_select:
                            imoveis_temp.append(imovel)
                    if len(imoveis_temp) > 0:
                        self.imoveis_filtrados = imoveis_temp

                self.filtrou_select = True
                self.select_evento = evento
                self.atualizar_imagens()

    def filtro(self, palavras, index, filtro_recebido):
        lista_filtros = ["quant", "codigo"]
        campo = f"get_{filtro_recebido}"
        nova_lista = []

        if index + 1 < len(palavras):
            filtro = " ".join((palavras[index+1:]))

            if "," in filtro:
                filtro = filtro[0:filtro.index(
                    ",")]
            if "-" in filtro.split():
                for palavraa in filtro.split("-"):
                    if filtro.index("-")+1 < len(filtro) and palavraa not in nova_lista:
                        nova_lista.append(palavraa.strip())

            if filtro_recebido in lista_filtros:
                try:
                    filtro = int(filtro)
                except ValueError:
                    self.notify("Valor Inválido")
                    return

            if len(self.imoveis_filtrados) > 0:
                imoveis_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for imovel in self.imoveis_filtrados:
                            if type(filtro) == int:
                                if p == getattr(imovel, campo)() and imovel not in imoveis_temp:
                                    imoveis_temp.append(
                                        imovel)
                            else:
                                if p in getattr(imovel, campo)() and imovel not in imoveis_temp:
                                    imoveis_temp.append(
                                        imovel)
                else:
                    for imovel in self.imoveis_filtrados:
                        if type(filtro) == int:
                            if filtro == getattr(imovel, campo)() and imovel not in imoveis_temp:
                                imoveis_temp.append(imovel)
                        else:
                            if filtro in getattr(imovel, campo)() and imovel not in imoveis_temp:
                                imoveis_temp.append(imovel)
                if len(imoveis_temp) > 0:
                    self.imoveis_filtrados = imoveis_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for imovel in self.imoveis:
                            if type(filtro) == int:
                                if p == getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                    self.imoveis_filtrados.append(
                                        imovel)
                            else:
                                if p in getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                    self.imoveis_filtrados.append(
                                        imovel)
                else:
                    for imovel in self.imoveis:
                        if type(filtro) == int:
                            if filtro == getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                self.imoveis_filtrados.append(imovel)
                        else:
                            if filtro in getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                self.imoveis_filtrados.append(imovel)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value
        palavras = texto.split()

        if len(palavras) > 0:
            self.imoveis_filtrados = []
            for palavra in palavras:
                if palavra[:-1].lower() in Init.um_imovel.__dict__.keys():
                    index = palavras.index(palavra)
                    self.filtro(palavras, index, palavra[:-1].lower())
                    self.atualizar_imagens()
        else:
            self.atualizar_imagens()
