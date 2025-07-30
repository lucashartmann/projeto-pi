from textual.app import App
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Input, Pretty, TextArea
from textual.screen import Screen
from controller.Controller import Controller


class TelaEstoque(Screen):

    CSS_PATH = "css/TelaEstoque.tcss"

    def compose(self):
        yield Input()
        yield TextArea(disabled=True)

    produtos = Controller.loja.get_estoque().get_lista_produtos()
    produtos_filtrados = []

    def on_mount(self):
        Controller.init(Controller)
        produtos_str = [str(produto) for produto in self.produtos]
        self.mount(Pretty(produtos_str))

    def on_input_changed(self, evento):
        texto = self.query_one(Input).value
        resultado = self.query_one(Pretty)
        palavras = texto.split()

        if len(palavras) > 1:
            if "marca:" in palavras:
                index = palavras.index("marca:")
                if index + 1 < len(palavras):
                    marca_busca = palavras[index + 1]
                    if len(self.produtos_filtrados) > 0 and len(palavras) > 2:
                        for produto1 in self.produtos_filtrados:
                            if produto1.get_marca() != marca_busca:
                                self.produtos_filtrados.remove(produto1)
                    else:
                        for produto in self.produtos:
                            if produto.get_marca() == marca_busca and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)

            if "valor:" in palavras:
                index = palavras.index("valor:")
                if index + 1 < len(palavras):
                    valor_busca = float(palavras[index + 1])
                    if len(self.produtos_filtrados) > 0 and len(palavras) > 2:
                        for produto1 in self.produtos_filtrados:
                            if produto1.get_preco() != valor_busca:
                                self.produtos_filtrados.remove(produto1)
                    else:
                        for produto in self.produtos:
                            if produto.get_preco() == valor_busca and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)

            if "nome:" in palavras:
                index = palavras.index("nome:")
                if index + 1 < len(palavras):
                    nome_busca = palavras[index + 1]
                    if len(self.produtos_filtrados) > 0 and len(palavras) > 2:
                        for produto1 in self.produtos_filtrados:
                            if produto1.get_nome() != nome_busca:
                                self.produtos_filtrados.remove(produto1)
                    else:
                        for produto in self.produtos:
                            if produto.get_nome() == nome_busca and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)

            if "quantidade:" in palavras:
                index = palavras.index("quantidade:")
                if index + 1 < len(palavras):
                    quantidade_busca = int(palavras[index + 1])
                    if len(self.produtos_filtrados) > 0 and len(palavras) > 2:
                        for produto1 in self.produtos_filtrados:
                            if produto1.get_quantidade() != quantidade_busca:
                                self.produtos_filtrados.remove(produto1)
                    else:
                        for produto in self.produtos:
                            if produto.get_quantidade() == quantidade_busca and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)

            if "modelo:" in palavras:
                index = palavras.index("modelo:")
                if index + 1 < len(palavras):
                    modelo_busca = palavras[index + 1].upper()
                    if len(self.produtos_filtrados) > 0 and len(palavras) > 2:
                        for produto1 in self.produtos_filtrados:
                            if produto1.get_modelo() != modelo_busca:
                                self.produtos_filtrados.remove(produto1)
                    else:
                        for produto in self.produtos:
                            if produto.get_modelo() == modelo_busca and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)

            if "cor:" in palavras:
                index = palavras.index("cor:")
                if index + 1 < len(palavras):
                    cor_busca = palavras[index + 1]
                    if len(self.produtos_filtrados) > 0 and len(palavras) > 2:
                        for produto1 in self.produtos_filtrados:
                            if produto1.get_cor() != cor_busca:
                                self.produtos_filtrados.remove(produto1)
                    else:
                        for produto in self.produtos:
                            if produto.get_cor() == cor_busca and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)

            if "id:" in palavras:
                index = palavras.index("id:")
                if index + 1 < len(palavras):
                    id_busca = int(palavras[index + 1])
                    if len(self.produtos_filtrados) > 0 and len(palavras) > 2:
                        for produto1 in self.produtos_filtrados:
                            if produto1.get_id() != id_busca:
                                self.produtos_filtrados.remove(produto1)
                    else:
                        for produto in self.produtos:
                            if produto.get_id() == id_busca and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)
                                
            if len(self.produtos_filtrados) > 0:
                produtos_str = [str(produto)
                                for produto in self.produtos_filtrados]
                resultado.update(produtos_str)
            else: 
                produtos_str = [str(produto) for produto in self.produtos]
                resultado.update(produtos_str)
