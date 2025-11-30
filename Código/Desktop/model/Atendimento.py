from enum import Enum


class Status(Enum):
    EM_ANDAMENTO = "Em Andamento"
    PENDENTE = "Pendente"
    # RECEM_CADASTRADO = "Recém Cadastrado"


class Atendimento:

    def __init__(self):
        self.id = 0
        self.corretor = ""
        self.cliente = ""
        self.imovel = ""
        self.status = None

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def get_corretor(self):
        return self.corretor

    def set_corretor(self, value):
        self.corretor = value

    def get_cliente(self):
        return self.cliente

    def set_cliente(self, value):
        self.cliente = value

    def get_imovel(self):
        return self.imovel

    def set_imovel(self, value):
        self.imovel = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value
