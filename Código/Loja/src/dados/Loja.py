import Estoque 
import Funcionario
import Cliente
import Fornecedor

class Loja:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self.estoque = Estoque()
        self.pessoas = []
        self.quantidade_funcionarios = 0
        self.quantidade_clientes = 0
        self.quantidade_fornecedores = 0
        self.faturamento = 0

        def realizar_compra(cliente, produto): #ou realizar_venda()?
            # Pedir dados do cliente?
            # Ver se cliente está cadastrado
            # Remover produto do estoque, diminuir quantidade do produto no estoque
            # Somar preço do produto ao faturamento da loja 
            # Permitir usuario de realizar mais compras? Implementar lógica de um carrinho?
            # Receber uma lista de produtos?
            # Usar um for em uma lista de produtos passando para cada produto o realizar_compra
            pass
        
        def cadastrar(self, pessoa):
            if pessoa not in self.pessoas:
                self.pessoas.append(pessoa)
                return True
            return False
            
        def remover(self, pessoa):
            if pessoa in self.pessoas:
                self.pessoas.remove(pessoa)
                return True
            return False
        
        def set_quantidade_funcionarios(self):
            for funcionario in self.pessoas:
                if isinstance(funcionario, Funcionario):
                    self.quantidade_funcionarios += 1

        def set_quantidade_clientes(self):
            for cliente in self.pessoas:
                if isinstance(cliente, Cliente):
                    self.quantidade_clientes += 1
        
        def set_quantidade_fornecedores(self):
            for fornecedor in self.pessoas:
                if isinstance(fornecedor, Fornecedor):
                    self.quantidade_fornecedores += 1
        
        def get_quantidade_funcionarios(self):
            return self.quantidade_funcionarios
        
        def get_quantidade_clientes(self):
            return self.quantidade_clientes
        
        def get_quantidade_fornecedores(self):
            return self.quantidade_fornecedores
        
        def get_faturamento(self):
            return self.faturamento
        
        def is_cliente_cadastrado(self, cpf):
            for cliente in self.clientes:
                if cliente.get_cpf() == cpf:
                    return True
            return False