from enum import Enum
from model import Endereco


bairros = [
    "Aberta dos Morros", "Agronomia", "Anchieta", "Arquipélago", "Auxiliadora", "Azenha",
    "Bela Vista", "Belém Novo", "Belém Velho", "Boa Vista", "Bom Jesus", "Bom Fim",
    "Camaquã", "Cascata", "Cavalhada", "Centro Histórico", "Chácara das Pedras", "Cidade Baixa",
    "Coronado", "Cristal", "Cristo Redentor", "Espírito Santo", "Farrapos", "Floresta",
                "Glória", "Guarujá", "Higienópolis", "Hípica", "Humaitá", "Independência", "Ipanema",
                "Jardim Botânico", "Jardim Carvalho", "Jardim do Salso", "Jardim Europa", "Jardim Floresta",
                "Jardim Isabel", "Lagoa da Conceição", "Lami", "Lomba do Pinheiro", "Menino Deus",
                "Moinhos de Vento", "Mont'Serrat", "Navegantes", "Nonoai", "Passo da Areia",
                "Passo D'Areia", "Partenon", "Petrópolis", "Ponta Grossa", "Praia de Belas",
                "Restinga", "Rio Branco", "Rubem Berta", "Santa Cecília", "Santa Maria Goretti",
                "Santa Teresa", "Santana", "Santo Antônio", "Sarandi", "São Geraldo", "São João",
                "São José", "São Sebastião", "Serraria", "Terra Nova", "Três Figueiras", "Tristeza",
                "Vila Assunção", "Vila Conceição", "Vila Ipiranga", "Vila Jardim", "Vila João Pessoa",
                "Vila Nova", "Vila São José"
]


class Categoria(Enum):
    SALA_COMERCIAL = "Sala Comercial"
    APARTAMENTO = "Apartamento"
    LOJA = "Loja"
    CASA = "Casa"
    COBERTURA = "Cobertura"
    LOFT = "Loft"
    STUDIO = "Studio"
    DEPOSITO = "Depósito"
    GALPAO = "Galpão"
    PAVILHAO = "Pavilhão"
    PREDIO_COMERCIAL = "Prédio Comercial"
    PONTO_COMERCIAL = "Ponto Comercial"
    EMPREENDIMENTO = "Empreendimento"
    CASA_EM_CONDOMINIO = "Casa em Condomínio"
    SOBRADO = "Sobrado"
    SITIO = "Sítio"
    TERRENO = "Terreno"
    KITNET = "Kitnet"
    CHACARA = "Chácara"
    FAZENDA = "Fazenda"


class Situacao(Enum):
    COSTRUCAO = "Em Costrução"
    NOVO = "Novo"
    USADO = "Usado"


class Ocupacao(Enum):
    DESOCUPADO = "Desocupado"
    INQUILINO = "Inquilino"
    PROPRIETARIO = "Proprietário"


class Estado(Enum):
    BOM = "Bom"
    OTIMO = "Ótimo"
    REGULAR = "Regular"


class Status(Enum):
    VENDA = "Venda"
    ALUGUEL = "Aluguel"
    VENDA_ALUGUEL = "Venda_Aluguel"
    ALUGADO = "Alugado"
    VENDIDO = "Vendido"
    PENDENTE = "Pendente"


class Imovel:
    codigo = 0

    def __init__(self, endereco: Endereco.Endereco, status, categoria):
        self.id = 0
        self.valor_venda = 0
        self.valor_aluguel = 0
        self.quant_quartos = 0
        self.quant_salas = 0
        self.quant_vagas = 0
        self.quant_banheiros = 0
        self.quant_varandas = 0
        self.nome_condominio = ""
        self.cor = ""
        self.categoria = categoria
        self.endereco = endereco
        self.status = status
        self.iptu = 0
        self.valor_condominio = 0
        self.andar = 0
        self.estado = None
        self.bloco = ""
        self.ano_construcao = ""
        self.area_total = 0
        self.area_privativa = 0
        self.situacao = None
        self.ocupacao = None
        self.proprietario = None
        self.corretor = None
        self.captador = None
        self.data_cadastro = None
        self.data_modificacao = None
        self.anuncio = None

        self.aceita_pet = False
        self.churrasqueira = False
        self.armarios_embutidos = False
        self.cozinha_americana = False
        self.area_de_servico = False
        self.suite_master = False
        self.banheiro_com_janela = False
        self.piscina = False
        self.lareira = False
        self.ar_condicionado = False
        self.semi_mobiliado = False
        self.mobiliado = False
        self.dependencia_de_empregada = False
        self.dispensa = False
        self.deposito = False

    def set_data_cadastro(self, data):
        self.data_cadastro = data

    def get_data_cadastro(self):
        return self.data_cadastro

    def set_data_modificacao(self, data):
        self.data_modificacao = data

    def get_data_modificacao(self):
        return self.data_modificacao

    def gerar_id(self):
        Imovel.codigo += 1
        return Imovel.codigo


    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_valor_venda(self):
        return self.valor_venda

    def set_valor_venda(self, value):
        self.valor_venda = value

    def get_valor_aluguel(self):
        return self.valor_aluguel

    def set_valor_aluguel(self, value):
        self.valor_aluguel = value

    def get_quant_quartos(self):
        return self.quant_quartos

    def set_quant_quartos(self, value):
        self.quant_quartos = value

    def get_quant_salas(self):
        return self.quant_salas

    def set_quant_salas(self, value):
        self.quant_salas = value

    def get_quant_vagas(self):
        return self.quant_vagas

    def set_quant_vagas(self, value):
        self.quant_vagas = value

    def get_quant_banheiros(self):
        return self.quant_banheiros

    def set_quant_banheiros(self, value):
        self.quant_banheiros = value

    def get_quant_varandas(self):
        return self.quant_varandas

    def set_quant_varandas(self, value):
        self.quant_varandas = value

    def get_nome_condominio(self):
        return self.nome_condominio

    def set_nome_condominio(self, value):
        self.nome_condominio = value

    def get_cor(self):
        return self.cor

    def set_cor(self, value):
        self.cor = value

    def get_categoria(self):
        return self.categoria

    def set_categoria(self, value):
        self.categoria = value


    def get_endereco(self):
        return self.endereco

    def set_endereco(self, value):
        self.endereco = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    def get_iptu(self):
        return self.iptu

    def set_iptu(self, value):
        self.iptu = value

    def get_valor_condominio(self):
        return self.valor_condominio

    def set_valor_condominio(self, value):
        self.valor_condominio = value

    def get_andar(self):
        return self.andar

    def set_andar(self, value):
        self.andar = value

    def get_estado(self):
        return self.estado

    def set_estado(self, value):
        self.estado = value

    def get_bloco(self):
        return self.bloco

    def set_bloco(self, value):
        self.bloco = value

    def get_ano_construcao(self):
        return self.ano_construcao

    def set_ano_construcao(self, value):
        self.ano_construcao = value

    def get_area_total(self):
        return self.area_total

    def set_area_total(self, value):
        self.area_total = value

    def get_area_privativa(self):
        return self.area_privativa

    def set_area_privativa(self, value):
        self.area_privativa = value

    def get_situacao(self):
        return self.situacao

    def set_situacao(self, value):
        self.situacao = value

    def get_ocupacao(self):
        return self.ocupacao

    def set_ocupacao(self, value):
        self.ocupacao = value

    def get_proprietario(self):
        return self.proprietario

    def set_proprietario(self, value):
        self.proprietario = value

    def get_corretor(self):
        return self.corretor

    def set_corretor(self, corretor):
        self.corretor = corretor

    def get_captador(self):
        return self.captador

    def set_captador(self, captador):
        self.captador = captador

    def set_endereco(self, endereco):
        self.endereco = endereco

    def get_endereco(self):
        return self.endereco
    
    def set_anuncio(self, anuncio):
        self.anuncio = anuncio

    def get_anuncio(self):
        return self.anuncio

