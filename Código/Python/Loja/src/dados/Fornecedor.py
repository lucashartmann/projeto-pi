class Fornecedor:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def __str__(self):
        return f"Fornecedor [nome={self.nome}, cpf={self.cpf}]"