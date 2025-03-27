class Cliente:
    def __init__(self, id=None, nome=None, cpf=None, rg=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.idade = None 

    def __str__(self):
        return f"Cliente [nome={self.nome}, cpf={self.cpf}, rg={self.rg}, idade={self.idade}]"