from model.Usuario import Usuario


class Cliente(Usuario):
    def __init__(self, username, senha, email, nome, cpf_cnpj, tipo_usuario):
        super().__init__(username, senha, email, nome, cpf_cnpj, tipo_usuario)
        self.tipo_imoveis_desejado = []
        self.quant_quartos_desejado = 0
        self.quant_banheiros_desejado = 0
        self.endereco_desejado = None

    def set_tipos_imoveis_desejados(self, tipo_imoveis):
        self.tipo_imoveis_desejado = tipo_imoveis

    def set_quat_quartos_desejado(self, quant_quartos_desejado):
        self.quant_quartos_desejado = quant_quartos_desejado

    def set_quant_banheiros_desejado(self, quant_banheiros_desejado):
        self.quant_banheiros_desejado = quant_banheiros_desejado

    def set_endereco_desejado(self, endereco):
        self.endereco_desejado = endereco
