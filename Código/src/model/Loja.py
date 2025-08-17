from model.Estoque import Estoque
from model.Funcionario import Funcionario
from model.Cliente import Cliente
from model.Fornecedor import Fornecedor


class Loja:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self.estoque = Estoque()
        self.pessoas = []
        self.quantidade_funcionarios = self.set_quantidade()
        self.quantidade_clientes = self.set_quantidade()
        self.quantidade_fornecedores = self.set_quantidade()
        self.faturamento = 0

    def cadastrar(self, pessoa):
        if pessoa not in self.pessoas:
            self.pessoas.append(pessoa)
            self.set_quantidade()
            return True
        return False

    def remover(self, pessoa):
        if pessoa in self.pessoas:
            self.pessoas.remove(pessoa)
            self.set_quantidade()
            return True
        return False

    def set_quantidade(self):
        self.quantidade_clientes = 0
        self.quantidade_fornecedores = 0
        self.quantidade_funcionarios = 0

        for pessoa in self.pessoas:
            if isinstance(pessoa, Cliente):
                self.quantidade_clientes += 1
            elif isinstance(pessoa, Fornecedor):
                self.quantidade_fornecedores += 1
            self.quantidade_funcionarios += 1
    
    def get_lista_clientes(self):
        clientes = []
        for pessoa in self.pessoas:
            if isinstance(pessoa, Cliente):
                clientes.append(pessoa)
        return clientes

    def get_estoque(self):
        return self.estoque

    def get_nome(self):
        return self.nome

    def get_cnpj(self):
        return self.cnpj

    def get_quantidade_funcionarios(self):
        return self.quantidade_funcionarios

    def get_quantidade_clientes(self):
        return self.quantidade_clientes

    def get_quantidade_fornecedores(self):
        return self.quantidade_fornecedores

    def get_faturamento(self):
        return self.faturamento

    def get_cliente_por_cpf(self, cpf):
        for cliente in self.clientes:
            if cliente.get_cpf() == cpf:
                return cliente
        return None

    def get_produto_por_id(self, id):
        for produto in self.estoque.get_lista_produtos():
            if produto.get_id() == id:
                return produto
        return None

    def is_cpf_cadastrado(self, cpf):
        for pessoa in self.pessoas:
            if pessoa.get_cpf() == cpf:
                return True
        return False

    def is_rg_cadastrado(self, rg):
        for pessoa in self.pessoas:
            if pessoa.get_rg() == rg:
                return True
        return False

    def is_telefone_cadastrado(self, telefone):
        for pessoa in self.pessoas:
            if pessoa.get_telefone() == telefone:
                return True
        return False
