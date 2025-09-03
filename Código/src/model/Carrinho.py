class Carrinho:
    def __init__(self):
        self.itens = {}

    def adicionar_produto(self, produto, quantidade):
        if quantidade <= produto.get_quantidade():
            if produto not in self.itens:
                self.itens[produto] = quantidade
                return True
            else:
                self.itens[produto] += quantidade
                return True
        return False

    def remover_produto_por_id(self, id_produto):
        for produto in self.itens:
            if self.itens[produto].get_id() == id_produto:
                del self.itens[produto]
                return True
        return False

    def listar_produtos(self):
        return self.itens

    def esta_vazio(self):
        return len(self.itens) == 0

    def limpar(self):
        self.itens.clear()

    def get_total(self):
        total = 0
        for produto, quantidade in self.itens.items():
            total += produto.get_preco() * quantidade
        return total
