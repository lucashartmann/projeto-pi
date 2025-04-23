from Estoque import Estoque 

class Loja:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self.estoque = Estoque()
        self.funcionarios = []
        self.clientes = []
        self.fornecedores = []
        self.quantidade_funcionarios = 0
        self.quantidade_clientes = 0
        self.quantidade_fornecedores = 0
        
        def adicionar_funcionario(self, funcionario):
            if funcionario not in self.funcionarios:
                self.funcionarios.append(funcionario)
                self.quantidade_funcionarios += 1
                return True
            return False
            
        def adicionar_cliente(self, cliente):
            if cliente not in self.clientes:
                self.clientes.append(cliente)
                self.quantidade_clientes += 1
                return True
            return False
        
        def adicionar_fornecedor(self, fornecedor):
            if fornecedor not in self.fornecedores:
                self.fornecedores.append(fornecedor)
                self.quantidade_fornecedores += 1
                return True
            return False
            
        def remover_funcionario(self, funcionario):
            if funcionario in self.funcionarios:
                self.funcionarios.remove(funcionario)
                self.quantidade_funcionarios -= 1
                return True
            return False

        def remover_cliente(self, cliente):
            if cliente in self.clientes:
                self.clientes.remove(cliente)
                self.quantidade_clientes -= 1
                return True
            return False
            
        def remover_fornecedor(self, fornecedor):
            if fornecedor in self.fornecedores:
                self.fornecedores.remove(fornecedor)
                self.quantidade_fornecedores -= 1
                return True
            return False
        
        def get_quantidade_funcionarios(self):
            return self.quantidade_funcionarios
        
        def get_quantidade_clientes(self):
            return self.quantidade_clientes
        
        def get_quantidade_fornecedores(self):
            return self.quantidade_fornecedores