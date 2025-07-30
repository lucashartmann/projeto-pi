from model.Pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        super().__init__(nome, cpf, rg, telefone, endereco, email)

    def __str__(self):
        return f"Funcionario [nome={self.get_nome()}, cpf={self.get_cpf()}, rg={self.get_rg()}, idade={self.get_idade()}]"
