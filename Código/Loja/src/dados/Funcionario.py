from Pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        super().__init__(nome, cpf, rg, telefone, endereco, email)

    def __str__(self):
        return f"Funcionario [nome={self.nome}, cpf={self.cpf}, rg={self.rg}, idade={self.idade}]"
