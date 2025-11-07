class Venda:

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

    def get_data_venda(self):
        return self.data_venda

    def set_data_venda(self, value):
        self.data_venda = value

    def get_produtos(self):
        return self.produtos

    def set_produtos(self, value):
        self.produtos = value
