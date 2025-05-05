class Pessoa:
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.telefone = telefone
        self.endereco = endereco
        self.email = email

    def get_cpf(self):
        return self.cpf
