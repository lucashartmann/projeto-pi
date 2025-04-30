class Produto:
    def __init__(self, nome, marca, modelo, cor, preco, quantidade):
        self.id = id =+ 1
        self.nome = nome
        self.codigo = None
        self.cor = cor
        self.preco = preco
        self.marca = marca
        self.modelo = modelo
        self.quantidade = quantidade

    def get_quantidade(self):
        return self.quantidade
    
    def get_nome(self):
        return self.nome
    
    def get_codigo(self):
        return self.codigo
    
    def get_marca(self):
        return self.marca

    def get_modelo(self):
        return
    def get_cor(self):
        return self.cor

    def get_preco(self):
        return self.preco
    
    def get_id(self):
        return self.id
    

    def __str__(self):
        return (f"Produto [id = {self.get_id}, nome={self.get_nome}, codigo={self.get_codigo}, cor={self.get_cor}, "
                f"preco={self.get_preco}, marca={self.get_marca}, modelo={self.get_modelo}]")