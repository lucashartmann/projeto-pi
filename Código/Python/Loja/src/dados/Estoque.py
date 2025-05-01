class Estoque:
    def __init__(self):
        self.produtos = []
        self.quantidade = 0
        
    def adicionar_produto(self, produto):
        if(produto not in self.produtos):
            self.produtos.append(produto)
            self.quantidade += 1
            return True
        return False
    
    def remover_produto(self, produto):
        if(produto in self.produtos):
            self.produtos.remove(produto)
            self.quantidade -= 1
            return True
        return False
    
    def get_lista_produtos(self):
        return self.produtos
        
    def get_quantidade(self):
        return self.quantidade
    
    def consultar_produtos_por_nome(self, nome):
        produtos = []
        for produto in self.produtos:
            if(produto.nome == nome):
                produtos.append(produto)
        if(len(produtos) > 0):
            return produtos
        return None

    def consultar_produto_por_id(self, id):
        for produto in self.produtos:
            if(produto.id == id):
                return produto
        return None