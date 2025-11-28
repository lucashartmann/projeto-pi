class Condominio:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco
        self.churrasqueira_coletiva = False
        self.piscina = False
        self.piscina_infantil = False
        self.piscina_aquecida = False
        self.quiosque = False
        self.sauna = False
        self.quadra_de_esportes = False
        self.jardim = False
        self.salao_de_festas = False
        self.academia = False
        self.sala_de_jogos = False
        self.playground = False
        self.brinquedoteca = False
        self.vaga_coberta = False
        self.estacionamento = False
        self.vaga_para_visitantes = False
        self.mercado = False
        self.mesa_de_sinuca = False
        self.mesa_de_ping_pong = False
        self.mesa_de_pebolim = False
        self.quadra_de_tenis = False
        self.quadra_de_futebol = False
        self.quadra_de_basquete = False
        self.quadra_de_volei = False
        self.quadra_de_areia = False
        self.bicicletario = False
        self.heliponto = False
        self.elevador_de_serviço = False

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome
