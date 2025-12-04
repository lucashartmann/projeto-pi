from model.Usuario import Usuario

class Corretor(Usuario):
    def __init__(self, username, senha, email, nome, cpf_cnpj, tipo_usuario, creci):
        super().__init__(username, senha, email, nome, cpf_cnpj, tipo_usuario)
        self.creci = creci

    def get_creci(self):
        return self.creci

    def set_creci(self, value):
        self.creci = value