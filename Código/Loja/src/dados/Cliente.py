from Pessoa import Pessoa
from Carrinho import Carrinho

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
        return f"Cliente [nome={self.nome}, cpf={self.cpf}, rg={self.rg}, endereco={self.endereco}, email={self.email}, telefone={self.telefone}, isCadastrado={self.isCadastrado}]"
