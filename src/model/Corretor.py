from model.Usuario import Usuario, Tipo

class Corretor(Usuario):
    def __init__(self, username, senha, email, nome, cpf_cnpj, creci):
        super().__init__(username, senha, email, nome, cpf_cnpj, Tipo.CORRETOR)
        self.creci = creci

    def get_creci(self):
        return self.creci

    def set_creci(self, value):
        self.creci = value