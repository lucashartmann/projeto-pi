from database import Banco
from model import Estoque


class Imobiliaria:
    def __init__(self, nome, cnpj):
        self.banco_dados = Banco.Banco()
        self.nome = nome
        self.cnpj = cnpj
        self.estoque = Estoque.Estoque()
        self.quantidade_funcionarios = self.set_quantidade()
        self.quantidade_clientes = self.set_quantidade()
        self.quantidade_fornecedores = self.set_quantidade()
        self.faturamento = 0

    def get_nome(self):
        return self.nome

    def set_nome(self, value):
        self.nome = value

    def get_cnpj(self):
        return self.cnpj

    def set_cnpj(self, value):
        self.cnpj = value

    def get_estoque(self):
        return self.estoque

    def set_estoque(self, value):
        self.estoque = value

    def get_quantidade_funcionarios(self):
        return self.quantidade_funcionarios

    def set_quantidade_funcionarios(self, value):
        self.quantidade_funcionarios = value

    def get_quantidade_clientes(self):
        return self.quantidade_clientes

    def set_quantidade_clientes(self, value):
        self.quantidade_clientes = value

    def get_quantidade_fornecedores(self):
        return self.quantidade_fornecedores

    def set_quantidade_fornecedores(self, value):
        self.quantidade_fornecedores = value

    def get_faturamento(self):
        return self.faturamento

    def set_faturamento(self, value):
        self.faturamento = value

        
    def verificar_usuario(self, usuario):
        return self.banco_dados.verificar_usuario(usuario)

    def cadastrar_comprador(self, comprador):
        return self.banco_dados.cadastrar_comprador(comprador)
    
    def cadastrar_proprietario(self, proprietario):
        return self.banco_dados.cadastrar_proprietario(proprietario)
    
    def cadastrar_captador(self, captador):
        return self.banco_dados.cadastrar_captador(captador)
    
    def cadastrar_corretor(self, corretor):
        return self.banco_dados.cadastrar_corretor(corretor)

    def get_lista_corretores(self):
        return self.banco_dados.get_lista_corretores()
    
    def get_lista_captadores(self):
        return self.banco_dados.get_lista_captadores()
    
    def get_lista_compradores(self):
        return self.banco_dados.get_lista_compradores()
    
    def get_lista_proprietarios(self):
        return self.banco_dados.get_lista_proprietarios()
