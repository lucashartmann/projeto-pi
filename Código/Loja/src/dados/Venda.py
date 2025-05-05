class Venda:
    def __init__(self, cliente):
        self.cliente = cliente
        self.produto = []

    def adicionar_produto(self, produto):
        self.produto.append(produto)

    def remover_produto(self, produto):
        self.produto.remove(produto)

    def __str__(self):
        return f"Venda [cliente={self.cliente}, produto={self.produto}, quantidade={self.produto.quantidade}]"
