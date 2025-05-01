from Pessoa import Pessoa

class Fornecedor(Pessoa):
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        super().__init__(nome, cpf, rg, telefone, endereco, email)

    def __str__(self):
        return f"Fornecedor [nome={self.nome}, cpf={self.cpf}]"