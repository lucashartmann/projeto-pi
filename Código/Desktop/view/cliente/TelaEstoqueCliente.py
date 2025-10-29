from textual.widgets import Label, Button, ListItem, ListView, Footer, Header, Select, Input
from textual import on
from textual.screen import Screen
from textual.containers import VerticalScroll, HorizontalGroup, Container
from textual.binding import Binding
from model import Init
from textual_image.widget import Image as TextualImage
from io import BytesIO


class ContainerProduto(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        #     yield TextualImage("")
        #     yield Label("Dualshock")
        #     yield Label("R$ 299,99")
        yield Button("Comprar")


class TelaEstoqueCliente(Screen):

    CSS_PATH = "css/TelaEstoqueCliente.tcss"

    BINDINGS = [
        Binding("ctrl+l", "app.switch_screen('tela_inicial')", "Voltar")
    ]

    produtos = Init.loja.get_estoque().get_lista_produtos()
    produtos_filtrados = []

    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    montou = False

    produtos_etiquetados = dict()

    def atualizar_imagens(self):
        self.produtos = Init.loja.get_estoque().get_lista_produtos()
        list_view = self.query_one("#lst_item", ListView)
        list_view.clear()
        lista = self.produtos
        if len(self.produtos_filtrados) > 0:
            lista = self.produtos_filtrados

        for produto in lista:
            if produto.get_codigo() not in self.produtos_etiquetados.keys():
                if produto.get_imagem():
                    container = ContainerProduto()
                    list_item = ListItem(name=produto.get_nome())
                    list_view.append(list_item)
                    list_item.mount(container)
                    imagem = TextualImage(BytesIO(produto.get_imagem()))
                    imagem.styles.height = 13
                    imagem.styles.width = 30
                    container.mount(imagem, before=container.query_one(Button))
                    container.mount(Label(content=produto.get_nome(
                    ), id="tx_nome"), after=container.query_one(TextualImage))
                    container.mount(Label(
                        content=f"R$ {produto.get_preco():.2f}", id="tx_preco"), after=container.query_one("#tx_nome"))

                    list_item.styles.width = 30
                    list_item.styles.height = 30

    def _on_screen_resume(self):
        self.produtos = Init.loja.get_estoque().get_lista_produtos()

        self.atualizar_imagens()

        lista_categorias = []
        for produto in self.produtos:
            if produto.get_categoria() not in lista_categorias:
                lista_categorias.append(produto.get_categoria())
        self.query_one(Select).set_options(
            [(categoria, categoria) for categoria in lista_categorias])
        self.atualizar_imagens()

    def compose(self):
        yield Header()
        with VerticalScroll():
            with HorizontalGroup(id="hg_pesquisa"):
                yield Select([("genero", 'genero')])
                yield Input()
                yield Button("Remover", id="bt_remover")
                yield Button("Voltar", id="bt_voltar")
            yield ListView(id="lst_item")
            yield Label("item", id="tx_info")

            yield Footer()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_remover":
                input_id = self.query_one(Input).value
                self.atualizar_imagens()

    def on_list_view_highlighted(self, evento: ListView.Highlighted):
        self.query_one("#tx_info", Label).update(
            evento.list_view.highlighted_child.name)

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
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
