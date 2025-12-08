from database import Banco
from model import Estoque


class Imobiliaria:
    def __init__(self, nome, cnpj):
        self.banco_dados = Banco.Banco()
        self.nome = nome
        self.cnpj = cnpj
        self.estoque = Estoque.Estoque()
        self.quantidade_funcionarios = 0
        self.quantidade_clientes = 0
        self.quantidade_fornecedores = 0
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
        
    def atualizar(self, campo_desejado, valor, tabela):
        return self.banco_dados.atualizar(campo_desejado, valor, tabela)
    
    def verificar_usuario(self, 
        username, senha, tipo_usuario):
        return self.banco_dados.verificar_usuario(
        username, senha, tipo_usuario)

    def cadastrar_endereco(self, endereco):
        return self.banco_dados.cadastrar_endereco(endereco)

    def cadastrar_atendimento(self, atendimento):
        return self.banco_dados.cadastrar_atendimento(atendimento)

    def get_lista_atendimentos(self):
        return self.banco_dados.get_lista_atendimentos()

    def cadastrar_usuario(self, usuario):
        return self.banco_dados.cadastrar_usuario(usuario)
    
    def cadastrar_proprietario(self, proprietario):
        return self.banco_dados.cadastrar_proprietario(proprietario)

    def get_lista_usuarios(self):
        return self.banco_dados.get_lista_usuarios()
    
    def get_lista_usuarios_por_condicao(self, campo_desejado, valor):
        return self.banco_dados.get_lista_usuarios_por_condicao(campo_desejado, valor)
    
    def get_usuario_por_cpf(self, cpf):
        return self.banco_dados.get_usuario_por_cpf(cpf)
    
    def get_proprietario_por_cpf(self, cpf):
        return self.banco_dados.get_proprietario_por_cpf(cpf)
    
    def get_lista_clientes(self):
        return self.banco_dados.get_lista_clientes()
    
    def remover(self, campo_desejado, valor, tabela):
        return self.banco_dados.remover(campo_desejado, valor, tabela)
    
    def cadastrar_lista_filtros(self, lista_filtros, tabela):
        return self.banco_dados.cadastrar_lista_filtros(lista_filtros, tabela)
    
    def get_endereco_por_cep(self, cep):
        return self.banco_dados.get_endereco_por_cep(cep)