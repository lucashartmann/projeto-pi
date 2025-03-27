class Funcionario:
    def __init__(self, nome, cpf, rg):
        self.id = None  
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.idade = None  

    def __str__(self):
        return f"Funcionario [nome={self.nome}, cpf={self.cpf}, rg={self.rg}, idade={self.idade}]"