from datetime import datetime


class Pedido:
    def __init__(self):
        self.cupom_aplicado = ""
        self.itens = []
        self.status = ""
        self.id_cliente = 0
        self.billing = object
        self.shipping = object
        self.data_criado = datetime(2025, 1, 1)
        self.data_modificado = datetime(2025, 1, 1)
        self.desconto = ""
        self.frete = ""
        self.total = ""
        self.data_pago = datetime(2025, 1, 1)
        self.data_concluido = datetime(2025, 1, 1)
        self.refunds = []
