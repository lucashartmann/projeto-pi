from model.Pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        super().__init__(nome, cpf, rg, telefone, endereco, email)
        self.matricula = ""
        self.salario = 0.0
        self.cargo = ""
        self.idade = 0
        self.data_nascimento = ""
        self.setor = ""
        self.turno = ""

    def __str__(self):
        return f"Funcionario [nome={self.get_nome()}, cpf={self.get_cpf()}, rg={self.get_rg()}, idade={self.get_idade()}]"
