class Venda:
    def __init__(self, cliente):
        self.cliente = cliente
        self.produto = []
        self.quantidade = 0

    def adicionar_produto(self, produto):
        self.produto.append(produto)
    
    def remover_produto(self, produto):
        self.produto.remove(produto)

    def set_quantidade(self, quantidade):
        quantidade = 0
        for produto in self.produto:
            quantidade = quantidade + produto.get_quantidade()
        return quantidade

    def __str__(self):
            return f"Venda [cliente={self.cliente}, produto={self.produto}, quantidade={self.quantidade}]"