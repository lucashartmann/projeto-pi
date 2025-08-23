from textual.widgets import Input, Pretty, TextArea, Button, Checkbox, Footer, Header, Select
from textual.screen import Screen
from textual.containers import HorizontalGroup
from controller import Controller
from textual import on


class TelaEstoque(Screen):

    CSS_PATH = "css/TelaEstoque.tcss"

    def compose(self):
        yield Header()
        with HorizontalGroup(id="hg_pesquisa"):
            yield Select([("produto", 'produto')])
            yield Input()
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        with HorizontalGroup(id="container"):
            pass
        yield Footer()

    produtos = Controller.ver_produtos_estoque()
    produtos_filtrados = []
    filtrou_checkbox = False
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    checkbox_evento = ""

    def montar_checkboxes(self):
        lista_categorias = []
        horizontal = self.query_one("#container", HorizontalGroup)
        for produto in self.produtos:
            if produto.get_categoria() not in lista_categorias:
                horizontal.mount(Checkbox(produto.get_categoria()))
                lista_categorias.append(produto.get_categoria())
        self.query_one(Select).set_options(
            [(categoria, categoria) for categoria in lista_categorias])

    def setup_dados(self):
        if len(self.produtos_filtrados) > 0:
            quant = len(self.produtos_filtrados)
        else:
            quant = len(self.produtos)
        self.query_one(TextArea).text = f"Quantidade de produtos: {quant}"

    def on_mount(self):
        produtos_str = [str(produto) for produto in self.produtos]
        self.mount(Pretty(produtos_str))
        self.montar_checkboxes()
        self.setup_dados()

    def on_button_pressed(self):
        self.screen.app.switch_screen("tela_inicial")

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        if evento.select.is_blank():
            if self.filtrou_input == False and self.filtrou_checkbox == False and self.filtrou_select:
                self.produtos_filtrados = []
            produtos_str = [str(produto) for produto in self.produtos]
            self.query_one(Pretty).update(produtos_str)
            self.setup_dados()
            self.filtrou_select = False
        else:
            valor_select = str(evento.value)
            valor_antigo = ""
            if valor_select != valor_antigo and self.filtrou_input == False and self.filtrou_checkbox == False and self.filtrou_select:
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

            produtos_str = [str(produto)for produto in self.produtos_filtrados]
            self.query_one(Pretty).update(produtos_str)
            self.setup_dados()
            self.filtrou_select = True
            self.select_evento = evento

    @on(Checkbox.Changed)
    def checkbox_changed(self, evento: Checkbox.Changed):
        valor_checkbox = str(evento.checkbox.label)
        if evento.checkbox.value is False:
            if self.filtrou_input == False and self.filtrou_select == False and self.filtrou_checkbox:
                self.produtos_filtrados = []
            produtos_str = [str(produto) for produto in self.produtos]
            self.query_one(Pretty).update(produtos_str)
            self.setup_dados()
            self.filtrou_checkbox = False
        else:
            if self.filtrou_input == False and self.filtrou_select == False and self.filtrou_checkbox:
                self.produtos_filtrados = []
            if len(self.produtos_filtrados) == 0:
                for produto in self.produtos:
                    if produto.get_categoria() == valor_checkbox:
                        self.produtos_filtrados.append(produto)
            else:
                produtos_temp = []
                for produto in self.produtos_filtrados:
                    if produto.get_categoria() == valor_checkbox:
                        produtos_temp.append(produto)
                if len(produtos_temp) > 0:
                    self.produtos_filtrados = produtos_temp
            produtos_str = [str(produto)for produto in self.produtos_filtrados]
            self.query_one(Pretty).update(produtos_str)
            self.setup_dados()
            self.filtrou_checkbox = True
            self.checkbox_evento = evento

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        resultado = self.query_one(Pretty)
        palavras = texto.split()

        if len(palavras) > 0:
            if self.filtrou_select == False and self.filtrou_checkbox == False:
                self.produtos_filtrados = []

            for palavra in palavras:
                match palavra:

                    case "MARCA:":  # TODO: Permitir multiplas marcas
                        index = palavras.index("MARCA:")
                        if index + 1 < len(palavras):
                            marca_busca = " ".join((palavras[index+1:]))
                            if "," in marca_busca:
                                marca_busca = marca_busca[0:marca_busca.index(
                                    ",")]
                            if len(self.produtos_filtrados) > 0:
                                produtos_temp = []
                                for produto in self.produtos_filtrados:
                                    if marca_busca in produto.get_marca():
                                        produtos_temp.append(produto)
                                if len(produtos_temp) > 0:
                                    self.produtos_filtrados = produtos_temp
                            else:
                                for produto in self.produtos:
                                    if marca_busca in produto.get_marca():
                                        self.produtos_filtrados.append(produto)

                    case "VALOR:":
                        index = palavras.index("VALOR:")
                        if index + 1 < len(palavras):
                            try:
                                valor_busca = " ".join((palavras[index+1:]))
                                if "," in valor_busca:
                                    valor_busca = valor_busca[0:valor_busca.index(
                                        ",")]
                                valor_busca = float(valor_busca)
                                if len(self.produtos_filtrados) > 0:
                                    produtos_temp = []
                                    for produto in self.produtos_filtrados:
                                        if produto.get_preco() == valor_busca:
                                            produtos_temp.append(produto)
                                    if len(produtos_temp) > 0:
                                        self.produtos_filtrados = produtos_temp
                                else:
                                    for produto in self.produtos:
                                        if produto.get_preco() == valor_busca:
                                            self.produtos_filtrados.append(
                                                produto)
                            except ValueError:
                                self.notify("Valor inválido")

                    case "NOME:":
                        index = palavras.index("NOME:")
                        if index + 1 < len(palavras):
                            nome_busca = " ".join((palavras[index+1:]))
                            if "," in nome_busca:
                                nome_busca = nome_busca[0:nome_busca.index(
                                    ",")]
                            if len(self.produtos_filtrados) > 0:
                                produtos_temp = []
                                for produto in self.produtos_filtrados:
                                    if nome_busca in produto.get_nome():
                                        produtos_temp.append(produto)
                                if len(produtos_temp) > 0:
                                    self.produtos_filtrados = produtos_temp
                            else:
                                for produto in self.produtos:
                                    if nome_busca in produto.get_nome():
                                        self.produtos_filtrados.append(produto)

                    case "QUANTIDADE:":
                        index = palavras.index("QUANTIDADE:")
                        if index + 1 < len(palavras):
                            try:
                                quantidade_busca = " ".join(
                                    (palavras[index+1:]))
                                if "," in quantidade_busca:
                                    quantidade_busca = quantidade_busca[0:quantidade_busca.index(
                                        ",")]
                                quantidade_busca = int(quantidade_busca)
                                if len(self.produtos_filtrados) > 0:
                                    produtos_temp = []
                                    for produto in self.produtos_filtrados:
                                        if produto.get_quantidade() == quantidade_busca:
                                            produtos_temp.append(produto)
                                    if len(produtos_temp) > 0:
                                        self.produtos_filtrados = produtos_temp
                                else:
                                    for produto in self.produtos:
                                        if produto.get_quantidade() == quantidade_busca:
                                            self.produtos_filtrados.append(
                                                produto)
                            except ValueError:
                                self.notify("Valor inválido")

                    case "MODELO:":
                        index = palavras.index("MODELO:")
                        if index + 1 < len(palavras):
                            modelo_busca = " ".join((palavras[index+1:]))
                            if "," in modelo_busca:
                                modelo_busca = modelo_busca[0:modelo_busca.index(
                                    ",")]
                            if len(self.produtos_filtrados) > 0:
                                produtos_temp = []
                                for produto in self.produtos_filtrados:
                                    if modelo_busca in produto.get_modelo():
                                        produtos_temp.append(produto)
                                if len(produtos_temp) > 0:
                                    self.produtos_filtrados = produtos_temp
                            else:
                                for produto in self.produtos:
                                    if modelo_busca in produto.get_modelo():
                                        self.produtos_filtrados.append(produto)

                    case "COR:":
                        index = palavras.index("COR:")
                        if index + 1 < len(palavras) and len(palavras[index + 1]) > 3:
                            cor_busca = " ".join((palavras[index+1:]))
                            if "," in cor_busca:
                                cor_busca = cor_busca[0:cor_busca.index(
                                    ",")]
                            if len(self.produtos_filtrados) > 0:
                                produtos_temp = []
                                for produto in self.produtos_filtrados:
                                    if cor_busca in produto.get_cor():
                                        produtos_temp.append(produto)
                                if len(produtos_temp) > 0:
                                    self.produtos_filtrados = produtos_temp
                            else:
                                for produto in self.produtos:
                                    if cor_busca in produto.get_cor():
                                        self.produtos_filtrados.append(produto)

                    case "ID:":
                        index = palavras.index("ID:")
                        if index + 1 < len(palavras):
                            try:
                                id_busca = " ".join((palavras[index+1:]))
                                if "," in id_busca:
                                    id_busca = id_busca[0:id_busca.index(
                                        ",")]
                                id_busca = int(id_busca)
                                if len(self.produtos_filtrados) > 0:
                                    produtos_temp = []
                                    for produto in self.produtos_filtrados:
                                        if produto.get_id() == id_busca:
                                            produtos_temp.append(produto)
                                    if len(produtos_temp) > 0:
                                        self.produtos_filtrados = produtos_temp
                                else:
                                    for produto in self.produtos:
                                        if produto.get_id() == id_busca:
                                            self.produtos_filtrados.append(
                                                produto)
                            except ValueError:
                                self.notify("Valor inválido")

                    case "CATEGORIA:":
                        index = palavras.index("CATEGORIA:")
                        if index + 1 < len(palavras):
                            categoria_busca = " ".join((palavras[index+1:]))
                            if "," in categoria_busca:
                                categoria_busca = categoria_busca[0:categoria_busca.index(
                                    ",")]
                            if len(self.produtos_filtrados) > 0:
                                produtos_temp = []
                                for produto in self.produtos_filtrados:
                                    if categoria_busca in produto.get_categoria():
                                        produtos_temp.append(produto)
                                if len(produtos_temp) > 0:
                                    self.produtos_filtrados = produtos_temp
                            else:
                                for produto in self.produtos:
                                    if categoria_busca in produto.get_categoria():
                                        self.produtos_filtrados.append(produto)

                if len(self.produtos_filtrados) > 0:
                    produtos_str = [str(produto)
                                    for produto in self.produtos_filtrados]
                    resultado.update(produtos_str)
                    self.setup_dados()
                else:
                    produtos_str = [str(produto) for produto in self.produtos]
                    resultado.update(produtos_str)
                    self.setup_dados()
        else:
            if len(self.produtos_filtrados) > 0 and self.filtrou_select == False and self.filtrou_checkbox == False:
                produtos_str = [str(produto)
                                for produto in self.produtos_filtrados]
                resultado.update(produtos_str)
                self.setup_dados()
            elif self.filtrou_checkbox:
                self.checkbox_changed(self.checkbox_evento)
            elif self.filtrou_select:
                self.select_changed(self.select_evento)
            else:
                produtos_str = [str(produto) for produto in self.produtos]
                resultado.update(produtos_str)
                self.setup_dados()
