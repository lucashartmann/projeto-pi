import bcrypt
from enum import Enum

class TipoUsuario(Enum):
    CLIENTE = 1
    GERENTE = 4
    FUNCIONARIO = 2
    ADMINISTRADOR = 3


class Usuario:
    def __init__(self, nome, email, senha, tipo, gerar_hash_senha=True):
        self.nome = nome
        self.email = email
        if gerar_hash_senha:
            senha_bytes = senha.encode('utf-8')
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(senha_bytes, salt)
            self.senha = senha_hash
        else:
            self.senha = senha
        self.tipo = tipo

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_senha(self):
        return self.senha

    def get_tipo(self):
        return self.tipo

    def set_nome(self, nome):
        self.nome = nome

    def set_email(self, email):
        self.email = email

    def set_senha(self, senha):
        self.senha = senha

    def set_tipo(self, tipo):
        self.tipo = tipo