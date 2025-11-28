from enum import Enum


class Status(Enum):
        EM_ANDAMENTO = "Em Costrução"
        PENDENTE = "Novo"
        # RECEM_CADASTRADO = "Usado"

class Atendimento:
    
    def __init__(self):
        self.id = 0
        self.corretor = ""
        self.cliente = ""
        self.imovel = ""
        self.status = None