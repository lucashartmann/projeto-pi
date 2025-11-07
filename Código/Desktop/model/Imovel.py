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
        self.proprietario = Cliente.Cliente()
        self.corretor_vinculado = Corretor.Corretor()

    def gerar_codigo_com_prefixo(self, prefixo='PROD-', tamanho_sufixo=6):
        sufixo_caracteres = string.ascii_uppercase + string.digits
        sufixo = ''.join(random.choice(sufixo_caracteres)
                         for _ in range(tamanho_sufixo))
        codigo = f'{prefixo}{sufixo}'
        return codigo
