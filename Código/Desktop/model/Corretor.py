class Corretor():
    def __init__(self, nome, cpf_cnpj, rg, telefone, endereco, email):
        self.matricula = ""
        self.salario = 0.0
        self.cargo = ""
        self.setor = ""
        self.turno = ""
        self.username = ""
        self.senha = ""
        self.email = email
        self.telefones = []
        self.id = 0
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.rg = rg
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.idade = 0
        self.data_nascimento = ""
        self.creci = 0

    def get_matricula(self):
        return self.matricula

    def set_matricula(self, value):
        self.matricula = value

    def get_salario(self):
        return self.salario

    def set_salario(self, value):
        self.salario = value

    def get_cargo(self):
        return self.cargo

    def set_cargo(self, value):
        self.cargo = value

    def get_setor(self):
        return self.setor

    def set_setor(self, value):
        self.setor = value

    def get_turno(self):
        return self.turno

    def set_turno(self, value):
        self.turno = value

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

    def get_telefones(self):
        return self.telefones

    def set_telefones(self, value):
        self.telefones = value

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

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

    def get_telefone(self):
        return self.telefone

    def set_telefone(self, value):
        self.telefone = value

    def get_endereco(self):
        return self.endereco

    def set_endereco(self, value):
        self.endereco = value

    def get_email(self):
        return self.email

    def set_email(self, value):
        self.email = value

    def get_idade(self):
        return self.idade

    def set_idade(self, value):
        self.idade = value

    def get_data_nascimento(self):
        return self.data_nascimento

    def set_data_nascimento(self, value):
        self.data_nascimento = value
