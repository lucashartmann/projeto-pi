from model import Pessoa

class Cliente(Pessoa.Pessoa):
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        super().__init__(nome, cpf, rg, telefone, endereco, email)

    def __str__(self):
        return f"Cliente [nome={self.get_nome()}, cpf={self.get_cpf()}, rg={self.get_rg()}, endereco={self.get_endereco()}, email={self.get_email()}, telefone={self.get_telefone()}]"
