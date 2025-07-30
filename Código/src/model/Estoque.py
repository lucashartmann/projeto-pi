class Estoque:
    def __init__(self):
        self.produtos = list()

    def adicionar_produto(self, produto):
        if produto not in self.produtos:
            self.produtos.append(produto)
            return True
        return False

    def remover_produto(self, produto):
        if produto in self.produtos:
            self.produtos.remove(produto)
            return True
        return False

    def get_lista_produtos(self):
        return self.produtos

    def verifica_produto(self, produto):
        if produto in self.produtos:
            return True
        return False

    def get_produtos_por_nome(self, nome):
        produtos = []
        for produto in self.produtos:
            if produto.get_nome() == nome:
                produtos.append(produto)
        if len(produtos) > 0:
            return produtos
        return None

    def get_produtos_por_marca(self, marca):
        produtos = []
        for produto in self.produtos:
            if produto.get_marca() == marca:
                produtos.append(produto)
        if len(produtos) > 0:
            return produtos
        return None

    def get_produtos_por_modelo(self, modelo):
        produtos = []
        for produto in self.produtos:
            if produto.get_modelo() == modelo:
                produtos.append(produto)
        if len(produtos) > 0:
            return produtos
        return None

    def get_produtos_por_categoria(self, categoria):
        produtos = []
        for produto in self.produtos:
            if produto.get_categoria() == categoria:
                produtos.append(produto)
        if len(produtos) > 0:
            return produtos
        return None

    def get_produto_por_id(self, id):
        for produto in self.produtos:
            if produto.get_id() == id:
                return produto
        return None

    def get_quantidade_produto_por_marca(self, marca):
        quantidade = 0
        for produto in self.produtos:
            if produto.get_marca() == marca:
                quantidade += produto.get_quantidade()
        return quantidade

    def get_quantidade_produto_por_modelo(self, modelo):
        quantidade = 0
        for produto in self.produtos:
            if produto.get_modelo() == modelo:
                quantidade += produto.get_quantidade()
        return quantidade

    def get_quantidade_produto_por_categoria(self, categoria):
        quantidade = 0
        for produto in self.produtos:
            if produto.get_categoria() == categoria:
                quantidade += produto.get_quantidade()
        return quantidade

    def get_quantidade_produtos(self):
        quantidade = 0
        for produto in self.produtos:
            quantidade += produto.get_quantidade()
        return quantidade

    def __str__(self):
        if not self.produtos:
            return "Estoque: Vazio"
        
        resultado = "Estoque:\n"
        for produto in self.produtos:
            resultado += f"  - {produto}\n"
        return resultado