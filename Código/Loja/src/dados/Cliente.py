from Pessoa import Pessoa


class Cliente(Pessoa):
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        super().__init__(nome, cpf, rg, telefone, endereco, email)

    def __str__(self):
        return f"Cliente [nome={self.nome}, cpf={self.cpf}, rg={self.rg}, endereco={self.endereco}, email={self.email}, telefone={self.telefone}]"
