class Endereco:

    def __init__(self, rua, bairro, cep, cidade, uf):
        self.id = None
        self.rua = rua
        self.numero = None
        self.bairro = bairro
        self.cep = cep
        self.complemento = None
        self.cidade = cidade
        self.uf = uf

    def get_uf(self):
        return self.uf

    def set_uf(self, uf):
        self.uf = uf

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_rua(self):
        return self.rua

    def set_rua(self, value):
        self.rua = value

    def get_numero(self):
        return self.numero

    def set_numero(self, value):
        self.numero = value

    def get_bairro(self):
        return self.bairro

    def set_bairro(self, value):
        self.bairro = value

    def get_cep(self):
        return self.cep

    def set_cep(self, value):
        self.cep = value

    def get_complemento(self):
        return self.complemento

    def set_complemento(self, value):
        self.complemento = value

    def get_cidade(self):
        return self.cidade

    def set_cidade(self, value):
        self.cidade = value
