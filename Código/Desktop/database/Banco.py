import sqlite3
import hashlib
import os
import io

from model import Cliente, Imovel, Administrador, Captador, Corretor, Endereco
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
                CREATE TABLE IF NOT EXISTS Endereco (
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
                CREATE TABLE IF NOT EXISTS Administrador (
                    id_administrador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NULL ,
                    senha TEXT  NULL,
                    email TEXT NULL 
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Comprador (
                    id_comprador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NULL ,
                    senha TEXT  NULL,
                    email TEXT NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT NULL,
                    endereco TEXT NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Proprietario (
                    id_proprietario INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT NULL,
                    endereco TEXT NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Captador (
                    id_captador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT  NULL ,
                    senha TEXT  NULL,
                    email TEXT  NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT  NULL,
                    endereco TEXT  NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT  NULL,
                    turno TEXT NULL,
                    salario REAL NULL,
                    matricula TEXT NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Corretor (
                    id_corretor INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT  NULL ,
                    senha TEXT  NULL,
                    email TEXT  NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT  NULL,
                    endereco TEXT  NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT  NULL,
                    turno TEXT NULL,
                    salario REAL NULL,
                    matricula TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Imovel (
                    id_imovel INTEGER PRIMARY KEY AUTOINCREMENT,
                    valor_venda REAL NULL,
                    valor_aluguel REAL NULL,
                    quant_quartos INTEGER NULL,
                    quant_salas INTEGER NULL,
                    quant_vagas INTEGER NULL,
                    quant_banheiros INTEGER NULL,
                    quant_varandas INTEGER NULL,
                    nome_condominio TEXT NULL,
                    cor TEXT NULL,
                    categoria TEXT NULL,
                    descricao TEXT NULL,
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
                    FOREIGN KEY (id_endereco) REFERENCES Endereco(id_endereco),
                    FOREIGN KEY (cpf_cnpj_proprietario) REFERENCES Proprietario(cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_corretor) REFERENCES Corretor(cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_captador) REFERENCES Captador(cpf_cnpj)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Midia_Imovel (
                    id_imovel INTEGER  NULL,
                    midia BLOB  NULL,
                    tipo TEXT  NULL,
                    FOREIGN KEY (id_imovel) references Imovel (id_imovel)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Venda_Aluguel (
                    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpf_cnpj_cliente TEXT  NULL,
                    cpf_cnpj_proprietario TEXT  NULL, 
                    cpf_cnpj_captador TEXT NULL,
                    cpf_cnpj_corretor TEXT  NULL,
                    data_venda TEXT  NULL,
                    id_imovel INTEGER  NULL,
                    comissao_captador REAL NULL,
                    comissao_corretor REAL NULL,
                    FOREIGN KEY (id_imovel) REFERENCES Imovel (id_imovel),
                    FOREIGN KEY (cpf_cnpj_cliente) REFERENCES Comprador (cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_proprietario) references Proprietario (cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_corretor) references Corretor (cpf_cnpj)
                    );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Gerente (
                    id_gerente INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT  NULL ,
                    senha TEXT  NULL,
                    email TEXT  NULL ,
                    nome TEXT  NULL,
                    cpf_cnpj TEXT  NULL ,
                    rg TEXT  NULL,
                    telefone TEXT  NULL,
                    endereco TEXT  NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT  NULL,
                    turno TEXT NULL,
                    salario REAL NULL,
                    matricula TEXT NULL
                );
                                ''')

            conexao.commit()

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

                query = '''
                    UPDATE Imovel SET
                        valor_venda = ?,
                        valor_aluguel = ?,
                        quant_quartos = ?,
                        quant_salas = ?,
                        quant_vagas = ?,
                        quant_banheiros = ?,
                        quant_varandas = ?,
                        nome_condominio = ?,
                        cor = ?,
                        categoria = ?,
                        descricao = ?,
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
                        data_modificacao = ?
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
                    imovel.get_cor(),
                    categoria,
                    imovel.get_descricao(),
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
                    imovel.get_id()
                )

                cursor.execute(query, valores)
                self.conn.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def cadastrar_anexo(self, id_imovel, blob, tipo):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:

                sql_query = f''' 
                    INSERT INTO Midia_Imovel (id_imovel, midia, tipo) 
                    VALUES(?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    id_imovel, blob, tipo
                ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"Banco.cadastrar_anexo: ERRO! {e}"
                print(erro)
                return False

    def get_lista_anexos(self, id_imovel):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM Midia_Imovel 
                        WHERE id_imovel = ?
                    ''', (id_imovel,))
                registros = cursor.fetchall()

                imagens = []
                videos = []
                documentos = []

                if not registros:
                    raise Exception("Não há imóveis cadastrados")

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
                erro = "Banco.get_lista_anexos: ERRO!", e
                print(erro)
                return []

    def get_lista_compradores(self):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM Comprador 
                    ''')
                registros = cursor.fetchall()

                if not registros:
                    raise Exception("Não há compradores cadastrados")

                return registros
            except Exception as e:
                erro = "Banco.get_lista_compradores: ERRO!", e
                print(erro)
                return []

    def get_lista_proprietarios(self):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM Proprietario 
                    ''')
                registros = cursor.fetchall()

                if not registros:
                    raise Exception("Não há proprietarios cadastrados")

                return registros
            except Exception as e:
                erro = "Banco.get_lista_proprietarios: ERRO!", e
                print(erro)
                return []

    def verificar_usuario(self, username, senha, tabela):
        if tabela == "Cliente":
            tabela == "Comprador"

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
                        case "Comprador":
                            pessoa = Cliente.Comprador(*registro[1:])
                        case "Corretor":
                            pessoa = Corretor.Corretor(*registro[1:]), ""
                        case "Captador":
                            pessoa = Captador.Captador(*registro[1:]), ""
                        case "Administrador":
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
                    INSERT INTO Endereco (rua, numero, bairro, cep, complemento, cidade, estado) 
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
                senha_hash = hashlib.sha256(
                    corretor.get_senha().encode('utf-8')).hexdigest()
                sql_query = f''' 
                    INSERT INTO Corretor (username, senha, email, nome, cpf_cnpj, rg, telefone, endereco, idade, data_nascimento) 
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
                    corretor.get_endereco(),
                    corretor.get_idade(),
                    corretor.get_data_nascimento()
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
                senha_hash = hashlib.sha256(
                    captador.get_senha().encode('utf-8')).hexdigest()
                sql_query = f''' 
                    INSERT INTO Captador (username, senha, email, nome, cpf_cnpj, rg, telefone, endereco, idade, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    captador.get_username(),
                    senha_hash,
                    captador.get_email(),
                    captador.get_nome(),
                    captador.get_cpf_cnpj(),
                    captador.get_rg(),
                    captador.get_telefone(),
                    captador.get_endereco(),
                    captador.get_idade(),
                    captador.get_data_nascimento()
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
                if isinstance(proprietario, Cliente.Proprietario):

                    sql_query = f''' 
                    INSERT INTO Proprietario (email, nome, cpf_cnpj, rg, telefone, endereco, idade, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    cursor.execute(sql_query, (
                        proprietario.get_email(),
                        proprietario.get_nome(),
                        proprietario.get_cpf_cnpj(),
                        proprietario.get_rg(),
                        proprietario.get_telefone(),
                        proprietario.get_endereco(),
                        proprietario.get_idade(),
                        proprietario.get_data_nascimento()
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
                    INSERT INTO Endereco (rua, numero, bairro, cep, complemento, cidade, estado) 
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
                if isinstance(comprador, Cliente.Comprador):
                    senha_hash = hashlib.sha256(
                        comprador.get_senha().encode('utf-8')).hexdigest()
                    sql_query = f''' 
                    INSERT INTO Comprador (username, senha, email, nome, cpf_cnpj, rg, telefone, endereco, idade, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    cursor.execute(sql_query, (
                        comprador.get_username(),
                        senha_hash,
                        comprador.get_email(),
                        comprador.get_nome(),
                        comprador.get_cpf_cnpj(),
                        comprador.get_rg(),
                        comprador.get_telefone(),
                        comprador.get_endereco(),
                        comprador.get_idade(),
                        comprador.get_data_nascimento()
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
                        SELECT * FROM Endereco 
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
                erro = "Banco.get_lista_proprietarios: ERRO!", e
                print(erro)
                return None

    def get_corretor_por_cpf_cnpj(self, cpf_cnpj):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM Corretor 
                        WHERE cpf_cnpj = ?
                    ''', (cpf_cnpj,))
                registros = cursor.fetchone()

                if not registros:
                    raise Exception(
                        f"Não há proprietarios cadastrados com cpf_cnpj {cpf_cnpj}")

                return registros
            except Exception as e:
                erro = "Banco.get_lista_proprietarios: ERRO!", e
                print(erro)
                return None

    def get_captador_por_cpf_cnpj(self, cpf_cnpj):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM Captador 
                        WHERE cpf_cnpj = ?
                    ''', (cpf_cnpj,))
                registros = cursor.fetchone()

                if not registros:
                    raise Exception("Não há proprietarios cadastrados")

                return registros
            except Exception as e:
                erro = "Banco.get_lista_proprietarios: ERRO!", e
                print(erro)
                return None

    def get_proprietario_por_cpf_cnpj(self, cpf_cnpj):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM Proprietario 
                        WHERE cpf_cnpj = ?
                    ''', (cpf_cnpj,))
                registros = cursor.fetchone()

                if not registros:
                    raise Exception("Não há proprietarios cadastrados")

                return registros
            except Exception as e:
                erro = "Banco.get_lista_proprietarios: ERRO!", e
                print(erro)
                return None

    def get_imovel_por_codigo(self, codigo):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    f'SELECT * FROM Imovel WHERE codigo = ?', (codigo,))
                registro = cursor.fetchone()
                if not registro:
                    raise Exception(f"Nenhum imóvel com codigo {codigo}")

                if registro[0]:
                    mapa_anexos = self.get_lista_anexos(registro[0])
                if registro[13]:
                    status = Imovel.Status(registro[13])
                if registro[10]:
                    categoria = Imovel.Categoria(registro[10])
                if registro[12]:
                    endereco = self.get_endereco_por_id(int(registro[12]))
                    if not endereco:
                        raise Exception("Erro com endereço")
                imovel = Imovel.Imovel(endereco, status, categoria)
                if mapa_anexos["Imagens"]:
                    imovel.set_imagens(mapa_anexos["Imagens"])
                if mapa_anexos["Videos"]:
                    imovel.set_videos(mapa_anexos["Videos"])
                if mapa_anexos["Documentos"]:
                    imovel.set_anexos(mapa_anexos["Documentos"])
                imovel.set_id(int(registro[0]))
                imovel.set_valor_venda(float(registro[1])),
                imovel.set_valor_aluguel(float(registro[2])),
                imovel.set_quant_quartos(int(registro[3])),
                imovel.set_quant_salas(int(registro[4])),
                imovel.set_quant_vagas(int(registro[5])),
                imovel.set_quant_banheiros(int(registro[6])),
                imovel.set_quant_varandas(int(registro[7])),
                imovel.set_nome_condominio(registro[8]),
                imovel.set_cor(registro[9]),
                imovel.set_descricao(registro[11]),
                imovel.set_iptu(float(registro[14])),
                imovel.set_valor_condominio(float(registro[15])),
                imovel.set_andar(int(registro[16])),
                if registro[17]:
                    imovel.set_estado(Imovel.Estado(registro[17])),
                imovel.set_bloco(registro[18]),
                imovel.set_ano_construcao(datetime(year=registro[19])),
                imovel.set_area_total(float(registro[20])),
                imovel.set_area_privativa(float(registro[21])),
                if registro[22]:
                    imovel.set_situacao(Imovel.Situacao(registro[22])),
                if registro[23]:
                    imovel.set_ocupacao(Imovel.Ocupacao(registro[23])),
                if registro[24]:
                    proprietario = self.get_proprietario_por_cpf_cnpj(registro[24])
                    if proprietario:
                        imovel.set_proprietario(proprietario),
                if registro[25]:
                    corretor = self.get_corretor_por_cpf_cnpj(registro[25])
                    if corretor:
                        imovel.set_corretor(corretor)
                if registro[26]:
                    captador = self.get_captador_por_cpf_cnpj(registro[26])
                    if captador:
                        imovel.set_captador(captador)
                return imovel
            except Exception as e:
                erro = f"Banco.get_imovel_por_id: ERRO! {e}"
                print(erro)
                return None

    def cadastrar_imovel(self, imovel):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO Imovel(valor_venda, valor_aluguel, quant_quartos, quant_salas, quant_vagas, quant_banheiros, quant_varandas, nome_condominio, cor, categoria, descricao, id_endereco, status, iptu, valor_condominio, andar, estado, bloco, ano_construcao, area_total, area_privativa, situacao, ocupacao, cpf_cnpj_proprietario, cpf_cnpj_corretor, cpf_cnpj_captador, data_cadastro, data_modificacao) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    imovel.get_cor(),
                    categoria,
                    imovel.get_descricao(),
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
                ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"Banco.cadastrar_imovel: ERRO! {e}"
                print(erro)
                return False

    def get_lista_imoveis(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:

                cursor = conexao.cursor()
                lista = []
                cursor.execute("SELECT * FROM Imovel")
                resultados = cursor.fetchall()
                if not resultados:
                    raise Exception(f"Tabela imovel esta vázia")
                for dados in resultados:
                    if dados[0]:
                        mapa_anexos = self.get_lista_anexos(dados[0])
                    else:
                        mapa_anexos = None
                    if dados[13]:
                        status = Imovel.Status(dados[13])
                    else:
                        status = None
                    if dados[10]:
                        categoria = Imovel.Categoria(dados[10])
                    else:
                        categoria = None
                    if dados[12]:
                        print(dados[12])
                        endereco = self.get_endereco_por_id(int(dados[12]))
                        if not endereco:
                            raise Exception("Erro com endereço")
                    else:
                        raise Exception("ERRO: Imóvel não possui endereço")
                    imovel = Imovel.Imovel(endereco, status, categoria)
                    if mapa_anexos["Imagens"] and isinstance(mapa_anexos["Imagens"], list):
                        imovel.set_imagens(mapa_anexos["Imagens"])
                    if mapa_anexos["Videos"] and isinstance(mapa_anexos["Videos"], list):
                        imovel.set_videos(mapa_anexos["Videos"] and isinstance(
                            mapa_anexos["Imagens"], list))
                    if mapa_anexos["Documentos"] and isinstance(mapa_anexos["Documentos"], list):
                        imovel.set_anexos(mapa_anexos["Documentos"])
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
                    imovel.set_cor(dados[9])
                    imovel.set_descricao(dados[11])
                    if not isinstance(dados[14], str):
                        imovel.set_iptu(float(dados[14]))
                    if not isinstance(dados[15], str):
                        imovel.set_valor_condominio(float(dados[15]))
                    if not isinstance(dados[16], str):
                        imovel.set_andar(int(dados[16]))
                    if dados[17]:
                        imovel.set_estado(Imovel.Estado(dados[17]))
                    else:
                        imovel.set_estado(None)
                    imovel.set_bloco(dados[18])
                    if not isinstance(dados[19], str):
                        imovel.set_ano_construcao(int(dados[19]))

                    if not isinstance(dados[20], str):
                        imovel.set_area_total(float(dados[20]))

                    if not isinstance(dados[21], str):
                        imovel.set_area_privativa(float(dados[21]))

                    if dados[22]:
                        imovel.set_situacao(Imovel.Situacao(dados[22]))
                    else:
                        imovel.set_situacao(None)
                    if dados[23]:
                        imovel.set_ocupacao(Imovel.Ocupacao(dados[23]))
                    else:
                        imovel.set_ocupacao(None)
                    if dados[24]:
                        proprietario = self.get_proprietario_por_cpf_cnpj(dados[24])
                        if proprietario:
                            imovel.set_proprietario(proprietario)
                        else:
                            imovel.set_proprietario(None)
                    else:
                        imovel.set_proprietario(None)
                    if dados[25]:
                        corretor = self.get_corretor_por_cpf_cnpj(dados[25])
                        if corretor:
                            imovel.set_corretor(corretor)
                        else:
                            imovel.set_corretor(None)
                    else:
                        imovel.set_corretor(None)
                    if dados[26]:
                        captador = self.get_captador_por_cpf_cnpj(dados[26])
                        if captador:
                            imovel.set_captador(captador)
                        else:
                            imovel.set_captador(None)
                    else:
                        imovel.set_captador(None)
                    if dados[27]:
                        imovel.set_data_cadastro(datetime.strptime(dados[27]))
                    else:
                        imovel.set_data_cadastro(None)
                    if dados[28]:
                        imovel.set_data_modificacao(
                            datetime.strptime(dados[28]))
                    else:
                        imovel.set_data_modificacao(None)
                    lista.append(imovel)
                return lista
            except Exception as e:
                erro = f"Banco.get_lista_imoveis: ERRO! {e}"
                print(erro)
                return []

    def get_lista_imoveis_disponiveis(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                lista = []
                cursor.execute(
                    "SELECT * FROM Imovel WHERE status IN ('Venda', 'Aluguel', 'Venda_Aluguel')")
                resultados = cursor.fetchall()
                if not resultados:
                    raise Exception(f"Tabela imovel esta vázia")

                for dados in resultados:
                    if dados[0]:
                        mapa_anexos = self.get_lista_anexos(dados[0])
                    if dados[13]:
                        status = Imovel.Status(dados[13])
                    if dados[10]:
                        categoria = Imovel.Categoria(dados[10])

                    if dados[12]:
                        endereco = self.get_endereco_por_id(int(dados[12]))
                        if not endereco:
                            raise Exception("Erro com endereço")
                    imovel = Imovel.Imovel(endereco, status, categoria)
                    if mapa_anexos["Imagens"]:
                        imovel.set_imagens(mapa_anexos["Imagens"])
                    if mapa_anexos["Videos"]:
                        imovel.set_videos(mapa_anexos["Videos"])
                    if mapa_anexos["Documentos"]:
                        imovel.set_anexos(mapa_anexos["Documentos"])
                    imovel.set_id(int(dados[0]))
                    imovel.set_valor_venda(float(dados[1])),
                    imovel.set_valor_aluguel(float(dados[2])),
                    imovel.set_quant_quartos(int(dados[3])),
                    imovel.set_quant_salas(int(dados[4])),
                    imovel.set_quant_vagas(int(dados[5])),
                    imovel.set_quant_banheiros(int(dados[6])),
                    imovel.set_quant_varandas(int(dados[7])),
                    imovel.set_nome_condominio(dados[8]),
                    imovel.set_cor(dados[9]),
                    imovel.set_descricao(dados[11]),
                    imovel.set_iptu(float(dados[14])),
                    imovel.set_valor_condominio(float(dados[15])),
                    imovel.set_andar(int(dados[16])),
                    if dados[17]:
                        imovel.set_estado(Imovel.Estado(dados[17])),
                    imovel.set_bloco(dados[18]),
                    imovel.set_ano_construcao(datetime(year=dados[19])),
                    imovel.set_area_total(float(dados[20])),
                    imovel.set_area_privativa(float(dados[21])),
                    if dados[22]:
                        imovel.set_situacao(Imovel.Situacao(dados[22])),
                    if dados[23]:
                        imovel.set_ocupacao(Imovel.Ocupacao(dados[23])),
                    if dados[24]:
                        proprietario = self.get_proprietario_por_cpf_cnpj(dados[24])
                        if proprietario:
                            imovel.set_proprietario(proprietario),
                    if dados[25]:
                        corretor = self.get_corretor_por_cpf_cnpj(dados[25])
                        if corretor:
                            imovel.set_corretor(corretor)
                    if dados[26]:
                        captador = self.get_captador_por_cpf_cnpj(dados[26])
                        if captador:
                            imovel.set_captador(captador)
                    if dados[27]:
                        imovel.set_data_cadastro(datetime(dados[27]))
                    if dados[28]:
                        imovel.set_data_modificacao(datetime(dados[28]))

                    list.append(imovel)
                return lista
            except Exception as e:
                erro = f"Banco.get_lista_imoveis_disponiveis: ERRO! {e}"
                print(erro)
                return []

    def get_imoveis_por_categoria(self, categoria):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    f'SELECT * FROM Imovel WHERE categoria = ?', (categoria,))
                lista_registros = cursor.fetchall()
                lista_imoveis = []
                if not lista_imoveis:
                    raise Exception(f"Tabela imovel esta vázia")
                for registro in lista_registros:
                    if registro[0]:
                        mapa_anexos = self.get_lista_anexos(registro[0])
                    if registro[13]:
                        status = Imovel.Status(registro[13])
                    if registro[10]:
                        categoria = Imovel.Categoria(registro[10])
                    if registro[12]:
                        endereco = self.get_endereco_por_id(int(registro[12]))
                        if not endereco:
                            raise Exception("Erro com endereço")
                    imovel = Imovel.Imovel(endereco, status, categoria)
                    if mapa_anexos["Imagens"]:
                        imovel.set_imagens(mapa_anexos["Imagens"])
                    if mapa_anexos["Videos"]:
                        imovel.set_videos(mapa_anexos["Videos"])
                    if mapa_anexos["Documentos"]:
                        imovel.set_anexos(mapa_anexos["Documentos"])
                    imovel.set_id(int(registro[0]))
                    imovel.set_valor_venda(float(registro[1])),
                    imovel.set_valor_aluguel(float(registro[2])),
                    imovel.set_quant_quartos(int(registro[3])),
                    imovel.set_quant_salas(int(registro[4])),
                    imovel.set_quant_vagas(int(registro[5])),
                    imovel.set_quant_banheiros(int(registro[6])),
                    imovel.set_quant_varandas(int(registro[7])),
                    imovel.set_nome_condominio(registro[8]),
                    imovel.set_cor(registro[9]),
                    imovel.set_descricao(registro[11]),
                    imovel.set_iptu(float(registro[14])),
                    imovel.set_valor_condominio(float(registro[15])),
                    imovel.set_andar(int(registro[16])),
                    if registro[17]:
                        imovel.set_estado(Imovel.Estado(registro[17])),
                    imovel.set_bloco(registro[18]),
                    imovel.set_ano_construcao(datetime(year=registro[19])),
                    imovel.set_area_total(float(registro[20])),
                    imovel.set_area_privativa(float(registro[21])),
                    if registro[22]:
                        imovel.set_situacao(Imovel.Situacao(registro[22])),
                    if registro[23]:
                        imovel.set_ocupacao(Imovel.Ocupacao(registro[23])),
                    if registro[24]:
                        proprietario = self.get_proprietario_por_cpf_cnpj(
                            registro[24])
                        if proprietario:
                            imovel.set_proprietario(proprietario),
                    if registro[25]:
                        corretor = self.get_corretor_por_cpf_cnpj(registro[25])
                        if corretor:
                            imovel.set_corretor(corretor)
                    if registro[26]:
                        captador = self.get_captador_por_cpf_cnpj(registro[26])
                        if captador:
                            imovel.set_captador(captador)
                    lista_imoveis.append(imovel)
                return lista_imoveis
            except Exception as e:
                erro = f"Banco.get_imoveis_por_categoria: ERRO! {e}"
                print(erro)
                return []
