from model import Banco


class Estoque:

    def __init__(self):
        self.banco_dados = Banco.Banco()

    def adicionar_produto(self, produto):
        return self.banco_dados.adicionar_produto(produto)

    def remover_produto(self, produto):
        return self.banco_dados.remover_produto(produto.get_id())

    def get_lista_produtos(self):
        return self.banco_dados.get_lista_produtos()

    def get_produtos_por_nome(self, nome):
        return self.banco_dados.get_produtos_por_nome(nome)

    def get_produtos_por_marca(self, marca):
        return self.banco_dados.get_produtos_por_marca(marca)

    def get_produtos_por_modelo(self, modelo):
        return self.banco_dados.get_produtos_por_modelo(modelo)

    def get_produtos_por_categoria(self, categoria):
        return self.banco_dados.get_produtos_por_categoria(categoria)

    def get_produto_por_id(self, id):
        return self.banco_dados.get_produto_por_id(id)

    def get_quantidade_produto_por_marca(self, marca):
        return self.banco_dados.get_quantidade_produto_por_marca(marca)

    def get_quantidade_produto_por_modelo(self, modelo):
        return self.banco_dados.get_quantidade_produto_por_modelo(modelo)

    def get_quantidade_produto_por_categoria(self, categoria):
        return self.banco_dados.get_quantidade_produto_por_categoria(categoria)

    def get_quantidade_produtos(self):
        return self.banco_dados.get_quantidade_produtos()
