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
    
    def set_nome(self, nome):
        self.nome = nome

    def set_cpf(self, cpf):
        self.cpf = cpf
    
    def set_rg(self, rg):
        self.rg = rg

    def set_telefone(self, telefone):
        self.telefone = telefone

    def set_endereco(self, endereco):
        self.endereco = endereco
    
    def set_email(self, email):
        self.email = email