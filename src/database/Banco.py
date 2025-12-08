import sqlite3
import hashlib
import os
import io

from model import Cliente, Imovel, Captador, Corretor, Atendimento, Endereco, Anuncio, Venda_Aluguel, Condominio, Gerente, Usuario
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
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                senha TEXT NOT NULL,
                email TEXT UNIQUE,
                nome TEXT NOT NULL,
                cpf_cnpj TEXT UNIQUE NOT NULL,
                rg TEXT,
                id_endereco TEXT,
                data_nascimento TEXT,
                tipo_usuario TEXT NOT NULL
                         );
            ''')

            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS telefone (
                id_telefone INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER NOT NULL
                         );
            ''')

            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS telefone_usuario (
                id_usuario INTEGER,
                id_telefone INTEGER,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
                FOREIGN KEY (id_telefone) REFERENCES telefone(telefone)
                         );
            ''')

            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS telefone_proprietario (
                id_telefone INTEGER,
                id_proprietario INTEGER,
                FOREIGN KEY (id_telefone) REFERENCES telefone(telefone)
                FOREIGN KEY (id_proprietario) REFERENCES roprietario (id_proprietario)
                         );
            ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS endereco (
                    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
                    rua TEXT NOT NULL,
                    numero INTEGER NULL,
                    bairro TEXT NOT NULL,
                    cep INTEGER NOT NULL UNIQUE,
                    complemento TEXT NULL,
                    cidade TEXT NOT NULL,
                    uf TEXT NOT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS cliente (
                    id_usuario INTEGER PRIMARY KEY,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS proprietario (
                    id_proprietario INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    cpf_cnpj TEXT NULL UNIQUE,
                    rg TEXT NULL,
                    id_endereco TEXT NULL,
                    data_nascimento TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS captador (
                    id_usuario INTEGER PRIMARY KEY,
                    salario REAL NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS corretor (
                    id_usuario INTEGER PRIMARY KEY,
                    creci TEXT NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
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
                    id_condominio INTEGER NULL,
                    categoria TEXT NOT NULL,
                    id_endereco INTEGER  NULL,
                    status TEXT NOT NULL,
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
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    salario REAL NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
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
                CREATE TABLE IF NOT EXISTS filtros_imovel (
                    id_filtros_imovel INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE                    
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS filtros_condominio
                (
                    id_filtros_condominio INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE                    
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS imovel_filtros (
                    id_filtros_imovel INTEGER,
                    id_imovel INTEGER, 
                    valor BOOLEAN,
                    FOREIGN KEY (id_filtros_imovel) references filtros_imovel (id_filtros_imovel),
                    FOREIGN KEY (id_imovel) references imovel (id_imovel)                
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS condominio_filtros (
                    id_filtros_condominio INTEGER,
                    id_condominio INTEGER, 
                    valor BOOLEAN,
                    FOREIGN KEY (id_filtros_condominio) references filtros_condominio (id_filtros_condominio),
                    FOREIGN KEY (id_condominio) references condominio (id_condominio)                
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS condominio (
                    id_condominio INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NULL,
                    id_endereco INTEGER NULL,
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

    def get_lista_clientes(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = f''' 
                    SELECT * from usuario 
                    WHERE tipo_usuario = CLIENTE
                    '''
                cursor.execute(sql_query)
                dados = cursor.fetchall()
                if not dados:
                    raise Exception(f"Não há usuários cadastrados")
                lista = []
                for registro in dados:
                    id_usuario = int(registro[0])
                    username = registro[1]
                    senha = registro[2]
                    email = registro[3]
                    nome = registro[4]
                    cpf_cnpj = registro[5]
                    rg = registro[6]
                    endereco = registro[7]
                    if endereco:
                        endereco = self.get_endereco_por_id(int(registro[7]))
                    data_nascimento = registro[8]
                    if data_nascimento:
                        data_nascimento = datetime.strptime("%d-%m-%Y")
                    tipo_usuario = registro[9]
                    if tipo_usuario:
                        tipo_usuario = Usuario.Tipo(tipo_usuario)
                    usuario = Cliente.Cliente(
                        username, senha, email, nome, cpf_cnpj)
                    usuario.set_id(id_usuario)
                    usuario.set_rg(rg)
                    usuario.set_endereco(endereco)
                    usuario.set_data_nascimento(data_nascimento)
                    sql_query = f''' 
                                SELECT id_telefone FROM telefone_usuario 
                                WHERE id_usuario = ?
                                '''
                    cursor.execute(sql_query, (id_usuario,))
                    registros = cursor.fetchall()
                    if registros:
                        telefones = []
                        for id_telefone in registros:
                            sql_query = f''' 
                                SELECT numero FROM telefone 
                                WHERE id_telefone = ?
                                    '''
                            cursor.execute(sql_query, (id_telefone,))
                            registro = cursor.fetchone()
                        usuario.set_telefones(telefones)
                    lista.append(usuario)
                return lista
            except Exception as e:
                print(e)
                return []

    def get_lista_usuarios(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = f''' 
                    SELECT * from usuario 
                    '''
                cursor.execute(sql_query)
                dados = cursor.fetchall()
                if not dados:
                    raise Exception(f"Não há usuários cadastrados")
                lista = []
                for registro in dados:
                    id_usuario = int(registro[0])
                    username = registro[1]
                    senha = registro[2]
                    email = registro[3]
                    nome = registro[4]
                    cpf_cnpj = registro[5]
                    rg = registro[6]
                    endereco = registro[7]
                    if endereco:
                        endereco = self.get_endereco_por_id(int(registro[7]))
                    data_nascimento = registro[8]
                    if data_nascimento:
                        data_nascimento = datetime.strptime("%d-%m-%Y")
                    tipo_usuario = registro[9]
                    if tipo_usuario:
                        tipo_usuario = Usuario.Tipo(tipo_usuario)
                    usuario = Usuario.Usuario(
                        username, senha, email, nome, cpf_cnpj, tipo_usuario)
                    sql_query = f''' 
                                SELECT id_telefone FROM telefone_usuario 
                                WHERE id_usuario = ?
                                '''
                    cursor.execute(sql_query, (id_usuario,))
                    registros = cursor.fetchall()
                    if registros:
                        telefones = []
                        for id_telefone in registros:
                            sql_query = f''' 
                                SELECT numero FROM telefone 
                                WHERE id_telefone = ?
                                    '''
                            cursor.execute(sql_query, (id_telefone,))
                            registro = cursor.fetchone()
                    match tipo_usuario:
                        case Usuario.Tipo.CORRETOR:
                            cursor.execute(f'''
                                        SELECT creci FROM corretor 
                                        WHERE id_usuario = ?
                                    ''', (id,))
                            creci = cursor.fetchone()
                            if creci:
                                creci = int(creci)
                            usuario = Corretor.Corretor(
                                username, senha, email, nome, cpf_cnpj, creci)
                        case Usuario.Tipo.CAPTADOR:
                            usuario = Captador.Captador(
                                username, senha, email, nome, cpf_cnpj)
                            cursor.execute(f'''
                                        SELECT salario FROM captador 
                                        WHERE id_usuario = ?
                                    ''', (id,))
                            salario = cursor.fetchone()
                            if salario:
                                salario = float(salario)
                            usuario.set_salario(salario)
                        case Usuario.Tipo.GERENTE:
                            usuario = Gerente.Gerente(
                                username, senha, email, nome, cpf_cnpj)
                            cursor.execute(f'''
                                        SELECT salario FROM gerente 
                                        WHERE id_usuario = ?
                                    ''', (id,))
                            salario = cursor.fetchone()
                            if salario:
                                salario = float(salario)
                            usuario.set_salario(salario)
                        case Usuario.Tipo.CLIENTE:
                            usuario = Cliente.Cliente(
                                username, senha, email, nome, cpf_cnpj)
                            # cursor.execute(f'''
                            #             SELECT * FROM cliente
                            #             WHERE id_usuario = ?
                            #         ''', (id,))
                            # registros = cursor.fetchone()
                    usuario.set_id(id_usuario)
                    usuario.set_rg(rg)
                    usuario.set_endereco(endereco)
                    usuario.set_data_nascimento(data_nascimento)
                    usuario.set_telefones(telefones)
                    lista.append(usuario)
                return lista
            except Exception as e:
                print(e)
                return []

    def cadastrar_usuario(self, usuario):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = f''' 
                    INSERT INTO usuario (username, senha, email, nome, cpf_cnpj, rg, id_endereco, data_nascimento, tipo_usuario) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                if usuario.get_endereco():
                    endereco = usuario.get_endereco().get_id()
                else:
                    endereco = None
                if usuario.get_tipo():
                    tipo = usuario.get_tipo().value
                else:
                    tipo = None
                if usuario.get_data_nascimento():
                    data_nascimento = usuario.get_data_nascimento().strftime("%d-%m-%Y")
                else:
                    data_nascimento = None
                cursor.execute(sql_query, (
                    usuario.get_username(),
                    usuario.get_senha(),
                    usuario.get_email(),
                    usuario.get_nome(),
                    usuario.get_cpf_cnpj(),
                    usuario.get_rg(),
                    endereco,
                    data_nascimento,
                    tipo
                ))
                conexao.commit()
                id = cursor.lastrowid
                if usuario.get_telefones():
                    for telefone in usuario.get_telefones():
                        sql_query = f''' 
                            INSERT INTO telefone (numero) 
                            VALUES(?)
                            '''
                        cursor.execute(sql_query, (telefone,))
                        id_telefone = cursor.lastrowid
                        sql_query = f''' 
                            INSERT INTO telefone_usuario (id_usuario, id_telefone) 
                            VALUES(?, ?)
                            '''
                        cursor.execute(sql_query, (id, id_telefone))
                match usuario.get_tipo():
                    case Usuario.Tipo.CORRETOR:
                        cursor.execute(f'''
                                    INSERT INTO corretor (id_usuario, creci)
                                    VALUES(?, ?)
                                ''', (id, usuario.get_creci()))
                    case Usuario.Tipo.CAPTADOR:
                        cursor.execute(f'''
                                    INSERT INTO captador (id_usuario, salario)
                                    VALUES(?, ?)
                                ''', (id, usuario.get_salario()))
                    case Usuario.Tipo.GERENTE:
                        cursor.execute(f'''
                                    INSERT INTO gerente (id_usuario, salario)
                                    VALUES(?, ?)
                                ''', (id, usuario.get_salario()))
                    case Usuario.Tipo.CLIENTE:
                        cursor.execute(f'''
                                    INSERT INTO cliente (id_usuario)
                                    VALUES(?)
                                ''', (id,))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"ERRO! Banco.cadastrar_usuario: {e}"
                print(erro)
                return False

    def remover(self, campo_desejado, valor, tabela):
        with sqlite3.connect(f"data/Imobiliaria.db") as conexao:
            cursor = conexao.cursor()
            try:
                sql_delete_query = f"""
                DELETE FROM {tabela}
                WHERE {campo_desejado} = ?;
                """
                cursor.execute(sql_delete_query, (valor,))
                conexao.commit()
                return True
            except Exception as e:
                print(f"ERRO Banco.remover {tabela} - {valor}", e)
                return False

    def atualizar(self, campo_desejado, valor, tabela):
        with sqlite3.connect(f"data/Imobiliaria.db") as conexao:
            cursor = conexao.cursor()
            try:
                sql_update_query = f"""
                UPDATE {tabela}
                SET {campo_desejado} = ?
                """
                cursor.execute(sql_update_query, (valor,))
                conexao.commit()
                return True
            except Exception as e:
                print(f"ERRO Banco.atualizar {tabela} - {valor}", e)
                return False

    def get_usuario_por_cpf(self, cpf):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM usuario WHERE cpf_cnpj = ? 
                    ''', (cpf,))
                registro = cursor.fetchone()
                if not registro:
                    raise Exception(f"Não existe usuário com CPF/CNPJ {cpf}")
                id_usuario = int(registro[0])
                username = registro[1]
                senha = registro[2]
                email = registro[3]
                nome = registro[4]
                cpf_cnpj = registro[5]
                rg = registro[6]
                endereco = registro[7]
                if endereco:
                        endereco = self.get_endereco_por_id(int(registro[7]))
                data_nascimento = registro[8]
                if data_nascimento:
                        data_nascimento = datetime.strptime("%d-%m-%Y")
                tipo_usuario = registro[9]
                if tipo_usuario:
                        tipo_usuario = Usuario.Tipo(tipo_usuario)
                usuario = Usuario.Usuario(
                    username, senha, email, nome, cpf_cnpj, tipo_usuario)
                sql_query = f''' 
                            SELECT id_telefone FROM telefone_usuario 
                            WHERE id_usuario = ?
                            '''
                cursor.execute(sql_query, (id_usuario,))
                registros = cursor.fetchall()
                if registros:
                    telefones = []
                    for id_telefone in registros:
                        sql_query = f''' 
                            SELECT numero FROM telefone 
                            WHERE id_telefone = ?
                                '''
                        cursor.execute(sql_query, (id_telefone,))
                        registro = cursor.fetchone()
                match tipo_usuario:
                    case Usuario.Tipo.CORRETOR:
                        cursor.execute(f'''
                                    SELECT creci FROM corretor 
                                    WHERE id_usuario = ?
                                ''', (id,))
                        creci = cursor.fetchone()
                        if creci:
                            creci = int(creci)
                        usuario = Corretor.Corretor(
                            username, senha, email, nome, cpf_cnpj, creci)
                    case Usuario.Tipo.CAPTADOR:
                        usuario = Captador.Captador(
                            username, senha, email, nome, cpf_cnpj)
                        cursor.execute(f'''
                                    SELECT salario FROM captador 
                                    WHERE id_usuario = ?
                                ''', (id,))
                        salario = cursor.fetchone()
                        if salario:
                            salario = float(salario)
                        usuario.set_salario(salario)
                    case Usuario.Tipo.GERENTE:
                        usuario = Gerente.Gerente(
                            username, senha, email, nome, cpf_cnpj)
                        cursor.execute(f'''
                                    SELECT salario FROM gerente 
                                    WHERE id_usuario = ?
                                ''', (id,))
                        salario = cursor.fetchone()
                        if salario:
                            salario = float(salario)
                        usuario.set_salario(salario)
                    case Usuario.Tipo.CLIENTE:
                        usuario = Cliente.Cliente(
                            username, senha, email, nome, cpf_cnpj)
                        # cursor.execute(f'''
                        #             SELECT * FROM cliente
                        #             WHERE id_usuario = ?
                        #         ''', (id,))
                        # registros = cursor.fetchone()
                usuario.set_id(id_usuario)
                usuario.set_rg(rg)
                usuario.set_endereco(endereco)
                usuario.set_data_nascimento(data_nascimento)
                usuario.set_telefones(telefones)
                return usuario
            except Exception as e:
                erro = f"ERRO! Banco.get_usuario_por_cpf(): {e}"
                print(erro)
                return None

    def cadastrar_lista_filtros(self, lista_filtros, tabela):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                for filtro in lista_filtros:
                    sql_query = f''' 
                        INSERT INTO {tabela} (nome) 
                        VALUES(?)
                        '''
                    cursor.execute(sql_query, (
                        filtro,
                    ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"ERRO! Banco.cadastrar_lista_filtros: {e}"
                print(erro)
                return False

    def get_condominio_por_id_imovel(self, id_imovel):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                cursor.execute(f'''
                        SELECT * FROM condominio 
                        WHERE id_imovel = ?
                    ''', (id_imovel,))
                registro = cursor.fetchone()
                if not registro:
                    raise Exception(
                        f"Não existe condomínio para o imóvel com id {id_imovel}")
                id_condominio = int(registro[0])
                nome = registro[1]
                id_endereco = registro[2]
                endereco = self.get_endereco_por_id(id_endereco)
                if not endereco:
                    raise Exception(
                        f"Não existe endereço com id {id_endereco}")
                condominio = Condominio.Condominio()
                condominio.set_id(id_condominio)
                condominio.set_nome(nome)
                condominio.set_endereco(endereco)
                cursor.execute(f'''
                        SELECT * FROM condominio_filtros
                        WHERE id_condominio = ?
                    ''', (id_condominio,))
                condominio_filtros = cursor.fetchall()
                mapa_condominio_filtros = dict()
                if condominio_filtros:
                    for dados in condominio_filtros:
                        id_condominio_filtros = int(dados[0])
                        valor = bool(dados[2])
                        cursor.execute(f'''
                                SELECT * FROM filtros_condominio
                                WHERE id_filtros_condominio = ?
                            ''', (id_condominio_filtros,))
                        novos_dados = cursor.fetchone()
                        if novos_dados:
                            nome = novos_dados[1]
                            mapa_condominio_filtros[nome] = valor
                if mapa_condominio_filtros:
                    condominio.set_filtros(mapa_condominio_filtros)
                return condominio
            except Exception as e:
                erro = f"ERRO! Banco.get_condominio_por_id_imovel(): {e}"
                print(erro)
                return None

    def atualizar_proprietario(self, proprietario):
        # TODO: atualizar telefones

        with sqlite3.connect(f"data/Imobiliaria.db") as conexao:
            cursor = conexao.cursor()
            try:
                sql_update_query = f"""
                UPDATE proprietario
                SET nome = ?,
                    email = ?,
                    endereco = ?
                WHERE cpf_cnpj = ?;
                """
                if proprietario.get_endereco():
                    endereco = proprietario.get_endereco().get_id()
                else:
                    endereco = None
                dados = (proprietario.get_nome(),
                         proprietario.get_email(),
                         endereco,
                         proprietario.get_cpf_cnpj())
                cursor.execute(sql_update_query, dados)
                conexao.commit()
                return True
            except Exception as e:
                print("ERRO Banco.atualizar_proprietario", e)
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
                    corretor = atendimento.get_corretor().get_cpf_cnpj()
                else:
                    corretor = None
                if atendimento.get_get_cliente():
                    cliente = atendimento.get_cliente().get_cpf_cnpj()
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
                    corretor = registro[1]
                    comprador = registro[2]
                    if corretor:
                        corretor = self.get_corretor_por_cpf_cnpj(registro[1])
                    if comprador:
                        comprador = self.get_cliente_por_cpf_cnpj(registro[2])
                    status = registro[3]
                    if status:
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

    def get_anuncio_por_id(self, id_anuncio):
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
                erro = f"ERRO! Banco.get_anuncio(): {e}"
                print(erro)
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

    def get_endereco_por_cep(self, cep):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                sql = '''
                    SELECT * FROM endereco WHERE cep = ? 
                '''
                cursor.execute(sql, (endereco.get_rua(), endereco.get_numero(), endereco.get_bairro(
                ), endereco.get_cep(), endereco.get_complemento(), endereco.get_cidade(), endereco.get_estado()))
                registro = cursor.fetchone()
                if registro:
                    id_endereco = registro[0]
                    rua = registro[1]
                    numero = registro[2]
                    bairro = registro[3]
                    cep = registro[4]
                    complemento = registro[5]
                    cidade = registro[6]
                    uf = registro[7]
                    endereco = Endereco.Endereco(
                        rua, numero, bairro, cep, complemento, cidade)
                    endereco.set_estado(uf)
                    endereco.set_id(id_endereco)
                    return endereco
                else:
                    return None
            except Exception as e:
                print(e)
                return None

    def verificar_usuario(self, username, senha, tabela):
        if tabela == "Cliente":
            tabela = "comprador"
        else:
            tabela = tabela.lower()
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                            SELECT * FROM usuario WHERE username = ?
                        ''', (username,))
                registro = cursor.fetchone()
                print(registro)
                if not registro:
                    raise Exception("Usuário não encontrado")
                senha_hash_banco = registro[2]
                senha_hash = hashlib.sha256(
                    senha.encode('utf-8')).hexdigest()
                if senha_hash_banco == senha_hash:
                    id_usuario = int(registro[0])
                    username = registro[1]
                    senha = registro[2]
                    email = registro[3]
                    nome = registro[4]
                    cpf_cnpj = registro[5]
                    rg = registro[6]
                    endereco = registro[7]
                    if endereco:
                        endereco = self.get_endereco_por_id(endereco)
                    data_nascimento = registro[9]
                    if data_nascimento:
                        data_nascimento = datetime.strptime(
                            data_nascimento[9], "%d-%m-%Y")
                    tipo = Usuario.Tipo(registro[10])
                    usuario = Usuario.Usuario(
                        username, senha_hash_banco, email, nome, cpf_cnpj, tipo)
                    match tipo:
                        case Usuario.Tipo.CORRETOR:
                            cursor.execute(f'''
                                    SELECT creci FROM corretor 
                                    WHERE id_usuario = ?
                                ''', (id,))
                            creci = cursor.fetchone()
                            if creci:
                                creci = int(creci)
                            usuario = Corretor.Corretor(
                                username, senha_hash_banco, email, nome, cpf_cnpj, creci)
                        case Usuario.Tipo.CAPTADOR:
                            usuario = Captador.Captador(
                                username, senha_hash_banco, email, nome, cpf_cnpj)
                            cursor.execute(f'''
                                    SELECT salario FROM captador 
                                    WHERE id_usuario = ?
                                ''', (id,))
                            salario = cursor.fetchone()
                            if salario:
                                salario = float(salario)
                            usuario.set_salario(salario)
                        case Usuario.Tipo.GERENTE:
                            usuario = Gerente.Gerente(
                                username, senha_hash_banco, email, nome, cpf_cnpj)
                            cursor.execute(f'''
                                    SELECT salario FROM gerente 
                                    WHERE id_usuario = ?
                                ''', (id,))
                            salario = cursor.fetchone()
                            if salario:
                                salario = float(salario)
                            usuario.set_salario(salario)
                        case Usuario.Tipo.CLIENTE:
                            usuario = Cliente.Cliente(
                                username, senha_hash_banco, email, nome, cpf_cnpj)
                            # cursor.execute(f'''
                            #         SELECT * FROM cliente 
                            #         WHERE id_usuario = ?
                            #     ''', (id,))
                            # registros = cursor.fetchone()
                    usuario.set_endereco(endereco)
                    usuario.set_data_nascimento(data_nascimento)
                    usuario.set_rg(rg)
                    usuario.set_id(id_usuario)
                    return usuario
                else:
                    raise Exception("Senha errada!")
        except Exception as e:
            print(e)
            return None

    def cadastrar_endereco(self, endereco):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = f''' 
                    INSERT INTO endereco (rua, numero, bairro, cep, complemento, cidade, uf) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    endereco.get_rua(),
                    endereco.get_numero(),
                    endereco.get_bairro(),
                    endereco.get_cep(),
                    endereco.get_complemento(),
                    endereco.get_cidade(),
                    endereco.get_uf(),
                ))
                conexao.commit()
                return True
            except Exception as e:
                erro = f"Banco.cadastrar_endereco: ERRO! {e}"
                print(erro)
                return False

    def cadastrar_proprietario(self, proprietario):
        # TODO: cadastrar telefones
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
                    data = proprietario.get_data_nascimento().strftime("%d-%m-%Y")
                else:
                    data = None
                sql_query = f''' 
                    INSERT INTO proprietario (email, nome, cpf_cnpj, rg, id_endereco, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    proprietario.get_email(),
                    proprietario.get_nome(),
                    proprietario.get_cpf_cnpj(),
                    proprietario.get_rg(),
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
                    INSERT INTO endereco (rua, numero, bairro, cep, complemento, cidade, uf) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    endereco.get_rua(),
                    endereco.get_numero(),
                    endereco.get_bairro(),
                    endereco.get_cep(),
                    endereco.get_complemento(),
                    endereco.get_cidade(),
                    endereco.get_uf(),
                ))
                conexao.commit()
                return cursor.lastrowid
            except Exception as e:
                erro = f"Banco.cadastrar_endereco: ERRO! {e}"
                print(erro)
                return False

    def cadastrar_anuncio(self, anuncio):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = f''' 
                    INSERT INTO anuncio (descricao, titulo) 
                    VALUES(?, ?)
                    '''
                cursor.execute(sql_query, (
                    anuncio.get_descricao(),
                    anuncio.get_titulo(),
                ))
                conexao.commit()
                return cursor.lastrowid
            except Exception as e:
                erro = f"Banco.cadastrar_anuncio: ERRO! {e}"
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
                endereco.set_uf(estado)
                endereco.set_id(id_endereco)
                return endereco
            except Exception as e:
                erro = "Banco.get_endereco_por_id: ERRO!", e
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
                    data_nascimento = datetime.strptime(
                        registro[6], "%d-%m-%Y")
                proprietario = Cliente.Proprietario(        
                    nome, cpf_cnpj, rg, telefone, email)
                proprietario.set_id(id_proprietario)
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
                    imovel.set_data_cadastro(
                        datetime.strptime(dados[25], "%d-%m-%Y"))
                else:
                    imovel.set_data_cadastro(None)
                if dados[26]:
                    imovel.set_data_modificacao(
                        datetime.strptime(dados[26], "%d-%m-%Y"))
                else:
                    imovel.set_data_modificacao(None)
                imovel.set_filtros([])
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
                INSERT INTO imovel(valor_venda, valor_aluguel, quant_quartos, quant_salas, quant_vagas, quant_banheiros, quant_varandas, id_condominio, categoria, id_endereco, status, iptu, valor_condominio, andar, estado, bloco, ano_construcao, area_total, area_privativa, situacao, ocupacao, cpf_cnpj_proprietario, cpf_cnpj_corretor, cpf_cnpj_captador, data_cadastro, data_modificacao, id_anuncio) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    '''
                if imovel.get_categoria():
                    categoria = imovel.get_categoria().value
                if imovel.get_endereco():
                    if imovel.get_endereco().get_id() != None:
                        endereco = imovel.get_endereco().get_id()
                    else:
                        endereco = None
                if imovel.get_anuncio():
                    if imovel.get_anuncio().get_id() != None:
                        anuncio = imovel.get_anuncio().get_id()
                    else:
                        anuncio = None
                if imovel.get_status():
                    status = imovel.get_status().value
                if imovel.get_estado():
                    estado = imovel.get_estado().value
                if imovel.get_situacao():
                    situacao = imovel.get_situacao().value
                if imovel.get_ocupacao():
                    ocupacao = imovel.get_ocupacao().value
                if imovel.get_proprietario():
                    proprietario = imovel.get_proprietario().get_cpf_cnpj()
                if imovel.get_corretor():
                    corretor = imovel.get_corretor().get_cpf_cnpj()
                if imovel.get_captador():
                    captador = imovel.get_captador().get_cpf_cnpj()
                if imovel.get_data_cadastro() and isinstance(imovel.get_data_cadastro(), datetime):
                    data_cadastro = imovel.get_data_cadastro().strftime("%d-%m-%Y")
                if imovel.get_data_modificacao() and isinstance(imovel.get_data_modificacao(), datetime):
                    data_modificacao = imovel.get_data_modificacao().strftime("%d-%m-%Y")
                if imovel.get_ano_construcao() and isinstance(imovel.get_ano_construcao(), datetime):
                    data_modificacao = imovel.get_data_modificacao().strftime("%d-%m-%Y")
                if imovel.get_ano_construcao() and isinstance(imovel.get_ano_construcao(), datetime):
                    ano_construcao = imovel.get_ano_construcao().strftime("%d-%m-%Y")
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
                    ano_construcao,
                    imovel.get_area_total(),
                    imovel.get_area_privativa(),
                    situacao,
                    ocupacao,
                    proprietario,
                    corretor,
                    captador,
                    data_cadastro,
                    data_modificacao,
                    anuncio
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
                    if dados[13]:
                        status = Imovel.Status(dados[12])
                    else:
                        status = None
                    if dados[9]:
                        categoria = Imovel.Categoria(dados[9])
                    else:
                        categoria = None
                    if dados[10] != "" and dados[10] is not None:
                        endereco = self.get_endereco_por_id(int(dados[10]))
                        if not endereco:
                            raise Exception("Erro com endereço")
                    else:
                        raise Exception("ERRO: Imóvel não possui endereço")
                    imovel = Imovel.Imovel(endereco, status, categoria)
                    if dados[42] != "" and dados[42] is not None:
                        anuncio = self.get_anuncio(dados[42])
                        if anuncio:
                            imovel.set_anuncio(anuncio)
                        else:
                            imovel.set_anuncio(None)
                    if not isinstance(dados[0], str) and dados[0] is not None:
                        imovel.set_id(int(dados[0]))
                    if not isinstance(dados[1], str) and dados[1] is not None:
                        imovel.set_valor_venda(float(dados[1]))
                    if not isinstance(dados[2], str) and dados[2] is not None:
                        imovel.set_valor_aluguel(float(dados[2]))
                    if not isinstance(dados[3], str) and dados[3] is not None:
                        imovel.set_quant_quartos(int(dados[3]))
                    if not isinstance(dados[4], str) and dados[4] is not None:
                        imovel.set_quant_salas(int(dados[4]))
                    if not isinstance(dados[5], str) and dados[5] is not None:
                        imovel.set_quant_vagas(int(dados[5]))
                    if not isinstance(dados[6], str) and dados[6] is not None:
                        imovel.set_quant_banheiros(int(dados[6]))
                    if not isinstance(dados[7], str) and dados[7] is not None:
                        imovel.set_quant_varandas(int(dados[7]))
                    imovel.set_nome_condominio(dados[8])
                    if not isinstance(dados[12], str) and dados[12] is not None:
                        imovel.set_iptu(float(dados[12]))
                    if not isinstance(dados[13], str) and dados[13] is not None:
                        imovel.set_valor_condominio(float(dados[13]))
                    if not isinstance(dados[14], str) and dados[14] is not None:
                        imovel.set_andar(int(dados[14]))
                    if dados[15]:
                        imovel.set_estado(Imovel.Estado(dados[15]))
                    else:
                        imovel.set_estado(None)
                    imovel.set_bloco(dados[16])
                    if not isinstance(dados[17], str) and dados[17] is not None:
                        imovel.set_ano_construcao(int(dados[17]))
                    if not isinstance(dados[18], str) and dados[18] is not None:
                        imovel.set_area_total(float(dados[18]))
                    if not isinstance(dados[19], str) and dados[19] is not None:
                        imovel.set_area_privativa(float(dados[19]))
                    if dados[20]:
                        imovel.set_situacao(Imovel.Situacao(dados[20]))
                    else:
                        imovel.set_situacao(None)
                    if dados[21]:
                        imovel.set_ocupacao(Imovel.Ocupacao(dados[21]))
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
                        imovel.set_data_cadastro(
                            datetime.strptime(dados[25], "%d-%m-%Y"))
                    else:
                        imovel.set_data_cadastro(None)
                    if dados[26]:
                        imovel.set_data_modificacao(
                            datetime.strptime(dados[26], "%d-%m-%Y"))
                    else:
                        imovel.set_data_modificacao(None)
                    imovel.set_filtros([])
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
                    if dados[13]:
                        status = Imovel.Status(dados[12])
                    else:
                        status = None
                    if dados[9]:
                        categoria = Imovel.Categoria(dados[9])
                    else:
                        categoria = None
                    if dados[10] != "" and dados[10] is not None:
                        endereco = self.get_endereco_por_id(int(dados[10]))
                        if not endereco:
                            raise Exception("Erro com endereço")
                    else:
                        raise Exception("Imóvel não possui endereço")
                    imovel = Imovel.Imovel(endereco, status, categoria)
                    if dados[42] != "" and dados[42] is not None:
                        anuncio = self.get_anuncio(dados[42])
                        if anuncio:
                            imovel.set_anuncio(anuncio)
                        else:
                            imovel.set_anuncio(None)
                    if not isinstance(dados[0], str) and dados[0] is not None:
                        imovel.set_id(int(dados[0]))
                    if not isinstance(dados[1], str) and dados[1] is not None:
                        imovel.set_valor_venda(float(dados[1]))
                    if not isinstance(dados[2], str) and dados[2] is not None:
                        imovel.set_valor_aluguel(float(dados[2]))
                    if not isinstance(dados[3], str) and dados[3] is not None:
                        imovel.set_quant_quartos(int(dados[3]))
                    if not isinstance(dados[4], str) and dados[4] is not None:
                        imovel.set_quant_salas(int(dados[4]))
                    if not isinstance(dados[5], str) and dados[5] is not None:
                        imovel.set_quant_vagas(int(dados[5]))
                    if not isinstance(dados[6], str) and dados[6] is not None:
                        imovel.set_quant_banheiros(int(dados[6]))
                    if not isinstance(dados[7], str) and dados[7] is not None:
                        imovel.set_quant_varandas(int(dados[7]))
                    imovel.set_nome_condominio(dados[8])
                    if not isinstance(dados[12], str) and dados[12] is not None:
                        imovel.set_iptu(float(dados[12]))
                    if not isinstance(dados[13], str) and dados[13] is not None:
                        imovel.set_valor_condominio(float(dados[13]))
                    if not isinstance(dados[14], str) and dados[14] is not None:
                        imovel.set_andar(int(dados[14]))
                    if dados[15]:
                        imovel.set_estado(Imovel.Estado(dados[15]))
                    else:
                        imovel.set_estado(None)
                    imovel.set_bloco(dados[16])
                    if not isinstance(dados[17], str) and dados[17] is not None:
                        imovel.set_ano_construcao(int(dados[17]))

                    if not isinstance(dados[18], str) and dados[18] is not None:
                        imovel.set_area_total(float(dados[18]))

                    if not isinstance(dados[19], str) and dados[19] is not None:
                        imovel.set_area_privativa(float(dados[19]))

                    if dados[20]:
                        imovel.set_situacao(Imovel.Situacao(dados[20]))
                    else:
                        imovel.set_situacao(None)
                    if dados[21]:
                        imovel.set_ocupacao(Imovel.Ocupacao(dados[21]))
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
                        imovel.set_data_cadastro(
                            datetime.strptime(dados[25], "%d-%m-%Y"))
                    else:
                        imovel.set_data_cadastro(None)
                    if dados[26]:
                        imovel.set_data_modificacao(
                            datetime.strptime(dados[26], "%d-%m-%Y"))
                    else:
                        imovel.set_data_modificacao(None)
                    imovel.set_filtros([])
                    lista.append(imovel)
                return lista
            except Exception as e:
                erro = f"ERRO! Banco.get_lista_imoveis_disponiveis: ERRO! {e}"
                print(erro)
                return []
