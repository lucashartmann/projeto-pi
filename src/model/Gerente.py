from model.Usuario import Usuario, Tipo


class Gerente(Usuario):
    def __init__(self, username, senha, email, nome, cpf_cnpj):
        super().__init__(username, senha, email, nome, cpf_cnpj, Tipo.GERENTE)
        self.salario = 0.0

    def get_salario(self):
        return self.salario

    def set_salario(self, value):
        self.salario = value
