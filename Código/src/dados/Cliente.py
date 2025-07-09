from dados.Pessoa import Pessoa
from dados.Carrinho import Carrinho


class Cliente(Pessoa):
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        super().__init__(nome, cpf, rg, telefone, endereco, email)
        self.isCadastrado = False
        self.carrinho = Carrinho()

    def get_is_cadastrado(self):
        return self.isCadastrado

    def set_is_cadastrado(self, isCadastrado):
        self.isCadastrado = isCadastrado

    def get_carrinho(self):
        return self.carrinho

    def __str__(self):
        return f"Cliente [nome={self.get_nome()}, cpf={self.get_cpf()}, rg={self.get_rg()}, endereco={self.get_endereco()}, email={self.get_email()}, telefone={self.get_telefone()}, isCadastrado={self.get_is_cadastrado()}]"
