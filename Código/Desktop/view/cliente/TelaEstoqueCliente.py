from textual.widgets import Static, Button, ListItem, ListView, Footer, Header, Select, Input, Tab, Tabs
from textual import on
from textual.screen import Screen
from textual.containers import VerticalScroll, HorizontalGroup, Container

from textual_image.widget import Image as TextualImage

from model import Init, Administrador, Corretor
from controller import Controller

from io import BytesIO


class Containerimovel(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_imovel = ""

    def compose(self):
        yield TextualImage("")
        yield Static("Dualshock", id="tx_nome")
        yield Static("R$ 299,99", id="tx_preco")
        yield Select([("1", 1)])
        yield Button("Adicionar ao carrinho", id="bt_comprar")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_comprar":
            mensagem = Controller.adicionar_no_carrinho(
                self.id_imovel, self.query_one(Select).value)
            self.screen.notify(mensagem)
            if "ERRO" not in mensagem:
                if self.app.get_screen("tela_carrinho_compras"):
                    try:
                        self.app.get_screen(
                            "tela_carrinho_compras").atualizar()
                    except Exception as e:
                        pass


class TelaEstoqueCliente(Screen):

    CSS_PATH = "css/TelaEstoqueCliente.tcss"

    imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis_disponiveis()
    imoveis_filtrados = []

    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    montou = False

    def atualizar_imagens(self):
        self.imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis_disponiveis()
        list_view = self.query_one("#lst_item", ListView)
        list_view.clear()
        lista = self.imoveis
        if len(self.imoveis_filtrados) > 0:
            lista = self.imoveis_filtrados

        for imovel in lista:
            if imovel.get_imagem():
                container = Containerimovel()
                list_item = ListItem(name=imovel.get_nome())
                list_view.append(list_item)
                list_item.mount(container)
                container.query_one(TextualImage).image = BytesIO(
                    imovel.get_imagem())

                container.query_one(TextualImage).styles.height = 13
                container.query_one(TextualImage).styles.width = 30

                container.query_one("#tx_nome").content = imovel.get_nome(
                )

                container.query_one(
                    "#tx_preco").content = f"R$ {imovel.get_preco():.2f}"

                lista = []
                for i in range(imovel.get_quantidade()):
                    lista.append((str(i+1), i+1))

                container.query_one(Select).set_options(lista)

                container.id_imovel = imovel.get_id()

                list_item.styles.width = 30
                list_item.styles.height = 30

    def compose(self):
        yield Header()
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"), Tab("Dados Cliente", id="tab_dados_usuario"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))
        else:
            yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Dados", id="tab_dados_cliente"))
        with VerticalScroll():
            with HorizontalGroup(id="hg_pesquisa"):
                yield Select([("genero", 'genero')], id="select_categoria")
                yield Input()
                yield Button("Remover", id="bt_remover")
            yield ListView(id="lst_item")
            yield Footer()

    def on_mount(self):
        self.query_one(Tabs).active = self.query_one("#tab_comprar", Tab).id
        # self.imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis_disponiveis()

        self.atualizar_imagens()

        lista_categorias = []
        for imovel in self.imoveis:
            if imovel.get_categoria() not in lista_categorias:
                lista_categorias.append(imovel.get_categoria())
        self.query_one(Select).set_options(
            [(categoria, categoria) for categoria in lista_categorias])
        self.atualizar_imagens()

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
