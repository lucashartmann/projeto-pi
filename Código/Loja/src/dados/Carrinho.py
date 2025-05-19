class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_produto(self, produto, quantidade):
        if quantidade <= produto.get_quantidade():
            self.itens.append({
                "produto": produto,
                "quantidade": quantidade
            })
            return True
        return False

    def remover_produto_por_id(self, id_produto):
        for item in self.itens:
            if item["produto"].get_id() == id_produto:
                self.itens.remove(item)
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
        for item in self.itens:
            produto = item["produto"]
            quantidade = item["quantidade"]
            total += produto.get_preco() * quantidade
        return total
