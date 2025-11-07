import string
import random
from enum import Enum
from model import Cliente, Corretor

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
    SALA_COMERCIAL = 1
    APARTAMENTO = 4
    LOJA = 2
    CASA = 3
    COBERTURA = 0
    LOFT = 0,
    STUDIO = 0,
    DEPOSITO = 0,
    GALPAO = 0,
    PAVILHAO = 0,
    PREDIO_COMERCIAL = 0,
    PONTO_COMERCIAL = 0,
    EMPREENDIMENTO = 0,
    CASA_EM_CONDOMINIO = 0,
    SOBRADO = 0,
    SITIO = 0,
    TERRENO = 0,
    KITNET = 0,
    CHACARA = 0,
    FAZENDA = 0,
    SOBRADO = 0


class Situacao(Enum):
    COSTRUCAO = 1
    NOVO = 4
    USADO = 2


class Ocupacao(Enum):
    DESOCUPADO = 1
    INQUILINO = 4
    PROPRIETARIO = 2


class Estado(Enum):
    BOM = 1
    OTIMO = 4
    REGULAR = 2


class Status(Enum):
    VENDIDO = 0
    VENDA = 0
    ALUGUEL = 0
    VENDA_ALUGUEL = 0
    ALUGADO = 0


class Imovel:

    def __init__(self):
        self.id = 0
        self.codigo = self.gerar_codigo_com_prefixo(prefixo='SKU-')
        self.valor_venda = 0
        self.valor_aluguel = 0
        self.quant_quartos = 0
        self.quant_salas = 0
        self.quant_vagas = 0
        self.quant_banheiros = 0
        self.quant_varandas = 0
        self.nome_condominio = ""
        self.cor = ""
        self.categoria = Categoria()
        self.descricao = ""
        self.imagens = []
        self.videos = []
        self.anexos = []
        self.endereco = ""
        self.status = Status()
        self.iptu = 0
        self.valor_condominio = 0
        self.andar = 0
        self.estado = ""
        self.numero = 0
        self.complemento = ""
        self.bloco = ""
        self.ano_construcao = ""
        self.area_total = 0
        self.area_privativa = 0
        self.bairro = ""
        self.rua = ""
        self.cidade = ""
        self.situacao = ""
        self.ocupacao = ""
        self.proprietario = Cliente.Proprietario()
        self.corretor_vinculado = Corretor.Corretor()
        
    
    def gerar_codigo_com_prefixo(self, prefixo='PROD-', tamanho_sufixo=6):
        sufixo_caracteres = string.ascii_uppercase + string.digits
        sufixo = ''.join(random.choice(sufixo_caracteres)
                         for _ in range(tamanho_sufixo))
        codigo = f'{prefixo}{sufixo}'
        return codigo


    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_codigo(self):
        return self.codigo

    def set_codigo(self, value):
        self.codigo = value

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

    def get_descricao(self):
        return self.descricao

    def set_descricao(self, value):
        self.descricao = value

    def get_imagens(self):
        return self.imagens

    def set_imagens(self, value):
        self.imagens = value

    def get_videos(self):
        return self.videos

    def set_videos(self, value):
        self.videos = value

    def get_anexos(self):
        return self.anexos

    def set_anexos(self, value):
        self.anexos = value

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

    def get_numero(self):
        return self.numero

    def set_numero(self, value):
        self.numero = value

    def get_complemento(self):
        return self.complemento

    def set_complemento(self, value):
        self.complemento = value

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

    def get_bairro(self):
        return self.bairro

    def set_bairro(self, value):
        self.bairro = value

    def get_rua(self):
        return self.rua

    def set_rua(self, value):
        self.rua = value

    def get_cidade(self):
        return self.cidade

    def set_cidade(self, value):
        self.cidade = value

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

    def get_corretor_vinculado(self):
        return self.corretor_vinculado

    def set_corretor_vinculado(self, value):
        self.corretor_vinculado = value

