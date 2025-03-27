class Produto:
    def __init__(self, nome, marca, modelo, cor, preco):
        self.nome = nome
        self.codigo = None
        self.cor = cor
        self.preco = preco
        self.marca = marca
        self.modelo = modelo

    def __str__(self):
        return (f"Produto [nome={self.nome}, codigo={self.codigo}, cor={self.cor}, "
                f"preco={self.preco}, marca={self.marca}, modelo={self.modelo}]")