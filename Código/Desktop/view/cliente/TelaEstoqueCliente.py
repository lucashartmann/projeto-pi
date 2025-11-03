from textual.widgets import Static, Button, ListItem, ListView, Footer, Header, Select, Input, Tab, Tabs
from textual import on
from textual.screen import Screen
from textual.containers import VerticalScroll, HorizontalGroup, Container

from textual_image.widget import Image as TextualImage

from model import Init
from controller import Controller

from io import BytesIO


class ContainerProduto(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_produto = ""

    def compose(self):
        yield TextualImage("")
        yield Static("Dualshock", id="tx_nome")
        yield Static("R$ 299,99", id="tx_preco")
        yield Select([("1", 1)])
        yield Button("Adicionar ao carrinho", id="bt_comprar")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_comprar":
            mensagem = Controller.adicionar_no_carrinho(
                self.id_produto, self.query_one(Select).value)
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

    produtos = Init.loja.get_estoque().get_lista_produtos_disponiveis()
    produtos_filtrados = []

    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    montou = False

    def atualizar_imagens(self):
        self.produtos = Init.loja.get_estoque().get_lista_produtos_disponiveis()
        list_view = self.query_one("#lst_item", ListView)
        list_view.clear()
        lista = self.produtos
        if len(self.produtos_filtrados) > 0:
            lista = self.produtos_filtrados

        for produto in lista:
            if produto.get_imagem():
                container = ContainerProduto()
                list_item = ListItem(name=produto.get_nome())
                list_view.append(list_item)
                list_item.mount(container)
                container.query_one(TextualImage).image = BytesIO(
                    produto.get_imagem())

                container.query_one(TextualImage).styles.height = 13
                container.query_one(TextualImage).styles.width = 30

                container.query_one("#tx_nome").content = produto.get_nome(
                )

                container.query_one(
                    "#tx_preco").content = f"R$ {produto.get_preco():.2f}"

                lista = []
                for i in range(produto.get_quantidade()):
                    lista.append((str(i+1), i+1))

                container.query_one(Select).set_options(lista)

                container.id_produto = produto.get_id()

                list_item.styles.width = 30
                list_item.styles.height = 30

    def compose(self):
        yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Carrinho", id="tab_carrinho_compras"), Tab("Dados", id="tab_dados_usuario"))
        yield Header()
        with VerticalScroll():
            with HorizontalGroup(id="hg_pesquisa"):
                yield Select([("genero", 'genero')], id="select_categoria")
                yield Input()
                yield Button("Remover", id="bt_remover")
                yield Button("Voltar", id="bt_voltar")
            yield ListView(id="lst_item")
            yield Footer()

    def on_mount(self):
        self.query_one(Tabs).active = self.query_one("#tab_comprar", Tab).id
        # self.produtos = Init.loja.get_estoque().get_lista_produtos_disponiveis()

        self.atualizar_imagens()

        lista_categorias = []
        for produto in self.produtos:
            if produto.get_categoria() not in lista_categorias:
                lista_categorias.append(produto.get_categoria())
        self.query_one(Select).set_options(
            [(categoria, categoria) for categoria in lista_categorias])
        self.atualizar_imagens()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_carrinho_compras", Tab).id:
            self.app.switch_screen("tela_carrinho_compras")
        elif event.tabs.active == self.query_one("#tab_dados_usuario", Tab).id:
            self.app.switch_screen("tela_dados_usuario")

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
                    self.produtos_filtrados = []
                self.filtrou_select = False
                self.atualizar_imagens()
            else:
                valor_select = str(evento.value)
                valor_antigo = ""
                if valor_select != valor_antigo and self.filtrou_input == False and self.filtrou_select:
                    self.produtos_filtrados = []
                    valor_antigo = valor_select
                if len(self.produtos_filtrados) == 0:
                    for produto in self.produtos:
                        if produto.get_categoria() == valor_select:
                            self.produtos_filtrados.append(produto)
                else:
                    produtos_temp = []
                    for produto in self.produtos_filtrados:
                        if produto.get_categoria() == valor_select:
                            produtos_temp.append(produto)
                    if len(produtos_temp) > 0:
                        self.produtos_filtrados = produtos_temp

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

            if len(self.produtos_filtrados) > 0:
                produtos_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.produtos_filtrados:
                            if type(filtro) == int:
                                if p == getattr(produto, campo)() and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                            else:
                                if p in getattr(produto, campo)() and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                else:
                    for produto in self.produtos_filtrados:
                        if type(filtro) == int:
                            if filtro == getattr(produto, campo)() and produto not in produtos_temp:
                                produtos_temp.append(produto)
                        else:
                            if filtro in getattr(produto, campo)() and produto not in produtos_temp:
                                produtos_temp.append(produto)
                if len(produtos_temp) > 0:
                    self.produtos_filtrados = produtos_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.produtos:
                            if type(filtro) == int:
                                if p == getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                    self.produtos_filtrados.append(
                                        produto)
                            else:
                                if p in getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                    self.produtos_filtrados.append(
                                        produto)
                else:
                    for produto in self.produtos:
                        if type(filtro) == int:
                            if filtro == getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)
                        else:
                            if filtro in getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value
        palavras = texto.split()

        if len(palavras) > 0:
            self.produtos_filtrados = []
            for palavra in palavras:
                if palavra[:-1].lower() in Init.um_produto.__dict__.keys():
                    index = palavras.index(palavra)
                    self.filtro(palavras, index, palavra[:-1].lower())
                    self.atualizar_imagens()
        else:
            self.atualizar_imagens()
