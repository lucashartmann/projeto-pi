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
        self.tipo= tipo