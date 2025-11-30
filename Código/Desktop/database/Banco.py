import sqlite3
import hashlib
import os
import io

from model import Cliente, Imovel, Administrador, Captador, Corretor, Atendimento, Endereco, Anuncio, Venda_Aluguel, Condominio
from datetime import datetime


class Banco:
    def __init__(self):
        diretorio = "data"
        if not os.path.isdir(diretorio):
            os.makedirs(diretorio)
        self.init_tabelas()

    def init_tabelas(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS endereco (
                    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
                    rua TEXT  NULL,
                    numero INTEGER NULL,
                    bairro TEXT  NULL,
                    cep INTEGER NULL,
                    complemento TEXT NULL,
                    cidade TEXT  NULL,
                    estado TEXT  NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS administrador (
                    id_administrador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NULL ,
                    senha TEXT  NULL,
                    email TEXT NULL 
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS comprador (
                    id_comprador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NULL ,
                    senha TEXT  NULL,
                    email TEXT NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT NULL,
                    endereco TEXT NULL,
                    data_nascimento TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS proprietario (
                    id_proprietario INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT NULL,
                    endereco TEXT NULL,
                    data_nascimento TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS captador (
                    id_captador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT  NULL ,
                    senha TEXT  NULL,
                    email TEXT  NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT  NULL,
                    endereco TEXT  NULL,
                    data_nascimento TEXT  NULL,
                    turno TEXT NULL,
                    salario REAL NULL,
                    matricula TEXT NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS corretor (
                    id_corretor INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT  NULL ,
                    senha TEXT  NULL,
                    email TEXT  NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT  NULL,
                    endereco TEXT  NULL,
                    data_nascimento TEXT  NULL,
                    creci TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS imovel (
                    id_imovel INTEGER PRIMARY KEY AUTOINCREMENT,
                    valor_venda REAL NULL,
                    valor_aluguel REAL NULL,
                    quant_quartos INTEGER NULL,
                    quant_salas INTEGER NULL,
                    quant_vagas INTEGER NULL,
                    quant_banheiros INTEGER NULL,
                    quant_varandas INTEGER NULL,
                    nome_condominio TEXT NULL,
                    categoria TEXT NULL,
                    id_endereco INT  NULL,
                    status TEXT NULL,
                    iptu REAL NULL,
                    valor_condominio REAL NULL,
                    andar INTEGER NULL,
                    estado TEXT NULL,
                    bloco TEXT NULL,
                    ano_construcao INTEGER NULL,
                    area_total REAL NULL,
                    area_privativa REAL NULL,
                    situacao TEXT NULL,
                    ocupacao TEXT NULL,
                    cpf_cnpj_proprietario TEXT  NULL,
                    cpf_cnpj_corretor TEXT NULL,
                    cpf_cnpj_captador TEXT NULL,
                    data_cadastro TEXT NUll,
                    data_modificacao TEXT NUll,
                    aceita_pet BOOLEAN,
                    churrasqueira BOOLEAN,
                    armarios_embutidos BOOLEAN,
                    cozinha_americana BOOLEAN,
                    area_de_servico BOOLEAN,
                    suite_master BOOLEAN,
                    banheiro_com_janela BOOLEAN,
                    piscina BOOLEAN,
                    lareira BOOLEAN,
                    ar_condicionado BOOLEAN,
                    semi_mobiliado BOOLEAN,
                    mobiliado BOOLEAN,
                    dependencia_de_empregada BOOLEAN,
                    dispensa BOOLEAN,
                    deposito BOOLEAN,
                    id_anuncio INT NULL,
                    FOREIGN KEY (id_anuncio) REFERENCES anuncio(id_anuncio),
                    FOREIGN KEY (id_endereco) REFERENCES endereco(id_endereco),
                    FOREIGN KEY (cpf_cnpj_proprietario) REFERENCES proprietario(cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_corretor) REFERENCES corretor(cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_captador) REFERENCES captador(cpf_cnpj)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS midia_imovel (
                    id_anuncio INTEGER  NULL,
                    midia BLOB  NULL,
                    tipo TEXT  NULL,
                    FOREIGN KEY (id_anuncio) references anuncio (id_anuncio)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS venda_aluguel (
                    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpf_cnpj_cliente TEXT  NULL,
                    cpf_cnpj_proprietario TEXT  NULL, 
                    cpf_cnpj_captador TEXT NULL,
                    cpf_cnpj_corretor TEXT  NULL,
                    data_venda TEXT  NULL,
                    id_imovel INTEGER  NULL,
                    comissao_captador REAL NULL,
                    comissao_corretor REAL NULL,
                    FOREIGN KEY (id_imovel) REFERENCES imovel (id_imovel),
                    FOREIGN KEY (cpf_cnpj_cliente) REFERENCES comprador (cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_proprietario) references proprietario (cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_corretor) references corretor (cpf_cnpj)
                    );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS gerente (
                    id_gerente INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT  NULL ,
                    senha TEXT  NULL,
                    email TEXT  NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT  NULL,
                    endereco TEXT  NULL,
                    data_nascimento TEXT  NULL,
                    turno TEXT NULL,
                    salario REAL NULL,
                    matricula TEXT NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS anuncio (
                    id_anuncio INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT  NULL,
                    titulo TEXT  NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS atendimento (
                    id_atendimento INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_imovel INTEGER  NULL,
                    cpf_cnpj_corretor TEXT NULL,
                    cpf_cnpj_comprador TEXT NULL,
                    status TEXT NULL,
                    FOREIGN KEY (id_imovel) REFERENCES imovel (id_imovel),
                    FOREIGN KEY (cpf_cnpj_corretor) references corretor (cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_comprador) references comprador (cpf_cnpj)
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS condominio (
                    id_condominio INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NULL,
                    id_endereco INTEGER NULL,
                    churrasqueira_coletiva BOOLEAN, 
                    piscina BOOLEAN, 
                    piscina_infantil BOOLEAN, 
                    piscina_aquecida BOOLEAN, 
                    quiosque BOOLEAN, 
                    sauna BOOLEAN, 
                    quadra_de_esportes BOOLEAN, 
                    jardim BOOLEAN, 
                    salao_de_festas BOOLEAN, 
                    academia BOOLEAN, 
                    sala_de_jogos BOOLEAN, 
                    playground BOOLEAN, 
                    brinquedoteca BOOLEAN, 
                    vaga_coberta BOOLEAN, 
                    estacionamento BOOLEAN, 
                    vaga_para_visitantes BOOLEAN, 
                    mercado BOOLEAN, 
                    mesa_de_sinuca BOOLEAN, 
                    mesa_de_ping_pong BOOLEAN, 
                    mesa_de_pebolim BOOLEAN, 
                    quadra_de_tenis BOOLEAN, 
                    quadra_de_futebol BOOLEAN, 
                    quadra_de_basquete BOOLEAN, 
                    quadra_de_volei BOOLEAN, 
                    quadra_de_areia BOOLEAN, 
                    bicicletario BOOLEAN, 
                    heliponto BOOLEAN, 
                    elevador_de_serviço BOOLEAN, 
                    FOREIGN KEY (id_endereco) REFERENCES endereco(id_endereco)

                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS condominio_imovel (
                    id_condominio INTEGER  NULL,
                    id_imovel INTEGER NULL,
                    FOREIGN KEY (id_condominio) references condominio (id_condominio),
                    FOREIGN KEY (id_imovel) references imovel (id_imovel)                
                );
                                ''')

            conexao.commit()
            
    def atualizar_comprador(self, tipo_dado, novo_valor, condicao):
        with sqlite3.connect(f"data/Biblioteca.db") as conexao:
            cursor = conexao.cursor()
            try:
                sql_update_query = f"""
                UPDATE comprador
                SET {tipo_dado} = ?
                WHERE cpf_cnpj = ?;
                """
                dados = (novo_valor, condicao)
                cursor.execute(sql_update_query, dados)
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO Banco.atualizar_comprador", e)
                return False

    def cadastrar_atendimento(self, atendimento):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:

                sql_query = f''' 
                    INSERT INTO atendimento (id_imovel, cpf_cnpj_corretor, cpf_cnpj_comprador, status) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    '''

                if atendimento.get_corretor():
                    corretor = atendimento.get_corretor().get_cpf()
                else:
                    corretor = None

                if atendimento.get_get_cliente():
                    cliente = atendimento.get_cliente().get_cpf()
                else:
                    cliente = None

                if atendimento.get_imovel():
                    imovel = atendimento.get_imovel().get_id()
                else:
                    imovel = None

                if atendimento.get_status():
                    status = atendimento.get_status().value
                else:
                    status = None

                cursor.execute(sql_query, (
                    imovel,
                    corretor,
                    cliente,
                    status
                ))

                conexao.commit()
                return True
            except Exception as e:
                erro = f"ERRO! Banco.cadastrar_atendimento: ERRO! {e}"
                print(erro)
                return False

    def get_lista_atendimentos(self):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM atendimento 
                    ''')
                registros = cursor.fetchall()

                if not registros:
                    raise Exception("Não há atendimentos cadastrados")

                lista = []

                for registro in registros:

                    id_atendimento = int(registro[0])
                    corretor = self.get_corretor_por_cpf_cnpj(registro[1])
                    comprador = self.get_comprador_por_cpf_cnpj(registro[2])
                    status = Atendimento.Status(registro[3])

                    atendimento = Atendimento.Atendimento()
                    atendimento.set_status(status)
                    atendimento.set_id(id_atendimento)
                    atendimento.set_corretor(corretor)
                    atendimento.set_cliente(comprador)

                    lista.append(atendimento)

                return lista
            except Exception as e:
                erro = "ERRO! Banco.get_lista_atendimentos: ERRO!", e
                print(erro)
                return []

    def atualizar_imovel(self, imovel: Imovel.Imovel):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()

                if imovel.get_categoria():
                    categoria = imovel.get_categoria().value
                else:
                    categoria = None
                if imovel.get_endereco():
                    if imovel.get_endereco().get_id() != None:
                        endereco = imovel.get_endereco().get_id()
                    else:
                        endereco = None
                else:
                    endereco = None
                if imovel.get_status():
                    status = imovel.get_status().value
                else:
                    status = None
                if imovel.get_estado():
                    estado = imovel.get_estado().value
                else:
                    estado = None
                if imovel.get_situacao():
                    situacao = imovel.get_situacao().value
                else:
                    situacao = None
                if imovel.get_ocupacao():
                    ocupacao = imovel.get_ocupacao().value
                else:
                    ocupacao = None
                if imovel.get_proprietario():
                    proprietario = imovel.get_proprietario().get_cpf_cnpj()
                else:
                    proprietario = None
                if imovel.get_corretor():
                    corretor = imovel.get_corretor().get_cpf_cnpj()
                else:
                    corretor = None
                if imovel.get_captador():
                    captador = imovel.get_captador().get_cpf_cnpj()
                else:
                    captador = None

                if imovel.get_data_cadastro():
                    data_cadastro = data_cadastro.strftime()
                else:
                    data_cadastro = None

                if imovel.get_data_modificacao():
                    data_modificacao = data_modificacao.strftime()
                else:
                    data_modificacao = None

                if imovel.get_anuncio():
                    anuncio = imovel.get_anuncio().get_id()
                else:
                    anuncio = None

                query = '''
                    UPDATE imovel SET
                        valor_venda = ?,
                        valor_aluguel = ?,
                        quant_quartos = ?,
                        quant_salas = ?,
                        quant_vagas = ?,
                        quant_banheiros = ?,
                        quant_varandas = ?,
                        nome_condominio = ?,
                        categoria = ?,
                        id_endereco = ?,
                        status = ?,
                        iptu = ?,
                        valor_condominio = ?,
                        andar = ?,
                        estado = ?,
                        bloco = ?,
                        ano_construcao = ?,
                        area_total = ?,
                        area_privativa = ?,
                        situacao = ?,
                        ocupacao = ?,
                        cpf_cnpj_proprietario = ?,
                        cpf_cnpj_corretor = ?,
                        cpf_cnpj_captador = ?,
                        data_cadastro = ?,
                        data_modificacao = ?,
                        aceita_pet = ?,
                        churrasqueira = ?,
                        armarios_embutidos = ?,
                        cozinha_americana = ?,
                        area_de_servico = ?,
                        suite_master = ?,
                        banheiro_com_janela = ?,
                        piscina = ?,
                        lareira = ?,
                        ar_condicionado = ?,
                        semi_mobiliado = ?,
                        mobiliado = ?,
                        dependencia_de_empregada = ?,
                        dispensa = ?,
                        deposito = ?,
                        id_anuncio = ?
                    WHERE id_imovel = ?
                '''

                valores = (
                    imovel.get_valor_venda(),
                    imovel.get_valor_aluguel(),
                    imovel.get_quant_quartos(),
                    imovel.get_quant_salas(),
                    imovel.get_quant_vagas(),
                    imovel.get_quant_banheiros(),
                    imovel.get_quant_varandas(),
                    imovel.get_nome_condominio(),
                    categoria,
                    endereco,
                    status,
                    imovel.get_iptu(),
                    imovel.get_valor_condominio(),
                    imovel.get_andar(),
                    estado,
                    imovel.get_bloco(),
                    imovel.get_ano_construcao(),
                    imovel.get_area_total(),
                    imovel.get_area_privativa(),
                    situacao,
                    ocupacao,
                    proprietario,
                    corretor,
                    captador,
                    data_cadastro,
                    data_modificacao,
                    imovel.aceita_pet,
                    imovel.churrasqueira,
                    imovel.armarios_embutidos,
                    imovel.cozinha_americana,
                    imovel.area_de_servico,
                    imovel.suite_master,
                    imovel.banheiro_com_janela,
                    imovel.piscina,
                    imovel.lareira,
                    imovel.ar_condicionado,
                    imovel.semi_mobiliado,
                    imovel.mobiliado,
                    imovel.dependencia_de_empregada,
                    imovel.dispensa,
                    imovel.deposito,
                    anuncio,
                    imovel.get_id(),
                )

                cursor.execute(query, valores)
                self.conn.commit()
                return True
            except Exception as e:
                erro = f"ERRO! Banco.atualizar_imovel: {e}"
                print(erro)
                return False

    def get_anuncio(self, id_anuncio):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                cursor.execute(f'''
                        SELECT * FROM anuncio
                        WHERE id_anuncio = ?
                    ''', (id_anuncio,))
                registro = cursor.fetchone()

                if not registro:
                    raise Exception(f"Não existe anúncio com id {id_anuncio}")

                anuncio = Anuncio.Anuncio()
                id_anuncio = registro[0]
                descricao = registro[1]
                titulo = registro[2]
                anuncio.set_id(id_anuncio)
                anuncio.set_descricao(descricao)
                anuncio.set_titulo(titulo)

                mapa_anexos = self.get_lista_anexos(id_anuncio)
                if mapa_anexos["Imagens"] and isinstance(mapa_anexos["Imagens"], list):
                    anuncio.set_imagens(mapa_anexos["Imagens"])
                if mapa_anexos["Videos"] and isinstance(mapa_anexos["Videos"], list):
                    anuncio.set_videos(mapa_anexos["Videos"] and isinstance(
                        mapa_anexos["Imagens"], list))
                if mapa_anexos["Documentos"] and isinstance(mapa_anexos["Documentos"], list):
                    anuncio.set_anexos(mapa_anexos["Documentos"])

                return anuncio
            except Exception as e:
                print(e)
                erro = f"ERRO! Banco.get_anuncio(): {e}"
                return None

    def cadastrar_anexo(self, id_anuncio, blob, tipo):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:

                sql_query = f''' 
                    INSERT INTO midia_imovel (id_anuncio, midia, tipo) 
                    VALUES(?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    id_anuncio, blob, tipo
                ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"ERRO! Banco.cadastrar_anexo: ERRO! {e}"
                print(erro)
                return False

    def get_lista_anexos(self, id_anuncio):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM midia_imovel 
                        WHERE id_imovel = ?
                    ''', (id_anuncio,))
                registros = cursor.fetchall()

                imagens = []
                videos = []
                documentos = []

                if not registros:
                    raise Exception("Não há midias_imóveis cadastrados")

                for registro in registros:
                    id = registro[0]
                    blob = io.BytesIO(registro[1])
                    tipo = registro[2]

                    if tipo == "Imagem":
                        imagens.append(blob)
                    elif tipo == "Documento":
                        documentos.append(blob)
                    elif tipo == "Video":
                        documentos.append(blob)

                mapa = dict()
                mapa["Imagens"] = imagens
                mapa["Videos"] = videos
                mapa["Documentos"] = documentos

                return mapa
            except Exception as e:
                erro = "ERRO! Banco.get_lista_anexos: ERRO!", e
                print(erro)
                return []

    def get_comprador_por_cpf_cnpj(self, cpf_cnpj):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM comprador 
                        WHERE cpf_cnpj = ?
                    ''', (cpf_cnpj,))
                registro = cursor.fetchone()

                if not registro:
                    raise Exception(
                        f"Não existe comprador com cpf/cnpj: {cpf_cnpj}")

                id_comprador = int(registro[0])
                username = registro[1]
                senha = registro[2]
                email = registro[3]
                nome = registro[4]
                cpf_cnpj = registro[5]
                rg = registro[6]
                telefone = registro[7]
                endereco = self.get_endereco_por_id(registro[8])
                if registro[9]:
                    data_nascimento = datetime.strptime(registro[9])

                comprador = Cliente.Comprador()
                comprador.set_nome(nome)
                comprador.set_id(id_comprador)
                comprador.set_username(username)
                comprador.set_senha(senha)
                comprador.set_email(email)
                comprador.set_cpf_cnpj(cpf_cnpj)
                comprador.set_rg(rg)
                comprador.set_telefone(telefone)
                comprador.set_endereco(endereco)
                comprador.set_data_nascimento(data_nascimento)

                return comprador
            except Exception as e:
                erro = "Banco.get_comprador_por_cpf_cnpj: ERRO!", e
                print(erro)
                return None

    def get_lista_compradores(self):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM comprador 
                    ''')
                registros = cursor.fetchall()

                if not registros:
                    raise Exception("Não há compradores cadastrados")

                lista = []

                for registro in registros:
                    id_comprador = int(registro[0])
                    username = registro[1]
                    senha = registro[2]
                    email = registro[3]
                    nome = registro[4]
                    cpf_cnpj = registro[5]
                    rg = registro[6]
                    telefone = registro[7]
                    endereco = self.get_endereco_por_id(registro[8])
                    if registro[9]:
                        data_nascimento = datetime.strptime(registro[9])

                    comprador = Cliente.Comprador()
                    comprador.set_nome(nome)
                    comprador.set_id(id_comprador)
                    comprador.set_username(username)
                    comprador.set_senha(senha)
                    comprador.set_email(email)
                    comprador.set_cpf_cnpj(cpf_cnpj)
                    comprador.set_rg(rg)
                    comprador.set_telefone(telefone)
                    comprador.set_endereco(endereco)
                    comprador.set_data_nascimento(data_nascimento)

                    lista.append(comprador)

                return lista

            except Exception as e:
                erro = "Banco.get_lista_compradores: ERRO!", e
                print(erro)
                return []

    def get_lista_proprietarios(self):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM proprietario 
                    ''')
                registros = cursor.fetchall()

                if not registros:
                    raise Exception("Não há proprietarios cadastrados")

                lista = []

                for registro in registros:

                    id_proprietario = int(registro[0])
                    email = registro[1]
                    nome = registro[2]
                    cpf_cnpj = registro[3]
                    rg = registro[4]
                    telefone = registro[5]
                    if registro[6]:
                        data_nascimento = datetime.strptime(registro[6])

                    proprietario = Cliente.Proprietario()
                    proprietario.set_nome(nome)
                    proprietario.set_id(id_proprietario)
                    proprietario.set_email(email)
                    proprietario.set_cpf_cnpj(cpf_cnpj)
                    proprietario.set_rg(rg)
                    proprietario.set_telefone(telefone)
                    proprietario.set_data_nascimento(data_nascimento)

                    lista.append(proprietario)

                return lista
            except Exception as e:
                erro = "Banco.get_lista_proprietarios: ERRO!", e
                print(erro)
                return []

    def verificar_endereco(self, endereco):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                sql = '''
                    SELECT * FROM endereco WHERE rua = ? numero = ? bairro = ? cep = ? complemento = ? cidade = ? estado = ?
                '''
                registro = cursor.fetchone(sql, (endereco.get_rua(), endereco.get_numero(), endereco.get_bairro(
                ), endereco.get_cep(), endereco.get_complemento(), endereco.get_cidade(), endereco.get_estado()))

                if registro:
                    id_endereco = registro[0]
                    rua = registro[1]
                    numero = registro[2]
                    bairro = registro[3]
                    cep = registro[4]
                    complemento = registro[5]
                    cidade = registro[6]
                    estado = registro[7]
                    endereco = Endereco.Endereco(
                        rua, numero, bairro, cep, complemento, cidade)
                    endereco.set_estado(estado)
                    endereco.set_id(id_endereco)
                    return endereco
                else:
                    return None

            except Exception as e:
                print(e)
                return None

    def verificar_usuario(self, username, senha, tabela):
        if tabela == "Cliente":
            tabela == "comprador"

        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                if "@" in username:
                    cursor.execute(f'''
                        SELECT * FROM {tabela} WHERE email = ?
                    ''', (username,))
                    registro = cursor.fetchone()
                else:
                    cursor.execute(f'''
                        SELECT * FROM {tabela} WHERE username = ?
                    ''', (username,))
                    registro = cursor.fetchone()
                if not registro:
                    raise Exception("Usuário não encontrado")

                senha_hash_banco = registro[3]

                senha_hash = hashlib.sha256(
                    senha.get_senha().encode('utf-8')).hexdigest()

                if senha_hash_banco == senha_hash:
                    pessoa = ""
                    match tabela:
                        case "comprador":
                            pessoa = Cliente.Comprador(*registro[1:])
                        case "corretor":
                            pessoa = Corretor.Corretor(*registro[1:]), ""
                        case "captador":
                            pessoa = Captador.Captador(*registro[1:]), ""
                        case "administrador":
                            pessoa = Administrador.Administrador(
                                *registro[1:]), ""

                    pessoa.set_id(registro[0])
                    return pessoa
                else:
                    raise Exception("Senha errada!")

            except Exception as e:
                erro = "Banco.verificar_usuario: ERRO!", e
                print(erro)
                return None

    def cadastrar_endereco(self, endereco):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:

                sql_query = f''' 
                    INSERT INTO endereco (rua, numero, bairro, cep, complemento, cidade, estado) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    endereco.get_rua(),
                    endereco.get_numero(),
                    endereco.get_bairro(),
                    endereco.get_cep(),
                    endereco.get_complemento(),
                    endereco.get_cidade(),
                    endereco.get_estado(),
                ))
                conexao.commit()
                endereco_id = cursor.lastrowid
                return endereco_id
            except Exception as e:
                erro = f"Banco.cadastrar_endereco: ERRO! {e}"
                print(erro)
                return False

    def cadastrar_corretor(self, corretor):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                if corretor.get_endereco():
                    if corretor.get_endereco().get_id() != None:
                        endereco = corretor.get_endereco().get_id()
                    else:
                        endereco = None
                else:
                    endereco = None

                if corretor.get_data_nascimento():
                    data = corretor.get_data_nascimento().strftime()
                else:
                    data = None

                senha_hash = hashlib.sha256(
                    corretor.get_senha().encode('utf-8')).hexdigest()
                sql_query = f''' 
                    INSERT INTO corretor (username, senha, email, nome, cpf_cnpj, rg, telefone, endereco, data_nascimento, creci TEXT NULL) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    corretor.get_username(),
                    senha_hash,
                    corretor.get_email(),
                    corretor.get_nome(),
                    corretor.get_cpf_cnpj(),
                    corretor.get_rg(),
                    corretor.get_telefone(),
                    endereco,
                    data,
                    corretor.get_creci()
                ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"Banco.cadastrar_corretor: ERRO! {e}"
                print(erro)
                return False

    def cadastrar_captador(self, captador):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                if captador.get_endereco():
                    if captador.get_endereco().get_id() != None:
                        endereco = captador.get_endereco().get_id()
                    else:
                        endereco = None
                else:
                    endereco = None

                if captador.get_data_nascimento():
                    data = captador.get_data_nascimento().strftime()
                else:
                    data = None

                senha_hash = hashlib.sha256(
                    captador.get_senha().encode('utf-8')).hexdigest()
                sql_query = f''' 
                    INSERT INTO captador (username, senha, email, nome, cpf_cnpj, rg, telefone, endereco, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    captador.get_username(),
                    senha_hash,
                    captador.get_email(),
                    captador.get_nome(),
                    captador.get_cpf_cnpj(),
                    captador.get_rg(),
                    captador.get_telefone(),
                    endereco,
                    data
                ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"Banco.cadastrar_captador: ERRO! {e}"
                print(erro)
                return False

    def cadastrar_proprietario(self, proprietario):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                if proprietario.get_endereco():
                    if proprietario.get_endereco().get_id() != None:
                        endereco = proprietario.get_endereco().get_id()
                    else:
                        endereco = None
                else:
                    endereco = None

                if proprietario.get_data_nascimento():
                    data = proprietario.get_data_nascimento().strftime()
                else:
                    data = None

                if isinstance(proprietario, Cliente.proprietario):

                    sql_query = f''' 
                    INSERT INTO proprietario (email, nome, cpf_cnpj, rg, telefone, endereco, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    '''
                    cursor.execute(sql_query, (
                        proprietario.get_email(),
                        proprietario.get_nome(),
                        proprietario.get_cpf_cnpj(),
                        proprietario.get_rg(),
                        proprietario.get_telefone(),
                        endereco,
                        data
                    ))
                    conexao.commit()
                    return True
            except Exception as e:
                erro = f"Banco.cadastrar_proprietario: ERRO! {e}"
                print(erro)
                return False

    def cadastrar_endereco(self, endereco):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:

                sql_query = f''' 
                    INSERT INTO endereco (rua, numero, bairro, cep, complemento, cidade, estado) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    endereco.get_rua(),
                    endereco.get_numero(),
                    endereco.get_bairro(),
                    endereco.get_cep(),
                    endereco.get_complemento(),
                    endereco.get_cidade(),
                    endereco.get_estado(),
                ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"Banco.cadastrar_endereco: ERRO! {e}"
                print(erro)
                return False

    def cadastrar_comprador(self, comprador):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                if comprador.get_endereco():
                    if comprador.get_endereco().get_id() != None:
                        endereco = comprador.get_endereco().get_id()
                    else:
                        endereco = None
                else:
                    endereco = None

                if comprador.get_data_nascimento():
                    data = comprador.get_data_nascimento().strftime()
                else:
                    data = None

                if isinstance(comprador, Cliente.Comprador):
                    senha_hash = hashlib.sha256(
                        comprador.get_senha().encode('utf-8')).hexdigest()
                    sql_query = f''' 
                    INSERT INTO comprador (username, senha, email, nome, cpf_cnpj, rg, telefone, endereco, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    cursor.execute(sql_query, (
                        comprador.get_username(),
                        senha_hash,
                        comprador.get_email(),
                        comprador.get_nome(),
                        comprador.get_cpf_cnpj(),
                        comprador.get_rg(),
                        comprador.get_telefone(),
                        endereco,
                        data
                    ))

                    conexao.commit()
                    return True
            except Exception as e:
                erro = f"Banco.cadastrar_comprador: ERRO! {e}"
                print(erro)
                return False

    def remover_imovel(self, codigo):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_delete_query = """
                    DELETE FROM imovel
                    WHERE codigo = ?
                    """
                cursor.execute(sql_delete_query, (codigo,))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"Banco.remover_imovel: ERRO! {e}"
                print(erro)
                return False

    def get_endereco_por_id(self, id):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM endereco 
                        WHERE id_endereco = ?
                    ''', (id,))
                registros = cursor.fetchone()

                if not registros:
                    raise Exception(
                        f"Não há endereços cadastrados com id {id}")

                id_endereco = int(registros[0])
                rua = registros[1]
                numero = int(registros[2])
                bairro = registros[3]
                cep = registros[4]
                complemento = registros[5]
                cidade = registros[6]
                estado = registros[7]

                endereco = Endereco.Endereco(
                    rua, numero, bairro, cep, complemento, cidade)
                endereco.set_estado(estado)
                endereco.set_id(id_endereco)

                return endereco
            except Exception as e:
                erro = "Banco.get_endereco_por_id: ERRO!", e
                print(erro)
                return None

    def get_corretor_por_cpf_cnpj(self, cpf_cnpj):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM corretor 
                        WHERE cpf_cnpj = ?
                    ''', (cpf_cnpj,))
                registro = cursor.fetchone()

                if not registro:
                    raise Exception(
                        f"Não existe corretor com CPF/CNPJ {cpf_cnpj}")

                id_corretor = int(registro[0])
                username = registro[1]
                senha = registro[2]
                email = registro[3]
                nome = registro[4]
                cpf_cnpj = registro[5]
                rg = registro[6]
                telefone = registro[7]
                endereco = self.get_endereco_por_id(registro[8])
                if registro[9]:
                    data_nascimento = datetime.strptime(registro[9])
                creci = registro[10]

                corretor = Corretor.Corretor()
                corretor.set_nome(nome)
                corretor.set_id(id_corretor)
                corretor.set_username(username)
                corretor.set_senha(senha)
                corretor.set_email(email)
                corretor.set_cpf_cnpj(cpf_cnpj)
                corretor.set_rg(rg)
                corretor.set_telefone(telefone)
                corretor.set_endereco(endereco)
                corretor.set_data_nascimento(data_nascimento)
                corretor.set_creci(creci)

                return corretor

            except Exception as e:
                erro = "Banco.get_corretor_por_cpf_cnpj: ERRO!", e
                print(erro)
                return None

    def get_captador_por_cpf_cnpj(self, cpf_cnpj):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM captador 
                        WHERE cpf_cnpj = ?
                    ''', (cpf_cnpj,))
                registro = cursor.fetchone()

                if not registro:
                    raise Exception(
                        f"Não existe captador com CPF/CNPJ {cpf_cnpj}")

                id_captador = int(registro[0])
                username = registro[1]
                senha = registro[2]
                email = registro[3]
                nome = registro[4]
                cpf_cnpj = registro[5]
                rg = registro[6]
                telefone = registro[7]
                endereco = self.get_endereco_por_id(registro[8])
                if registro[9]:
                    data_nascimento = datetime.strptime(registro[9])
                turno = registro[10]
                if registro[11]:
                    salario = float(registro[11])
                matricula = registro[12]

                captador = Captador.Captador()
                captador.set_nome(nome)
                captador.set_id(id_captador)
                captador.set_username(username)
                captador.set_senha(senha)
                captador.set_email(email)
                captador.set_cpf_cnpj(cpf_cnpj)
                captador.set_rg(rg)
                captador.set_telefone(telefone)
                captador.set_endereco(endereco)
                captador.set_data_nascimento(data_nascimento)
                captador.set_turno(turno)
                captador.set_matricula(matricula)
                captador.set_salario(salario)

                return captador
            except Exception as e:
                erro = "ERRO! Banco.get_captador_por_cpf_cnpj: ERRO!", e
                print(erro)
                return None

    def get_proprietario_por_cpf_cnpj(self, cpf_cnpj):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM proprietario 
                        WHERE cpf_cnpj = ?
                    ''', (cpf_cnpj,))
                registro = cursor.fetchone()

                if not registro:
                    raise Exception(
                        f"Não existe proprietario com CPF/CNPJ: {cpf_cnpj}")

                id_proprietario = int(registro[0])
                email = registro[1]
                nome = registro[2]
                cpf_cnpj = registro[3]
                rg = registro[4]
                telefone = registro[5]
                if registro[6]:
                    data_nascimento = datetime.strptime(registro[6])

                proprietario = Cliente.Proprietario()
                proprietario.set_nome(nome)
                proprietario.set_id(id_proprietario)
                proprietario.set_email(email)
                proprietario.set_cpf_cnpj(cpf_cnpj)
                proprietario.set_rg(rg)
                proprietario.set_telefone(telefone)
                proprietario.set_data_nascimento(data_nascimento)

                return proprietario
            except Exception as e:
                erro = "ERRO! Banco.get_proprietario_por_cpf_cnpj: ERRO!", e
                print(erro)
                return None

    def get_imovel_por_codigo(self, codigo):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    f'SELECT * FROM imovel WHERE codigo = ?', (codigo,))
                dados = cursor.fetchone()
                if not dados:
                    raise Exception(f"Não existe imóvel com codigo {codigo}")
                if dados[42]:
                    anuncio = self.get_anuncio(dados[42])
                    if anuncio:
                        imovel.set_anuncio(anuncio)
                    else:
                        imovel.set_anuncio(None)
                if dados[13]:
                    status = imovel.Status(dados[12])
                else:
                    status = None
                if dados[9]:
                    categoria = imovel.Categoria(dados[9])
                else:
                    categoria = None
                if dados[10]:
                    endereco = self.get_endereco_por_id(int(dados[10]))
                    if not endereco:
                        raise Exception("Erro com endereço")
                else:
                    raise Exception("ERRO: Imóvel não possui endereço")
                imovel = Imovel.Imovel(endereco, status, categoria)
                if not isinstance(dados[0], str):
                    imovel.set_id(int(dados[0]))
                if not isinstance(dados[1], str):
                    imovel.set_valor_venda(float(dados[1]))
                if not isinstance(dados[2], str):
                    imovel.set_valor_aluguel(float(dados[2]))
                if not isinstance(dados[3], str):
                    imovel.set_quant_quartos(int(dados[3]))
                if not isinstance(dados[4], str):
                    imovel.set_quant_salas(int(dados[4]))
                if not isinstance(dados[5], str):
                    imovel.set_quant_vagas(int(dados[5]))
                if not isinstance(dados[6], str):
                    imovel.set_quant_banheiros(int(dados[6]))
                if not isinstance(dados[7], str):
                    imovel.set_quant_varandas(int(dados[7]))
                imovel.set_nome_condominio(dados[8])
                if not isinstance(dados[12], str):
                    imovel.set_iptu(float(dados[12]))
                if not isinstance(dados[13], str):
                    imovel.set_valor_condominio(float(dados[13]))
                if not isinstance(dados[14], str):
                    imovel.set_andar(int(dados[14]))
                if dados[15]:
                    imovel.set_estado(imovel.Estado(dados[15]))
                else:
                    imovel.set_estado(None)
                imovel.set_bloco(dados[16])
                if not isinstance(dados[17], str):
                    imovel.set_ano_construcao(int(dados[17]))
                if not isinstance(dados[18], str):
                    imovel.set_area_total(float(dados[18]))
                if not isinstance(dados[19], str):
                    imovel.set_area_privativa(float(dados[19]))
                if dados[20]:
                    imovel.set_situacao(imovel.Situacao(dados[20]))
                else:
                    imovel.set_situacao(None)
                if dados[21]:
                    imovel.set_ocupacao(imovel.Ocupacao(dados[21]))
                else:
                    imovel.set_ocupacao(None)
                if dados[22]:
                    proprietario = self.get_proprietario_por_cpf_cnpj(
                        dados[22])
                    if proprietario:
                        imovel.set_proprietario(proprietario)
                    else:
                        imovel.set_proprietario(None)
                else:
                    imovel.set_proprietario(None)
                if dados[23]:
                    corretor = self.get_corretor_por_cpf_cnpj(dados[23])
                    if corretor:
                        imovel.set_corretor(corretor)
                    else:
                        imovel.set_corretor(None)
                else:
                    imovel.set_corretor(None)
                if dados[24]:
                    captador = self.get_captador_por_cpf_cnpj(dados[24])
                    if captador:
                        imovel.set_captador(captador)
                    else:
                        imovel.set_captador(None)
                else:
                    imovel.set_captador(None)
                if dados[25]:
                    imovel.set_data_cadastro(datetime.strptime(dados[25]))
                else:
                    imovel.set_data_cadastro(None)
                if dados[26]:
                    imovel.set_data_modificacao(
                        datetime.strptime(dados[26]))
                else:
                    imovel.set_data_modificacao(None)
                imovel.aceita_pet = dados[27]
                imovel.churrasqueira = dados[28]
                imovel.armarios_embutidos = dados[20]
                imovel.cozinha_americana = dados[30]
                imovel.area_de_servico = dados[31]
                imovel.suite_master = dados[32]
                imovel.banheiro_com_janela = dados[33]
                imovel.piscina = dados[34]
                imovel.lareira = dados[35]
                imovel.ar_condicionado = dados[36]
                imovel.semi_mobiliado = dados[37]
                imovel.mobiliado = dados[38]
                imovel.dependencia_de_empregada = dados[39]
                imovel.dispensa = dados[40]
                imovel.deposito = dados[41]
                return imovel
            except Exception as e:
                erro = f"ERRO! Banco.get_imovel_por_codigo: ERRO! {e}"
                print(erro)
                return None

    def cadastrar_imovel(self, imovel):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO imovel(valor_venda, valor_aluguel, quant_quartos, quant_salas, quant_vagas, quant_banheiros, quant_varandas, nome_condominio, categoria, id_endereco, status, iptu, valor_condominio, andar, estado, bloco, ano_construcao, area_total, area_privativa, situacao, ocupacao, cpf_cnpj_proprietario, cpf_cnpj_corretor, cpf_cnpj_captador, data_cadastro, data_modificacao,aceita_pet,churrasqueira, armarios_embutidos,cozinha_americana, area_de_servico, suite_master, banheiro_com_janela, piscina, lareira, ar_condicionado, semi_mobiliado, mobiliado, dependencia_de_empregada, dispensa, deposito, id_anuncio) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    '''

                if imovel.get_categoria():
                    categoria = imovel.get_categoria().value
                else:
                    categoria = None
                if imovel.get_endereco():
                    if imovel.get_endereco().get_id() != None:
                        endereco = imovel.get_endereco().get_id()
                    else:
                        endereco = None
                else:
                    endereco = None

                if imovel.get_anuncio():
                    if imovel.get_anuncio().get_id() != None:
                        anuncio = imovel.get_anuncio().get_id()
                    else:
                        anuncio = None
                else:
                    anuncio = None

                if imovel.get_status():
                    status = imovel.get_status().value
                else:
                    status = None
                if imovel.get_estado():
                    estado = imovel.get_estado().value
                else:
                    estado = None
                if imovel.get_situacao():
                    situacao = imovel.get_situacao().value
                else:
                    situacao = None
                if imovel.get_ocupacao():
                    ocupacao = imovel.get_ocupacao().value
                else:
                    ocupacao = None
                if imovel.get_proprietario():
                    proprietario = imovel.get_proprietario().get_cpf_cnpj()
                else:
                    proprietario = None
                if imovel.get_corretor():
                    corretor = imovel.get_corretor().get_cpf_cnpj()
                else:
                    corretor = None
                if imovel.get_captador():
                    captador = imovel.get_captador().get_cpf_cnpj()
                else:
                    captador = None

                if imovel.get_data_cadastro():
                    data_cadastro = data_cadastro.strftime()
                else:
                    data_cadastro = None

                if imovel.get_data_modificacao():
                    data_modificacao = data_modificacao.strftime()
                else:
                    data_modificacao = None

                cursor.execute(sql_query, (
                    imovel.get_valor_venda(),
                    imovel.get_valor_aluguel(),
                    imovel.get_quant_quartos(),
                    imovel.get_quant_salas(),
                    imovel.get_quant_vagas(),
                    imovel.get_quant_banheiros(),
                    imovel.get_quant_varandas(),
                    imovel.get_nome_condominio(),
                    categoria,
                    endereco,
                    status,
                    imovel.get_iptu(),
                    imovel.get_valor_condominio(),
                    imovel.get_andar(),
                    estado,
                    imovel.get_bloco(),
                    imovel.get_ano_construcao(),
                    imovel.get_area_total(),
                    imovel.get_area_privativa(),
                    situacao,
                    ocupacao,
                    proprietario,
                    corretor,
                    captador,
                    data_cadastro,
                    data_modificacao,
                    imovel.data_cadastro,
                    imovel.data_modificacao,
                    imovel.aceita_pet,
                    imovel.churrasqueira,
                    imovel.armarios_embutidos,
                    imovel.cozinha_americana,
                    imovel.area_de_servico,
                    imovel.suite_master,
                    imovel.banheiro_com_janela,
                    imovel.piscina,
                    imovel.lareira,
                    imovel.ar_condicionado,
                    imovel.semi_mobiliado,
                    imovel.mobiliado,
                    imovel.dependencia_de_empregada,
                    imovel.dispensa,
                    imovel.deposito,
                    anuncio,
                    imovel.get_id(),
                ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"ERRO! Banco.cadastrar_imovel: ERRO! {e}"
                print(erro)
                return False

    def get_lista_imoveis(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:

                cursor = conexao.cursor()
                lista = []
                cursor.execute("SELECT * FROM imovel")
                resultados = cursor.fetchall()
                if not resultados:
                    raise Exception(f"Não há imóveis cadastrados")
                for dados in resultados:
                    if dados[42]:
                        anuncio = self.get_anuncio(dados[42])
                        if anuncio:
                            imovel.set_anuncio(anuncio)
                        else:
                            imovel.set_anuncio(None)
                    if dados[13]:
                        status = imovel.Status(dados[12])
                    else:
                        status = None
                    if dados[9]:
                        categoria = imovel.Categoria(dados[9])
                    else:
                        categoria = None
                    if dados[10]:
                        endereco = self.get_endereco_por_id(int(dados[10]))
                        if not endereco:
                            raise Exception("Erro com endereço")
                    else:
                        raise Exception("ERRO: Imóvel não possui endereço")
                    imovel = Imovel.Imovel(endereco, status, categoria)

                    if not isinstance(dados[0], str):
                        imovel.set_id(int(dados[0]))
                    if not isinstance(dados[1], str):
                        imovel.set_valor_venda(float(dados[1]))
                    if not isinstance(dados[2], str):
                        imovel.set_valor_aluguel(float(dados[2]))
                    if not isinstance(dados[3], str):
                        imovel.set_quant_quartos(int(dados[3]))
                    if not isinstance(dados[4], str):
                        imovel.set_quant_salas(int(dados[4]))
                    if not isinstance(dados[5], str):
                        imovel.set_quant_vagas(int(dados[5]))
                    if not isinstance(dados[6], str):
                        imovel.set_quant_banheiros(int(dados[6]))
                    if not isinstance(dados[7], str):
                        imovel.set_quant_varandas(int(dados[7]))
                    imovel.set_nome_condominio(dados[8])

                    if not isinstance(dados[12], str):
                        imovel.set_iptu(float(dados[12]))
                    if not isinstance(dados[13], str):
                        imovel.set_valor_condominio(float(dados[13]))
                    if not isinstance(dados[14], str):
                        imovel.set_andar(int(dados[14]))
                    if dados[15]:
                        imovel.set_estado(imovel.Estado(dados[15]))
                    else:
                        imovel.set_estado(None)
                    imovel.set_bloco(dados[16])
                    if not isinstance(dados[17], str):
                        imovel.set_ano_construcao(int(dados[17]))

                    if not isinstance(dados[18], str):
                        imovel.set_area_total(float(dados[18]))

                    if not isinstance(dados[19], str):
                        imovel.set_area_privativa(float(dados[19]))

                    if dados[20]:
                        imovel.set_situacao(imovel.Situacao(dados[20]))
                    else:
                        imovel.set_situacao(None)
                    if dados[21]:
                        imovel.set_ocupacao(imovel.Ocupacao(dados[21]))
                    else:
                        imovel.set_ocupacao(None)
                    if dados[22]:
                        proprietario = self.get_proprietario_por_cpf_cnpj(
                            dados[22])
                        if proprietario:
                            imovel.set_proprietario(proprietario)
                        else:
                            imovel.set_proprietario(None)
                    else:
                        imovel.set_proprietario(None)
                    if dados[23]:
                        corretor = self.get_corretor_por_cpf_cnpj(dados[23])
                        if corretor:
                            imovel.set_corretor(corretor)
                        else:
                            imovel.set_corretor(None)
                    else:
                        imovel.set_corretor(None)
                    if dados[24]:
                        captador = self.get_captador_por_cpf_cnpj(dados[24])
                        if captador:
                            imovel.set_captador(captador)
                        else:
                            imovel.set_captador(None)
                    else:
                        imovel.set_captador(None)
                    if dados[25]:
                        imovel.set_data_cadastro(datetime.strptime(dados[25]))
                    else:
                        imovel.set_data_cadastro(None)
                    if dados[26]:
                        imovel.set_data_modificacao(
                            datetime.strptime(dados[26]))
                    else:
                        imovel.set_data_modificacao(None)
                    imovel.aceita_pet = dados[27]
                    imovel.churrasqueira = dados[28]
                    imovel.armarios_embutidos = dados[20]
                    imovel.cozinha_americana = dados[30]
                    imovel.area_de_servico = dados[31]
                    imovel.suite_master = dados[32]
                    imovel.banheiro_com_janela = dados[33]
                    imovel.piscina = dados[34]
                    imovel.lareira = dados[35]
                    imovel.ar_condicionado = dados[36]
                    imovel.semi_mobiliado = dados[37]
                    imovel.mobiliado = dados[38]
                    imovel.dependencia_de_empregada = dados[39]
                    imovel.dispensa = dados[40]
                    imovel.deposito = dados[41]
                return lista
            except Exception as e:
                erro = f"ERRO! Banco.get_lista_imoveis: ERRO! {e}"
                print(erro)
                return []

    def get_lista_imoveis_disponiveis(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                lista = []
                cursor.execute(
                    "SELECT * FROM imovel WHERE status IN ('Venda', 'Aluguel', 'venda_aluguel')")
                resultados = cursor.fetchall()
                if not resultados:
                    raise Exception(f"Não há imóveis disponiveis")

                for dados in resultados:
                    if dados[42]:
                        anuncio = self.get_anuncio(dados[42])
                        if anuncio:
                            imovel.set_anuncio(anuncio)
                        else:
                            imovel.set_anuncio(None)
                    if dados[13]:
                        status = imovel.Status(dados[12])
                    else:
                        status = None
                    if dados[9]:
                        categoria = imovel.Categoria(dados[9])
                    else:
                        categoria = None
                    if dados[10]:
                        endereco = self.get_endereco_por_id(int(dados[10]))
                        if not endereco:
                            raise Exception("Erro com endereço")
                    else:
                        raise Exception("Imóvel não possui endereço")
                    imovel = Imovel.Imovel(endereco, status, categoria)

                    if not isinstance(dados[0], str):
                        imovel.set_id(int(dados[0]))
                    if not isinstance(dados[1], str):
                        imovel.set_valor_venda(float(dados[1]))
                    if not isinstance(dados[2], str):
                        imovel.set_valor_aluguel(float(dados[2]))
                    if not isinstance(dados[3], str):
                        imovel.set_quant_quartos(int(dados[3]))
                    if not isinstance(dados[4], str):
                        imovel.set_quant_salas(int(dados[4]))
                    if not isinstance(dados[5], str):
                        imovel.set_quant_vagas(int(dados[5]))
                    if not isinstance(dados[6], str):
                        imovel.set_quant_banheiros(int(dados[6]))
                    if not isinstance(dados[7], str):
                        imovel.set_quant_varandas(int(dados[7]))
                    imovel.set_nome_condominio(dados[8])

                    if not isinstance(dados[12], str):
                        imovel.set_iptu(float(dados[12]))
                    if not isinstance(dados[13], str):
                        imovel.set_valor_condominio(float(dados[13]))
                    if not isinstance(dados[14], str):
                        imovel.set_andar(int(dados[14]))
                    if dados[15]:
                        imovel.set_estado(imovel.Estado(dados[15]))
                    else:
                        imovel.set_estado(None)
                    imovel.set_bloco(dados[16])
                    if not isinstance(dados[17], str):
                        imovel.set_ano_construcao(int(dados[17]))

                    if not isinstance(dados[18], str):
                        imovel.set_area_total(float(dados[18]))

                    if not isinstance(dados[19], str):
                        imovel.set_area_privativa(float(dados[19]))

                    if dados[20]:
                        imovel.set_situacao(imovel.Situacao(dados[20]))
                    else:
                        imovel.set_situacao(None)
                    if dados[21]:
                        imovel.set_ocupacao(imovel.Ocupacao(dados[21]))
                    else:
                        imovel.set_ocupacao(None)
                    if dados[22]:
                        proprietario = self.get_proprietario_por_cpf_cnpj(
                            dados[22])
                        if proprietario:
                            imovel.set_proprietario(proprietario)
                        else:
                            imovel.set_proprietario(None)
                    else:
                        imovel.set_proprietario(None)
                    if dados[23]:
                        corretor = self.get_corretor_por_cpf_cnpj(dados[23])
                        if corretor:
                            imovel.set_corretor(corretor)
                        else:
                            imovel.set_corretor(None)
                    else:
                        imovel.set_corretor(None)
                    if dados[24]:
                        captador = self.get_captador_por_cpf_cnpj(dados[24])
                        if captador:
                            imovel.set_captador(captador)
                        else:
                            imovel.set_captador(None)
                    else:
                        imovel.set_captador(None)
                    if dados[25]:
                        imovel.set_data_cadastro(datetime.strptime(dados[25]))
                    else:
                        imovel.set_data_cadastro(None)
                    if dados[26]:
                        imovel.set_data_modificacao(
                            datetime.strptime(dados[26]))
                    else:
                        imovel.set_data_modificacao(None)
                    imovel.aceita_pet = dados[27]
                    imovel.churrasqueira = dados[28]
                    imovel.armarios_embutidos = dados[20]
                    imovel.cozinha_americana = dados[30]
                    imovel.area_de_servico = dados[31]
                    imovel.suite_master = dados[32]
                    imovel.banheiro_com_janela = dados[33]
                    imovel.piscina = dados[34]
                    imovel.lareira = dados[35]
                    imovel.ar_condicionado = dados[36]
                    imovel.semi_mobiliado = dados[37]
                    imovel.mobiliado = dados[38]
                    imovel.dependencia_de_empregada = dados[39]
                    imovel.dispensa = dados[40]
                    imovel.deposito = dados[41]
                    lista.append(imovel)
                return lista
            except Exception as e:
                erro = f"ERRO! Banco.get_lista_imoveis_disponiveis: ERRO! {e}"
                print(erro)
                return []

    def get_imoveis_por_categoria(self, categoria):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    f'SELECT * FROM imovel WHERE categoria = ?', (categoria,))
                lista_registros = cursor.fetchall()
                lista_imoveis = []
                if not lista_imoveis:
                    raise Exception(f"Não há imóveis cadastrados")
                for dados in lista_registros:
                    if dados[42]:
                        anuncio = self.get_anuncio(dados[42])
                        if anuncio:
                            imovel.set_anuncio(anuncio)
                        else:
                            imovel.set_anuncio(None)
                    if dados[13]:
                        status = imovel.Status(dados[12])
                    else:
                        status = None
                    if dados[9]:
                        categoria = imovel.Categoria(dados[9])
                    else:
                        categoria = None
                    if dados[10]:
                        endereco = self.get_endereco_por_id(int(dados[10]))
                        if not endereco:
                            raise Exception("Erro com endereço")
                    else:
                        raise Exception("ERRO: Imóvel não possui endereço")
                    imovel = Imovel.Imovel(endereco, status, categoria)

                    if not isinstance(dados[0], str):
                        imovel.set_id(int(dados[0]))
                    if not isinstance(dados[1], str):
                        imovel.set_valor_venda(float(dados[1]))
                    if not isinstance(dados[2], str):
                        imovel.set_valor_aluguel(float(dados[2]))
                    if not isinstance(dados[3], str):
                        imovel.set_quant_quartos(int(dados[3]))
                    if not isinstance(dados[4], str):
                        imovel.set_quant_salas(int(dados[4]))
                    if not isinstance(dados[5], str):
                        imovel.set_quant_vagas(int(dados[5]))
                    if not isinstance(dados[6], str):
                        imovel.set_quant_banheiros(int(dados[6]))
                    if not isinstance(dados[7], str):
                        imovel.set_quant_varandas(int(dados[7]))
                    imovel.set_nome_condominio(dados[8])

                    if not isinstance(dados[12], str):
                        imovel.set_iptu(float(dados[12]))
                    if not isinstance(dados[13], str):
                        imovel.set_valor_condominio(float(dados[13]))
                    if not isinstance(dados[14], str):
                        imovel.set_andar(int(dados[14]))
                    if dados[15]:
                        imovel.set_estado(imovel.Estado(dados[15]))
                    else:
                        imovel.set_estado(None)
                    imovel.set_bloco(dados[16])
                    if not isinstance(dados[17], str):
                        imovel.set_ano_construcao(int(dados[17]))

                    if not isinstance(dados[18], str):
                        imovel.set_area_total(float(dados[18]))

                    if not isinstance(dados[19], str):
                        imovel.set_area_privativa(float(dados[19]))

                    if dados[20]:
                        imovel.set_situacao(imovel.Situacao(dados[20]))
                    else:
                        imovel.set_situacao(None)
                    if dados[21]:
                        imovel.set_ocupacao(imovel.Ocupacao(dados[21]))
                    else:
                        imovel.set_ocupacao(None)
                    if dados[22]:
                        proprietario = self.get_proprietario_por_cpf_cnpj(
                            dados[22])
                        if proprietario:
                            imovel.set_proprietario(proprietario)
                        else:
                            imovel.set_proprietario(None)
                    else:
                        imovel.set_proprietario(None)
                    if dados[23]:
                        corretor = self.get_corretor_por_cpf_cnpj(dados[23])
                        if corretor:
                            imovel.set_corretor(corretor)
                        else:
                            imovel.set_corretor(None)
                    else:
                        imovel.set_corretor(None)
                    if dados[24]:
                        captador = self.get_captador_por_cpf_cnpj(dados[24])
                        if captador:
                            imovel.set_captador(captador)
                        else:
                            imovel.set_captador(None)
                    else:
                        imovel.set_captador(None)
                    if dados[25]:
                        imovel.set_data_cadastro(datetime.strptime(dados[25]))
                    else:
                        imovel.set_data_cadastro(None)
                    if dados[26]:
                        imovel.set_data_modificacao(
                            datetime.strptime(dados[26]))
                    else:
                        imovel.set_data_modificacao(None)
                    imovel.aceita_pet = dados[27]
                    imovel.churrasqueira = dados[28]
                    imovel.armarios_embutidos = dados[20]
                    imovel.cozinha_americana = dados[30]
                    imovel.area_de_servico = dados[31]
                    imovel.suite_master = dados[32]
                    imovel.banheiro_com_janela = dados[33]
                    imovel.piscina = dados[34]
                    imovel.lareira = dados[35]
                    imovel.ar_condicionado = dados[36]
                    imovel.semi_mobiliado = dados[37]
                    imovel.mobiliado = dados[38]
                    imovel.dependencia_de_empregada = dados[39]
                    imovel.dispensa = dados[40]
                    imovel.deposito = dados[41]
                    lista_imoveis.append(imovel)
                return lista_imoveis
            except Exception as e:
                erro = f"ERRO! Banco.get_imoveis_por_categoria: ERRO! {e}"
                print(erro)
                return []
