class Proprietario:
    def __init__(self, email, nome, cpf_cnpj):
        self.id = None
        self.email = email
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.rg = None
        self.telefones = []
        self.endereco = None
        self.data_nascimento = None

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

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
        return self.telefone

    def set_telefones(self, value):
        self.telefone = value

    def get_endereco(self):
        return self.endereco

    def set_endereco(self, value):
        self.endereco = value

    def get_data_nascimento(self):
        return self.data_nascimento

    def set_data_nascimento(self, value):
        self.data_nascimento = value
