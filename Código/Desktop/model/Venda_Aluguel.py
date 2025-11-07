class Venda_Aluguel:

    def __init__(self):
        self.id_venda = 0
        self.cpf_cliente = 0
        self.cliente = ""
        self.proprietario = ""
        self.captador = ""
        self.corretor = ""
        self.imovel = ""
        self.data_venda = ""
        self.comissao_captador = 0
        self.comissao_corretor = 0

    def get_id_venda(self):
        return self.id_venda

    def set_id_venda(self, value):
        self.id_venda = value

    def get_cpf_cliente(self):
        return self.cpf_cliente

    def set_cpf_cliente(self, value):
        self.cpf_cliente = value

    def get_cliente(self):
        return self.cliente

    def set_cliente(self, value):
        self.cliente = value

    def get_proprietario(self):
        return self.proprietario

    def set_proprietario(self, value):
        self.proprietario = value

    def get_captador(self):
        return self.captador

    def set_captador(self, value):
        self.captador = value

    def get_corretor(self):
        return self.corretor

    def set_corretor(self, value):
        self.corretor = value

    def get_imovel(self):
        return self.imovel

    def set_imovel(self, value):
        self.imovel = value

    def get_data_venda(self):
        return self.data_venda

    def set_data_venda(self, value):
        self.data_venda = value

    def get_comissao_captador(self):
        return self.comissao_captador

    def set_comissao_captador(self, value):
        self.comissao_captador = value

    def get_comissao_corretor(self):
        return self.comissao_corretor

    def set_comissao_corretor(self, value):
        self.comissao_corretor = value
