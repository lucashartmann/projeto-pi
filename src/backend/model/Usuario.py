from enum import Enum


class Tipo(Enum):
    ADMINISTRADOR = "ADMIN"
    CORRETOR = "CORRETOR"
    GERENTE = "GERENTE"
    CAPTADOR = "CAPTADOR"
    CLIENTE = "CLIENTE"
    PROPRIETARIO = "PROPRIETARIO"


class Usuario:
    def __init__(self, username, senha, email, nome, cpf_cnpj, tipo):
        self.id = None
        self.username = username
        self.senha = senha
        self.email = email
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.rg = None
        self.telefones = []
        self.endereco = None
        self.data_nascimento = None
        self.tipo = tipo
        self.data_cadastro = None
        self.data_modificacao = None

    def set_data_cadastro(self, data):
        self.data_cadastro = data

    def get_data_cadastro(self):
        return self.data_cadastro

    def set_data_modificacao(self, data):
        self.data_modificacao = data

    def get_data_modificacao(self):
        return self.data_modificacao

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_username(self):
        return self.username

    def set_username(self, value):
        self.username = value

    def get_senha(self):
        return self.senha

    def set_senha(self, value):
        self.senha = value

    def get_email(self):
        return self.email

    def set_email(self, value):
        self.email = value

    def get_nome(self):
        return self.nome

    def set_nome(self, value):
        self.nome = value

    def get_cpf_cnpj(self):
        return self.cpf_cnpj

    def set_cpf_cnpj(self, value):
        self.cpf_cnpj = value

    def get_rg(self):
        return self.rg

    def set_rg(self, value):
        self.rg = value

    def get_telefones(self):
        return self.telefones

    def set_telefones(self, value):
        self.telefones = value

    def get_endereco(self):
        return self.endereco

    def set_endereco(self, value):
        self.endereco = value

    def get_data_nascimento(self):
        return self.data_nascimento

    def set_data_nascimento(self, value):
        self.data_nascimento = value

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, value):
        self.tipo = value
