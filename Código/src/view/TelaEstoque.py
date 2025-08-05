from textual.widgets import Input, Pretty, TextArea, Button, Checkbox
from textual.screen import Screen
from textual.containers import HorizontalGroup
from controller.Controller import Controller


class TelaEstoque(Screen):

    CSS_PATH = "css/TelaEstoque.tcss"

    def compose(self):
        with HorizontalGroup():
            yield Input()
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        with HorizontalGroup(id="container"):
            pass

    produtos = Controller.ver_produtos_estoque(Controller)
    produtos_filtrados = []

    def montar_checkboxes(self):
        lista_categorias = []
        horizontal = self.query_one("#container", HorizontalGroup)
        for produto in self.produtos:
            if produto.get_categoria() not in lista_categorias:
                horizontal.mount(Checkbox(produto.get_categoria()))
                lista_categorias.append(produto.get_categoria())

    def on_mount(self):
        Controller.init(Controller)
        produtos_str = [str(produto) for produto in self.produtos]
        self.mount(Pretty(produtos_str))
        self.montar_checkboxes()

    def on_button_pressed(self):
        self.screen.app.switch_screen("tela_inicial")

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value
        resultado = self.query_one(Pretty)
        palavras = texto.split()

        if len(palavras) > 1:
            self.produtos_filtrados = []
            if "marca:" in palavras: # TODO: Permitir multiplas marcas
                index = palavras.index("marca:")
                if index + 1 < len(palavras):
                    marca_busca = palavras[index + 1]
                    if len(self.produtos_filtrados) > 0:
                        produtos_temp = []
                        for produto in self.produtos_filtrados:
                            if produto.get_marca() == marca_busca:
                                produtos_temp.append(produto)
                        if len(produtos_temp) > 0:
                            self.produtos_filtrados = produtos_temp
                    else:
                        for produto in self.produtos:
                            if produto.get_marca() == marca_busca:
                                self.produtos_filtrados.append(produto)

            if "valor:" in palavras:
                index = palavras.index("valor:")
                if index + 1 < len(palavras):
                    try:
                        valor_busca = float(palavras[index + 1])
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
                                    self.produtos_filtrados.append(produto)
                    except ValueError:
                        self.notify("Valor inválido")

            if "nome:" in palavras:
                index = palavras.index("nome:")
                if index + 1 < len(palavras):
                    nome_busca = palavras[index + 1]
                    if len(self.produtos_filtrados) > 0:
                        produtos_temp = []
                        for produto in self.produtos_filtrados:
                            if produto.get_nome() == nome_busca:
                                produtos_temp.append(produto)
                        if len(produtos_temp) > 0:
                            self.produtos_filtrados = produtos_temp
                    else:
                        for produto in self.produtos:
                            if produto.get_nome() == nome_busca:
                                self.produtos_filtrados.append(produto)

            if "quantidade:" in palavras:
                index = palavras.index("quantidade:")
                if index + 1 < len(palavras):
                    try:
                        quantidade_busca = int(palavras[index + 1])
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
                                    self.produtos_filtrados.append(produto)
                    except ValueError:
                        self.notify("Valor inválido")

            if "modelo:" in palavras:
                index = palavras.index("modelo:")
                if index + 1 < len(palavras):
                    modelo_busca = palavras[index + 1].upper()
                    if len(self.produtos_filtrados) > 0:
                        produtos_temp = []
                        for produto in self.produtos_filtrados:
                            if produto.get_modelo() == modelo_busca:
                                produtos_temp.append(produto)
                        if len(produtos_temp) > 0:
                            self.produtos_filtrados = produtos_temp
                    else:
                        for produto in self.produtos:
                            if produto.get_modelo() == modelo_busca:
                                self.produtos_filtrados.append(produto)

            if "cor:" in palavras:
                index = palavras.index("cor:")
                if index + 1 < len(palavras) and len(palavras[index + 1]) > 3:
                    cor_busca = palavras[index + 1]
                    if len(self.produtos_filtrados) > 0:
                        produtos_temp = []
                        for produto in self.produtos_filtrados:
                            if produto.get_cor() == cor_busca:
                                produtos_temp.append(produto)
                        if len(produtos_temp) > 0:
                            self.produtos_filtrados = produtos_temp
                    else:
                        for produto in self.produtos:
                            if produto.get_cor() == cor_busca:
                                self.produtos_filtrados.append(produto)

            if "id:" in palavras:
                index = palavras.index("id:")
                if index + 1 < len(palavras):
                    try:
                        id_busca = int(palavras[index + 1])
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
                                    self.produtos_filtrados.append(produto)
                    except ValueError:
                        self.notify("Valor inválido")

            if "categoria:" in palavras:
                index = palavras.index("categoria:")
                if index + 1 < len(palavras):
                    categoria_busca = palavras[index + 1]
                    if len(self.produtos_filtrados) > 0:
                        produtos_temp = []
                        for produto in self.produtos_filtrados:
                            if produto.get_categoria() == categoria_busca:
                                produtos_temp.append(produto)
                        if len(produtos_temp) > 0:
                            self.produtos_filtrados = produtos_temp
                    else:
                        for produto in self.produtos:
                            if produto.get_categoria() == categoria_busca:
                                self.produtos_filtrados.append(produto)

            if len(self.produtos_filtrados) > 0:
                produtos_str = [str(produto)
                                for produto in self.produtos_filtrados]
                resultado.update(produtos_str)
            else:
                produtos_str = [str(produto) for produto in self.produtos]
                resultado.update(produtos_str)
        else:
            produtos_str = [str(produto) for produto in self.produtos]
            resultado.update(produtos_str)
