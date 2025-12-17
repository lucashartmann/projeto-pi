import sqlite3
import hashlib
import os
import io

from model import Cliente, Imovel, Captador, Corretor, Atendimento, Endereco, Anuncio, Venda_Aluguel, Condominio, Gerente, Usuario, Proprietario
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
                numero INTEGER NOT NULL UNIQUE
                         );
            ''')

            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS telefone_usuario (
                id_usuario INTEGER,
                id_telefone INTEGER,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
                FOREIGN KEY (id_telefone) REFERENCES telefone(telefone) ON DELETE CASCADE
                         );
            ''')

            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS telefone_proprietario (
                id_telefone INTEGER,
                id_proprietario INTEGER,
                FOREIGN KEY (id_telefone) REFERENCES telefone(telefone) ON DELETE CASCADE,
                FOREIGN KEY (id_proprietario) REFERENCES roprietario (id_proprietario) ON DELETE CASCADE
                         );
            ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS endereco (
                    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
                    rua TEXT NOT NULL,
                    numero INTEGER NULL,
                    bairro TEXT NOT NULL,
                    cep INTEGER NOT NULL,
                    complemento TEXT NULL,
                    cidade TEXT NOT NULL,
                    uf TEXT NOT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS cliente (
                    id_usuario INTEGER PRIMARY KEY,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
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
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS corretor (
                    id_usuario INTEGER PRIMARY KEY,
                    creci TEXT NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
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
                    cpf_cnpj_corretor TEXT NULL,
                    cpf_cnpj_captador TEXT NULL,
                    data_cadastro TEXT NUll,
                    data_modificacao TEXT NUll,
                    id_anuncio INT NULL,
                    id_condominio INT NULL,
                    FOREIGN KEY (id_anuncio) REFERENCES anuncio(id_anuncio),
                    FOREIGN KEY (id_endereco) REFERENCES endereco(id_endereco),
                    FOREIGN KEY (cpf_cnpj_corretor) REFERENCES corretor(cpf_cnpj),
                    FOREIGN KEY (cpf_cnpj_captador) REFERENCES captador(cpf_cnpj)
                    FOREIGN KEY (id_condominio) REFERENCES condominio (id_condominio)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS midia_anuncio (
                    id_anuncio INTEGER  NULL,
                    midia BLOB  NULL,
                    tipo TEXT  NULL,
                    FOREIGN KEY (id_anuncio) references anuncio (id_anuncio) ON DELETE CASCADE
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
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
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
                    FOREIGN KEY (cpf_cnpj_comprador) references comprador (cpf_cnpj) ON DELETE CASCADE
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
                    FOREIGN KEY (id_filtros_imovel) references filtros_imovel (id_filtros_imovel) ON DELETE CASCADE,
                    FOREIGN KEY (id_imovel) references imovel (id_imovel) ON DELETE CASCADE                
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS condominio_filtros (
                    id_filtros_condominio INTEGER,
                    id_condominio INTEGER, 
                    FOREIGN KEY (id_filtros_condominio) references filtros_condominio (id_filtros_condominio) ON DELETE CASCADE,
                    FOREIGN KEY (id_condominio) references condominio (id_condominio) ON DELETE CASCADE               
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
                CREATE TABLE IF NOT EXISTS proprietario_imovel (
                    cpf_cnpj_proprietario INTEGER  NULL,
                    id_imovel INTEGER NULL,
                    FOREIGN KEY (cpf_cnpj_proprietario) references proprietario (cpf_cnpj_proprietario) ON DELETE CASCADE,
                    FOREIGN KEY (id_imovel) references imovel (id_imovel) ON DELETE CASCADE                
                );
                                ''')

            conexao.commit()

    def get_lista_enderecos(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = f'''
                    SELECT * 
                    FROM endereco 
                '''
                cursor.execute(sql_query)
                dados = cursor.fetchall()
                if not dados:
                    raise Exception(f"Não há enderecos cadastrados")
                lista = []
                for registro in dados:
                    id_endereco = int(registro[0])
                    rua = registro[1]
                    numero = registro[2]
                    if numero:
                        numero = int(numero)
                    bairro = registro[3]
                    cep = registro[4]
                    if cep:
                        cep = int(cep)
                    complemento = registro[5]
                    cidade = registro[6]
                    uf = registro[7]
                    endereco = Endereco.Endereco(
                        rua, bairro, cep, cidade, uf)
                    endereco.set_id(id_endereco)
                    endereco.set_numero(numero)
                    endereco.set_complemento(complemento)
                    lista.append(endereco)
                return lista
            except Exception as e:
                erro = f"ERRO! Banco.get_lista_enderecos: {e}"
                print(erro)
                return []

    def get_lista_proprietarios(self):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                sql_query = f''' 
                    SELECT * FROM proprietario
                    '''
                cursor.execute(sql_query)
                dados = cursor.fetchall()
                if not dados:
                    raise Exception(f"Não há proprietarios cadastrados")
                lista = []
                for registro in dados:
                    id_proprietario = int(registro[0])
                    email = registro[1]
                    nome = registro[2]
                    cpf_cnpj = registro[3]
                    rg = registro[4]
                    data_nascimento = registro[5]
                    if data_nascimento:
                        data_nascimento = datetime.strptime(
                            data_nascimento, "%d-%m-%Y")
                    proprietario = Proprietario.Proprietario(
                        email, nome, cpf_cnpj)
                    proprietario.set_id(id_proprietario)
                    proprietario.set_data_nascimento(data_nascimento)
                    proprietario.set_rg(rg)
                    lista.append(proprietario)
                return lista
        except Exception as e:
            erro = f"ERRO! Banco.get_lista_clientes: {e}"
            print(erro)
            return []

    def get_lista_clientes(self):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()

                sql_query = f''' 
                    SELECT * from usuario 
                    WHERE tipo_usuario = 'CLIENTE'
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
                        data_nascimento = datetime.strptime(
                            data_nascimento, "%d-%m-%Y")
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
            erro = f"ERRO! Banco.get_lista_clientes:{e}"
            print(erro)
            return []

    def get_lista_usuarios(self):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
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
                        data_nascimento = datetime.strptime(
                            data_nascimento, "%d-%m-%Y")
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
                    telefones = []
                    if registros:
                        for id_telefone in registros:
                            sql_query = f''' 
                                SELECT numero FROM telefone 
                                WHERE id_telefone = ?
                                    '''
                            cursor.execute(sql_query, (id_telefone,))
                            numero = cursor.fetchone()[0]
                            telefones.append(numero)
                    match tipo_usuario:
                        case Usuario.Tipo.CORRETOR:
                            cursor.execute(f'''
                                        SELECT creci FROM corretor 
                                        WHERE id_usuario = ?
                                    ''', (id_usuario,))
                            creci = cursor.fetchone()[0]
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
                                    ''', (id_usuario,))
                            salario = cursor.fetchone()[0]
                            if salario:
                                salario = float(salario)
                            usuario.set_salario(salario)
                        case Usuario.Tipo.GERENTE:
                            usuario = Gerente.Gerente(
                                username, senha, email, nome, cpf_cnpj)
                            cursor.execute(f'''
                                        SELECT salario FROM gerente 
                                        WHERE id_usuario = ?
                                    ''', (id_usuario,))
                            salario = cursor.fetchone()[0]
                            if salario:
                                salario = float(salario)
                            usuario.set_salario(salario)
                        case Usuario.Tipo.CLIENTE:
                            usuario = Cliente.Cliente(
                                username, senha, email, nome, cpf_cnpj)
                            # cursor.execute(f'''
                            #             SELECT * FROM cliente
                            #             WHERE id_usuario = ?
                            #         ''', (id_usuario,))
                            # registros = cursor.fetchone()
                    usuario.set_id(id_usuario)
                    usuario.set_rg(rg)
                    usuario.set_endereco(endereco)
                    usuario.set_data_nascimento(data_nascimento)
                    usuario.set_telefones(telefones)
                    lista.append(usuario)
                return lista
        except Exception as e:
            erro = f"ERRO! Banco.get_lista_usuarios: {e}"
            print(erro)
            return []

    def cadastrar_usuario(self, usuario):
        try:

            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
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
                senha_hash = hashlib.sha256(
                    usuario.get_senha().encode('utf-8')).hexdigest()
                cursor.execute(sql_query, (
                    usuario.get_username(),
                    senha_hash,
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
        try:
            with sqlite3.connect(f"data/Imobiliaria.db") as conexao:
                cursor = conexao.cursor()
                sql_delete_query = f"""
                DELETE FROM {tabela}
                WHERE {campo_desejado} = ?;
                """
                cursor.execute(sql_delete_query, (valor,))
                conexao.commit()
                return True
        except Exception as e:
            print(f"ERRO Banco.remover {tabela} - {valor} {e}")
            return False

    def atualizar(self, campo_desejado, valor, tabela):
        try:
            with sqlite3.connect(f"data/Imobiliaria.db") as conexao:
                cursor = conexao.cursor()
                sql_update_query = f"""
                UPDATE {tabela}
                SET {campo_desejado} = ?
                """
                cursor.execute(sql_update_query, (valor,))
                conexao.commit()
                return True
        except Exception as e:
            print(f"ERRO Banco.atualizar {tabela} - {valor} {e}")
            return False

    def get_usuario_por_cpf_cnpj(self, cpf):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
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
                    data_nascimento = datetime.strptime(
                        data_nascimento, "%d-%m-%Y")
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
                telefones = []
                if registros:
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
                                ''', (id_usuario,))
                        creci = cursor.fetchone()[0]
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
                                ''', (id_usuario,))
                        salario = cursor.fetchone()[0]
                        if salario:
                            salario = float(salario)
                        usuario.set_salario(salario)
                    case Usuario.Tipo.GERENTE:
                        usuario = Gerente.Gerente(
                            username, senha, email, nome, cpf_cnpj)
                        cursor.execute(f'''
                                    SELECT salario FROM gerente 
                                    WHERE id_usuario = ?
                                ''', (id_usuario,))
                        salario = cursor.fetchone()[0]
                        if salario:
                            salario = float(salario)
                        usuario.set_salario(salario)
                    case Usuario.Tipo.CLIENTE:
                        usuario = Cliente.Cliente(
                            username, senha, email, nome, cpf_cnpj)
                        # cursor.execute(f'''
                        #             SELECT * FROM cliente
                        #             WHERE id_usuario = ?
                        #         ''', (id_usuario,))
                        # registros = cursor.fetchone()
                usuario.set_id(id_usuario)
                usuario.set_rg(rg)
                usuario.set_endereco(endereco)
                usuario.set_data_nascimento(data_nascimento)
                usuario.set_telefones(telefones)
                return usuario
        except Exception as e:
            erro = f"ERRO! Banco.get_usuario_por_cpf_cnpj: {e}"
            print(erro)
            return None

    def get_lista_filtros_apartamento(self):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM filtros_imovel 
                    ''')
                registros = cursor.fetchall()
                if not registros:
                    raise Exception(f"Não existe filtros")

                lista = []

                for registro in registros:
                    nome = registro[1]
                    lista.append(nome)

                return lista

        except Exception as e:
            print(f"ERRO! Banco.get_lista_filtros_apartamento: {e}")
            return []
        

    def get_lista_filtros_condominio(self):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM filtros_condominio 
                    ''')
                registros = cursor.fetchall()
                if not registros:
                    raise Exception(f"Não existe filtros")

                lista = []

                for registro in registros:
                    nome = registro[1]
                    lista.append(nome)

                return lista

        except Exception as e:
            print(f"ERRO! Banco.get_lista_filtros_apartamento: {e}")
            return []

    def cadastrar_lista_filtros(self, lista_filtros, tabela):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
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
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
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
                lista_condominio_filtros = []
                if condominio_filtros:
                    for dados in condominio_filtros:
                        id_condominio_filtros = int(dados[0])
                        cursor.execute(f'''
                                SELECT nome FROM filtros_condominio
                                WHERE id_filtros_condominio = ?
                            ''', (id_condominio_filtros,))
                        nome = cursor.fetchone()
                        if nome:
                            lista_condominio_filtros.append(nome)
                if lista_condominio_filtros:
                    condominio.set_filtros(lista_condominio_filtros)
                return condominio
        except Exception as e:
            erro = f"ERRO! Banco.get_condominio_por_id_imovel: {e}"
            print(erro)
            return None

    def atualizar_proprietario(self, proprietario):
        # TODO: atualizar telefones
        try:
            with sqlite3.connect(f"data/Imobiliaria.db") as conexao:
                cursor = conexao.cursor()
                sql_update_query = f"""
                UPDATE proprietario
                SET email = ?,
                    nome = ?,
                    cpf_cnpj = ?,
                    rg = ?,
                    id_endereco = ?,
                    data_nascimento = ?
                WHERE cpf_cnpj = ?;
                """
                endereco = proprietario.get_endereco()
                if endereco:
                    endereco = endereco.get_id()

                data_nascimento = proprietario.get_data_nascimento()
                if data_nascimento:
                    data_nascimento = data_nascimento.strftime("%d-%m-%Y")

                dados = (proprietario.get_email(), proprietario.get_nome(), proprietario.get_cpf_cnpj(), proprietario.get_rg(),
                         endereco, data_nascimento, proprietario.get_cpf_cnpj()
                         )
                cursor.execute(sql_update_query, dados)
                conexao.commit()
                return True
        except Exception as e:
            print(f"ERRO Banco.atualizar_proprietario {e}")
            return False

    def cadastrar_atendimento(self, atendimento):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                sql_query = f''' 
                    INSERT INTO atendimento (id_imovel, cpf_cnpj_corretor, cpf_cnpj_comprador, status) 
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    '''
                corretor = atendimento.get_corretor()
                if corretor:
                    corretor = corretor.get_cpf_cnpj()
                cliente = atendimento.get_cliente()
                if cliente:
                    cliente = cliente.get_cpf_cnpj()
                imovel = atendimento.get_imovel()
                if imovel:
                    imovel = imovel.get_id()
                status = atendimento.get_status()
                if status:
                    status = atendimento.get_status().value
                cursor.execute(sql_query, (
                    imovel,
                    corretor,
                    cliente,
                    status
                ))
                conexao.commit()
                return True
        except Exception as e:
            erro = f"ERRO! Banco.cadastrar_atendimento: {e}"
            print(erro)
            return False

    def get_lista_atendimentos(self):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
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
            erro = f"ERRO! Banco.get_lista_atendimentos: {e}"
            print(erro)
            return []

    def get_anuncio_por_id(self, id_anuncio):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM anuncio
                        WHERE id_anuncio = ?
                    ''', (id_anuncio,))
                registro = cursor.fetchone()
                if not registro:
                    raise Exception(f"Não existe anúncio com id {id_anuncio}")
                anuncio = Anuncio.Anuncio()
                id_anuncio = registro[0]
                if id_anuncio:
                    id_anuncio = int(id_anuncio)
                descricao = registro[1]
                titulo = registro[2]
                anuncio.set_id(id_anuncio)
                anuncio.set_descricao(descricao)
                anuncio.set_titulo(titulo)
                mapa_anexos = self.get_lista_anexos_por_id_anuncio(id_anuncio)
                if mapa_anexos and mapa_anexos["Imagens"]:
                    anuncio.set_imagens(mapa_anexos["Imagens"])
                if mapa_anexos and mapa_anexos["Videos"]:
                    anuncio.set_videos(mapa_anexos["Videos"])
                if mapa_anexos and mapa_anexos["Documentos"] :
                    anuncio.set_anexos(mapa_anexos["Documentos"])
                return anuncio
        except Exception as e:
            erro = f"ERRO! Banco.get_anuncio_por_id: {e}"
            print(erro)
            return None

    def cadastrar_anexo(self, id_anuncio, blob, tipo):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                sql_query = f''' 
                    INSERT INTO midia_anuncio (id_anuncio, midia, tipo) 
                    VALUES(?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    id_anuncio, blob, tipo
                ))
                conexao.commit()
                return True
        except Exception as e:
            erro = f"ERRO! Banco.cadastrar_anexo: {e}"
            print(erro)
            return False

    def get_lista_anexos_por_id_anuncio(self, id_anuncio):
        try:

            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT * FROM midia_anuncio 
                        WHERE id_anuncio = ?
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
                        videos.append(blob)
                mapa = dict()
                mapa["Imagens"] = imagens
                mapa["Videos"] = videos
                mapa["Documentos"] = documentos
                return mapa
        except Exception as e:
            erro = f"ERRO! Banco.get_lista_anexos: {e}"
            print(erro)
            return []

    def get_condominio_por_id_endereco(self, id):
        try:

            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                                SELECT * FROM condominio 
                                WHERE id_endereco = ?
                            ''', (id,))
                registro = cursor.fetchone()
                if not registro:
                    raise Exception(
                        f"Não existe condominio com id_endereco {id}")
                id_condominio = int(registro[0])
                nome = registro[1]
                id_endereco = int(registro[2])
                endereco = self.get_endereco_por_id(id_endereco)
                condominio = Condominio.Condominio(nome, endereco)
                condominio.set_id(id_condominio)
                return condominio
        except Exception as e:
            erro = f"ERRO! Banco.get_condominio_por_id_endereco: {e}"
            print(erro)
            return None

    def get_condominio_por_id(self, id):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                                SELECT * FROM condominio 
                                WHERE id_condominio = ?
                            ''', (id,))
                registro = cursor.fetchone()
                if not registro:
                    raise Exception(
                        f"Não existe condominio com id {id}")
                id_condominio = int(registro[0])
                nome = registro[1]
                id_endereco = int(registro[2])
                endereco = self.get_endereco_por_id(id_endereco)
                condominio = Condominio.Condominio(nome, endereco)
                condominio.set_id(id_condominio)
                return condominio
        except Exception as e:
            erro = f"ERRO! Banco.get_condominio_por_id: {e}"
            print(erro)
            return None

    def verificar_endereco(self, endereco):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                sql = '''
                    SELECT * 
                    FROM endereco 
                    WHERE cep = ?
                    AND numero = ?;
                '''
                cursor.execute(
                    sql, (endereco.get_cep(), endereco.get_numero()))
                registro = cursor.fetchone()
                if not registro:
                    raise Exception(f"Não existe imóvel com este endereço")
                if registro:
                    id_endereco = int(registro[0])
                    rua = registro[1]
                    numero = registro[2]
                    if numero:
                        numero = int(numero)
                    bairro = registro[3]
                    cep = registro[4]
                    if cep:
                        cep = int(cep)
                    complemento = registro[5]
                    cidade = registro[6]
                    uf = registro[7]
                    endereco = Endereco.Endereco(
                        rua, bairro, cep, cidade, uf)
                    endereco.set_id(id_endereco)
                    endereco.set_numero(numero)
                    endereco.set_complemento(complemento)
                    return endereco
                else:
                    return None
        except Exception as e:
            erro = f"ERRO! Banco.verificar_endereco: {e}"
            print(erro)
            return None

    def verificar_usuario(self, username, senha):
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
                    data_nascimento = registro[8]
                    if data_nascimento:
                        data_nascimento = datetime.strptime(
                            data_nascimento, "%d-%m-%Y")
                    tipo = registro[9]
                    if tipo:
                        tipo = Usuario.Tipo(tipo)
                    usuario = Usuario.Usuario(
                        username, senha_hash_banco, email, nome, cpf_cnpj, tipo)
                    sql_query = f''' 
                                SELECT id_telefone FROM telefone_usuario 
                                WHERE id_usuario = ?
                                '''
                    cursor.execute(sql_query, (id_usuario,))
                    registros = cursor.fetchall()
                    telefones = []
                    if registros:
                        for id_telefone in registros:
                            sql_query = f''' 
                                    SELECT numero FROM telefone 
                                    WHERE id_telefone = ?
                                        '''
                            cursor.execute(sql_query, (id_telefone,))
                            registro = cursor.fetchone()
                    match tipo:
                        case Usuario.Tipo.CORRETOR:
                            cursor.execute(f'''
                                        SELECT creci FROM corretor 
                                        WHERE id_usuario = ?
                                    ''', (id_usuario,))
                            creci = cursor.fetchone()[0]
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
                                    ''', (id_usuario,))
                            salario = cursor.fetchone()[0]
                            if salario:
                                salario = float(salario)
                            usuario.set_salario(salario)
                        case Usuario.Tipo.GERENTE:
                            usuario = Gerente.Gerente(
                                username, senha_hash_banco, email, nome, cpf_cnpj)
                            cursor.execute(f'''
                                        SELECT salario FROM gerente 
                                        WHERE id_usuario = ?
                                    ''', (id_usuario,))
                            salario = cursor.fetchone()[0]
                            if salario:
                                salario = float(salario)
                            usuario.set_salario(salario)
                        case Usuario.Tipo.CLIENTE:
                            usuario = Cliente.Cliente(
                                username, senha_hash_banco, email, nome, cpf_cnpj)
                            # cursor.execute(f'''
                            #         SELECT * FROM cliente
                            #         WHERE id_usuario = ?
                            #     ''', (id_usuario,))
                            # registros = cursor.fetchone()
                    usuario.set_endereco(endereco)
                    usuario.set_data_nascimento(data_nascimento)
                    usuario.set_rg(rg)
                    usuario.set_id(id_usuario)
                    usuario.set_telefones(telefones)
                    return usuario
                else:
                    raise Exception("Senha errada!")

        except Exception as e:
            erro = f"ERRO! Banco.verificar_usuario: {e}"
            print(erro)
            return None

    def cadastrar_endereco(self, endereco):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
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
            erro = f"ERRO! Banco.cadastrar_endereco: {e}"
            print(erro)
            return False

    def cadastrar_condominio(self, condominio):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                endereco = condominio.get_endereco()
                if endereco:
                    endereco = condominio.get_endereco().get_id()
                sql_query = f''' 
                    INSERT INTO condominio (nome, id_endereco) 
                    VALUES(?, ?)
                    '''
                cursor.execute(sql_query, (
                    condominio.get_nome(),
                    endereco
                ))
                conexao.commit()
                return True
        except Exception as e:
            erro = f"ERRO! Banco.cadastrar_condominio: {e}"
            print(erro)
            return False

    def cadastrar_proprietario(self, proprietario):
        # TODO: cadastrar telefones
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()

                endereco = proprietario.get_endereco()
                if endereco:
                    endereco = endereco.get_id()
                data = proprietario.get_data_nascimento()
                if data:
                    data = data.strftime("%d-%m-%Y")
                sql_query = f''' 
                    INSERT INTO proprietario (email, nome, cpf_cnpj, rg, id_endereco, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    proprietario.get_email(),
                    proprietario.get_nome(),
                    proprietario.get_cpf_cnpj(),
                    proprietario.get_rg(),
                    endereco,
                    data
                ))
                id = cursor.lastrowid
                if proprietario.get_telefones():
                    for telefone in proprietario.get_telefones():
                        sql_query = f''' 
                            INSERT INTO telefone (numero) 
                            VALUES(?)
                            '''
                        cursor.execute(sql_query, (telefone,))
                        id_telefone = cursor.lastrowid
                        sql_query = f''' 
                            INSERT INTO telefone_proprietario (id_proprietario, id_telefone) 
                            VALUES(?, ?)
                            '''
                        cursor.execute(sql_query, (id, id_telefone))
                conexao.commit()
                return True
        except Exception as e:
            erro = f"ERRO! Banco.cadastrar_proprietario: {e}"
            print(erro)
            return False

    def cadastrar_anuncio(self, anuncio):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()

                sql_query = f''' 
                    INSERT INTO anuncio (descricao, titulo) 
                    VALUES(?, ?)
                    '''
                cursor.execute(sql_query, (
                    anuncio.get_descricao(),
                    anuncio.get_titulo(),
                ))
                conexao.commit()

                id_anuncio = cursor.lastrowid

                if anuncio.get_imagens():
                    for imagem in anuncio.get_imagens():
                        self.cadastrar_anexo(id_anuncio, imagem, "Imagem")

                if anuncio.get_videos():
                    for video in anuncio.get_videos():
                        self.cadastrar_anexo(id_anuncio, video, "Video")

                if anuncio.get_anexos():
                    for anexo in anuncio.get_anexos():
                        self.cadastrar_anexo(id_anuncio, anexo, "Documento")

                return cursor.lastrowid
        except Exception as e:
            erro = f"ERRO! Banco.cadastrar_anuncio: {e}"
            print(erro)
            return False

    def get_endereco_por_id(self, id):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:

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
                uf = registros[7]
                endereco = Endereco.Endereco(
                    rua, bairro, cep, cidade, uf)
                endereco.set_id(id_endereco)
                endereco.set_numero(numero)
                endereco.set_complemento(complemento)
                return endereco
        except Exception as e:
            erro = f"ERRO! Banco.get_endereco_por_id: {e}"
            print(erro)
            return None

    def get_proprietario_por_cpf_cnpj(self, cpf_cnpj):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:

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
                data_nascimento = registro[5]
                if data_nascimento:
                    data_nascimento = datetime.strptime(
                        data_nascimento, "%d-%m-%Y")
                proprietario = Proprietario.Proprietario(email, nome, cpf_cnpj)
                proprietario.set_id(id_proprietario)
                proprietario.set_data_nascimento(data_nascimento)
                proprietario.set_rg(rg)
                return proprietario
        except Exception as e:
            erro = f"ERRO! Banco.get_proprietario_por_cpf_cnpj: {e}"
            print(erro)
            return None

    def get_imovel_por_id(self, id):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    f'SELECT * FROM imovel WHERE id_imovel = ?', (id,))
                dados = cursor.fetchone()
                if not dados:
                    raise Exception(f"Não existe imóvel com id {id}")
                id_imovel = int(dados[0])
                valor_venda = dados[1]
                if valor_venda:
                    valor_venda = float(valor_venda)
                valor_aluguel = dados[2]
                if valor_aluguel:
                    valor_aluguel = float(valor_aluguel)
                quant_quartos = dados[3]
                if quant_quartos:
                    quant_quartos = int(quant_quartos)
                quant_salas = dados[4]
                if quant_salas:
                    quant_salas = int(quant_salas)
                quant_vagas = dados[5]
                if quant_vagas:
                    quant_vagas = int(quant_vagas)
                quant_banheiros = dados[6]
                if quant_banheiros:
                    quant_banheiros = int(quant_banheiros)
                quant_varandas = dados[7]
                if quant_varandas:
                    quant_varandas = int(quant_varandas)
                categoria = dados[8]
                if categoria:
                    categoria = Imovel.Categoria(categoria)
                id_endereco = dados[9]
                endereco = None
                if id_endereco:
                    endereco = self.get_endereco_por_id(int(id_endereco))
                status = dados[10]
                if status:
                    status = Imovel.Status(status)
                iptu = dados[11]
                if iptu:
                    iptu = float(iptu)
                valor_condominio = dados[12]
                if valor_condominio:
                    valor_condominio = float(valor_condominio)
                andar = dados[13]
                if andar:
                    andar = int(andar)
                estado = dados[14]
                if estado:
                    estado = Imovel.Estado(estado)
                bloco = dados[15]
                ano_construcao = dados[16]
                if ano_construcao:
                    ano_construcao = int(ano_construcao)
                area_total = dados[17]
                if area_total:
                    area_total = float(area_total)
                area_privativa = dados[18]
                if area_privativa:
                    area_privativa = float(area_privativa)
                situacao = dados[19]
                if situacao:
                    situacao = Imovel.Situacao(situacao)
                ocupacao = dados[20]
                if ocupacao:
                    ocupacao = Imovel.Ocupacao(ocupacao)
                cpf_cnpj_corretor = dados[21]
                corretor = None
                if cpf_cnpj_corretor:
                    corretor = self.get_usuario_por_cpf(cpf_cnpj_corretor)
                cpf_cnpj_captador = dados[22]
                captador = None
                if cpf_cnpj_captador:
                    captador = self.get_usuario_por_cpf(cpf_cnpj_captador)
                data_cadastro = dados[23]
                if data_cadastro:
                    data_cadastro = datetime.strptime(
                        data_cadastro, "%d-%m-%Y")
                data_modificacao = dados[24]
                if data_modificacao:
                    data_modificacao = datetime.strptime(
                        data_modificacao, "%d-%m-%Y")
                id_anuncio = dados[25]
                anuncio = None
                if id_anuncio:
                    anuncio = self.get_anuncio_por_id(int(id_anuncio))

                id_condominio = dados[26]
                condominio = None
                if id_condominio:
                    condominio = self.get_condominio_por_id(int(id_condominio))
                imovel = Imovel.Imovel(endereco, status, categoria)
                imovel.set_id(id_imovel)
                imovel.set_valor_venda(valor_venda)
                imovel.set_valor_aluguel(valor_aluguel)
                imovel.set_quant_quartos(quant_quartos)
                imovel.set_quant_salas(quant_salas)
                imovel.set_quant_vagas(quant_vagas)
                imovel.set_quant_banheiros(quant_banheiros)
                imovel.set_quant_varandas(quant_varandas)
                imovel.set_categoria(categoria)
                imovel.set_endereco(endereco)
                imovel.set_status(status)
                imovel.set_iptu(iptu)
                imovel.set_valor_condominio(valor_condominio)
                imovel.set_andar(andar)
                imovel.set_estado(estado)
                imovel.set_bloco(bloco)
                imovel.set_ano_construcao(ano_construcao)
                imovel.set_area_total(area_total)
                imovel.set_area_privativa(area_privativa)
                imovel.set_situacao(situacao)
                imovel.set_ocupacao(ocupacao)
                imovel.set_corretor(corretor)
                imovel.set_captador(captador)
                imovel.set_data_cadastro(data_cadastro)
                imovel.set_data_modificacao(data_modificacao)
                imovel.set_anuncio(anuncio)
                imovel.set_condominio(condominio)

                cursor.execute(f'''
                            SELECT cpf_cnpj_proprietario FROM proprietario_imovel 
                            WHERE id_imovel = ?
                        ''', (id_imovel,))
                cpf_cnpj_proprietarios = cursor.fetchall()

                proprietarios = []

                if cpf_cnpj_proprietarios:
                    for cpf_cnpj in registros_imovel_filtros:
                        cpf_cnpj = cpf_cnpj[0]
                        proprietario = self.get_proprietario_por_cpf_cnpj(
                            cpf_cnpj)
                        if proprietario:
                            proprietarios.append(proprietario)

                imovel.set_proprietarios(proprietarios)

                cursor.execute(f'''
                    SELECT * FROM imovel_filtros 
                    WHERE id_imovel = ?
                ''', (id_imovel,))
                registros_imovel_filtros = cursor.fetchall()
                filtros = []

                if registros_imovel_filtros:
                    for registro in registros_imovel_filtros:
                        id_filtros_imovel = int(registro[0])
                        id_imovel = int(registro[1])
                        cursor.execute(f'''
                                SELECT nome FROM filtros_imovel 
                                WHERE id_filtros_imovel = ?
                            ''', (id_filtros_imovel,))
                        nome_filtro = cursor.fetchone()
                        if nome_filtro:
                            filtros.append(nome_filtro)

                imovel.set_filtros(filtros)
                return imovel
        except Exception as e:
            erro = f"ERRO! Banco.get_imovel_por_id: {e}"
            print(erro)
            return None

    def cadastrar_imovel(self, imovel):
        try:

            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                sql_query = ''' 
                INSERT INTO imovel(valor_venda, valor_aluguel, quant_quartos, quant_salas, quant_vagas, quant_banheiros, quant_varandas, categoria, id_endereco, status, iptu, valor_condominio, andar, estado, bloco, ano_construcao, area_total, area_privativa, situacao, ocupacao, cpf_cnpj_corretor, cpf_cnpj_captador, data_cadastro, data_modificacao, id_anuncio, id_condominio) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    '''

                if imovel.get_filtros():
                    for filtro in imovel.get_filtros():
                        id = self.get_id_filtro_imovel_por_nome(filtro)
                        if id is not None:
                            self.cadastrar_filtro_imovel(
                                imovel.get_id(), filtro)

                categoria = imovel.get_categoria()
                if categoria:
                    categoria = categoria.value

                endereco = imovel.get_endereco()
                if endereco:
                    if endereco.get_id() != None:
                        endereco = endereco.get_id()
                    else:
                        endereco = None

                anuncio = imovel.get_anuncio()
                if anuncio:
                    if anuncio.get_id() != None:
                        anuncio = anuncio.get_id()
                    else:
                        anuncio = None

                if imovel.get_proprietarios():
                    for proprietario in imovel.get_proprietarios():
                        sql_query = f'''
                                    INSERT INTO proprietario_imovel (cpf_cnpj_proprietario, id_imovel)
                                    VALUES(?, ?)
                                    '''
                        cursor.execute(sql_query, (proprietario.get_cpf_cnpj(),
                                                   imovel.get_id()))

                status = imovel.get_status()
                if status:
                    status = status.value

                estado = imovel.get_estado()
                if estado:
                    estado = estado.value

                situacao = imovel.get_situacao()
                if situacao:
                    situacao = situacao.value

                ocupacao = imovel.get_ocupacao()
                if ocupacao:
                    ocupacao = ocupacao.value

                corretor = imovel.get_corretor()
                if corretor:
                    corretor = corretor.get_cpf_cnpj()

                captador = imovel.get_captador()
                if captador:
                    captador = captador.get_cpf_cnpj()

                condominio = imovel.get_condominio()
                if condominio:
                    condominio = condominio.get_id()

                data_cadastro = imovel.get_data_cadastro()
                if data_cadastro and isinstance(data_cadastro, datetime):
                    data_cadastro = data_cadastro.strftime("%d-%m-%Y")

                data_modificacao = imovel.get_data_modificacao()
                if data_modificacao and isinstance(data_modificacao, datetime):
                    data_modificacao = data_modificacao.strftime("%d-%m-%Y")

                cursor.execute(sql_query, (
                    imovel.get_valor_venda(),
                    imovel.get_valor_aluguel(),
                    imovel.get_quant_quartos(),
                    imovel.get_quant_salas(),
                    imovel.get_quant_vagas(),
                    imovel.get_quant_banheiros(),
                    imovel.get_quant_varandas(),
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
                    corretor,
                    captador,
                    data_cadastro,
                    data_modificacao,
                    anuncio,
                    condominio
                ))
                conexao.commit()
                return True
        except Exception as e:
            erro = f"ERRO! Banco.cadastrar_imovel: {e}"
            print(erro)
            return False

    def get_lista_imoveis(self):

        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:

                cursor = conexao.cursor()
                lista = []
                cursor.execute("SELECT * FROM imovel")
                resultados = cursor.fetchall()
                if not resultados:
                    raise Exception(f"Não há imóveis cadastrados")
                for dados in resultados:
                    id_imovel = int(dados[0])
                    valor_venda = dados[1]
                    if valor_venda:
                        valor_venda = float(valor_venda)
                    valor_aluguel = dados[2]
                    if valor_aluguel:
                        valor_aluguel = float(valor_aluguel)
                    quant_quartos = dados[3]
                    if quant_quartos:
                        quant_quartos = int(quant_quartos)
                    quant_salas = dados[4]
                    if quant_salas:
                        quant_salas = int(quant_salas)
                    quant_vagas = dados[5]
                    if quant_vagas:
                        quant_vagas = int(quant_vagas)
                    quant_banheiros = dados[6]
                    if quant_banheiros:
                        quant_banheiros = int(quant_banheiros)
                    quant_varandas = dados[7]
                    if quant_varandas:
                        quant_varandas = int(quant_varandas)

                    categoria = dados[8]
                    if categoria:
                        categoria = Imovel.Categoria(categoria)

                    id_endereco = dados[9]
                    endereco = None
                    if id_endereco:
                        endereco = self.get_endereco_por_id(int(id_endereco))

                    status = dados[10]
                    if status:
                        status = Imovel.Status(status)
                    iptu = dados[11]
                    if iptu:
                        iptu = float(iptu)
                    valor_condominio = dados[12]
                    if valor_condominio:
                        valor_condominio = float(valor_condominio)
                    andar = dados[13]
                    if andar:
                        andar = int(andar)
                    estado = dados[14]
                    if estado:
                        estado = Imovel.Estado(estado)
                    bloco = dados[15]
                    ano_construcao = dados[16]
                    if ano_construcao:
                        ano_construcao = int(ano_construcao)
                    area_total = dados[17]
                    if area_total:
                        area_total = float(area_total)
                    area_privativa = dados[18]
                    if area_privativa:
                        area_privativa = float(area_privativa)
                    situacao = dados[19]
                    if situacao:
                        situacao = Imovel.Situacao(situacao)
                    ocupacao = dados[20]
                    if ocupacao:
                        ocupacao = Imovel.Ocupacao(ocupacao)
                    cpf_cnpj_corretor = dados[21]
                    corretor = None
                    if cpf_cnpj_corretor:
                        corretor = self.get_usuario_por_cpf(cpf_cnpj_corretor)
                    cpf_cnpj_captador = dados[22]
                    captador = None
                    if cpf_cnpj_captador:
                        captador = self.get_usuario_por_cpf(cpf_cnpj_captador)
                    data_cadastro = dados[23]
                    if data_cadastro:
                        data_cadastro = datetime.strptime(
                            data_cadastro, "%d-%m-%Y")
                    data_modificacao = dados[24]
                    if data_modificacao:
                        data_modificacao = datetime.strptime(
                            data_modificacao, "%d-%m-%Y")
                    id_anuncio = dados[25]
                    anuncio = None
                    if id_anuncio:
                        anuncio = self.get_anuncio_por_id(int(id_anuncio))
                    id_condominio = dados[26]
                    condominio = None
                    if id_condominio:
                        condominio = self.get_condominio_por_id(
                            int(id_condominio))

                    imovel = Imovel.Imovel(endereco, status, categoria)
                    imovel.set_id(id_imovel)
                    imovel.set_valor_venda(valor_venda)
                    imovel.set_valor_aluguel(valor_aluguel)
                    imovel.set_quant_quartos(quant_quartos)
                    imovel.set_quant_salas(quant_salas)
                    imovel.set_quant_vagas(quant_vagas)
                    imovel.set_quant_banheiros(quant_banheiros)
                    imovel.set_quant_varandas(quant_varandas)
                    imovel.set_categoria(categoria)
                    imovel.set_endereco(endereco)
                    imovel.set_status(status)
                    imovel.set_iptu(iptu)
                    imovel.set_valor_condominio(valor_condominio)
                    imovel.set_andar(andar)
                    imovel.set_estado(estado)
                    imovel.set_bloco(bloco)
                    imovel.set_ano_construcao(ano_construcao)
                    imovel.set_area_total(area_total)
                    imovel.set_area_privativa(area_privativa)
                    imovel.set_situacao(situacao)
                    imovel.set_ocupacao(ocupacao)
                    imovel.set_corretor(corretor)
                    imovel.set_captador(captador)
                    imovel.set_data_cadastro(data_cadastro)
                    imovel.set_data_modificacao(data_modificacao)
                    imovel.set_anuncio(anuncio)
                    imovel.set_condominio(condominio)

                    cursor.execute(f'''
                            SELECT cpf_cnpj_proprietario FROM proprietario_imovel 
                            WHERE id_imovel = ?
                        ''', (id_imovel,))
                    cpf_cnpj_proprietarios = cursor.fetchall()

                    proprietarios = []

                    if cpf_cnpj_proprietarios:
                        for cpf_cnpj in registros_imovel_filtros:
                            cpf_cnpj = cpf_cnpj[0]
                            proprietario = self.get_proprietario_por_cpf_cnpj(
                                cpf_cnpj)
                            if proprietario:
                                proprietarios.append(proprietario)

                    imovel.set_proprietarios(proprietarios)

                    cursor.execute(f'''
                        SELECT * FROM imovel_filtros 
                        WHERE id_imovel = ?
                    ''', (id_imovel,))
                    registros_imovel_filtros = cursor.fetchall()

                    filtros = []

                    if registros_imovel_filtros:
                        for registro in registros_imovel_filtros:
                            id_filtros_imovel = int(registro[0])
                            id_imovel = int(registro[1])
                            cursor.execute(f'''
                                SELECT nome FROM filtros_imovel 
                                WHERE id_filtros_imovel = ?
                            ''', (id_filtros_imovel,))
                            nome_filtro = cursor.fetchone()
                            if nome_filtro:
                                filtros.append(nome_filtro)

                    imovel.set_filtros(filtros)
                    lista.append(imovel)

                return lista
        except Exception as e:
            erro = f"ERRO! Banco.get_lista_imoveis: {e}"
            print(erro)
            return []

    def get_lista_imoveis_disponiveis(self):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                lista = []
                cursor.execute(
                    "SELECT * FROM imovel WHERE status IN ('Venda', 'Aluguel', 'venda_aluguel')")
                resultados = cursor.fetchall()
                if not resultados:
                    raise Exception(f"Não há imóveis disponiveis")
                for dados in resultados:
                    id_imovel = int(dados[0])
                    valor_venda = dados[1]
                    if valor_venda:
                        valor_venda = float(valor_venda)
                    valor_aluguel = dados[2]
                    if valor_aluguel:
                        valor_aluguel = float(valor_aluguel)
                    quant_quartos = dados[3]
                    if quant_quartos:
                        quant_quartos = int(quant_quartos)
                    quant_salas = dados[4]
                    if quant_salas:
                        quant_salas = int(quant_salas)
                    quant_vagas = dados[5]
                    if quant_vagas:
                        quant_vagas = int(quant_vagas)
                    quant_banheiros = dados[6]
                    if quant_banheiros:
                        quant_banheiros = int(quant_banheiros)
                    quant_varandas = dados[7]
                    if quant_varandas:
                        quant_varandas = int(quant_varandas)

                    categoria = dados[8]
                    if categoria:
                        categoria = Imovel.Categoria(categoria)

                    id_endereco = dados[9]
                    endereco = None
                    if id_endereco:
                        endereco = self.get_endereco_por_id(int(id_endereco))

                    status = dados[10]
                    if status:
                        status = Imovel.Status(status)
                    iptu = dados[11]
                    if iptu:
                        iptu = float(iptu)
                    valor_condominio = dados[12]
                    if valor_condominio:
                        valor_condominio = float(valor_condominio)
                    andar = dados[13]
                    if andar:
                        andar = int(andar)
                    estado = dados[14]
                    if estado:
                        estado = Imovel.Estado(estado)
                    bloco = dados[15]
                    ano_construcao = dados[16]
                    if ano_construcao:
                        ano_construcao = int(ano_construcao)
                    area_total = dados[17]
                    if area_total:
                        area_total = float(area_total)
                    area_privativa = dados[18]
                    if area_privativa:
                        area_privativa = float(area_privativa)
                    situacao = dados[19]
                    if situacao:
                        situacao = Imovel.Situacao(situacao)
                    ocupacao = dados[20]
                    if ocupacao:
                        ocupacao = Imovel.Ocupacao(ocupacao)
                    cpf_cnpj_corretor = dados[21]
                    corretor = None
                    if cpf_cnpj_corretor:
                        corretor = self.get_usuario_por_cpf(cpf_cnpj_corretor)
                    cpf_cnpj_captador = dados[22]
                    captador = None
                    if cpf_cnpj_captador:
                        captador = self.get_usuario_por_cpf(cpf_cnpj_captador)
                    data_cadastro = dados[23]
                    if data_cadastro:
                        data_cadastro = datetime.strptime(
                            data_cadastro, "%d-%m-%Y")
                    data_modificacao = dados[24]
                    if data_modificacao:
                        data_modificacao = datetime.strptime(
                            data_modificacao, "%d-%m-%Y")
                    id_anuncio = dados[25]
                    anuncio = None
                    if id_anuncio:
                        anuncio = self.get_anuncio_por_id(int(id_anuncio))

                    id_condominio = dados[26]
                    condominio = None
                    if id_condominio:
                        condominio = self.get_condominio_por_id(
                            int(id_condominio))

                    imovel = Imovel.Imovel(endereco, status, categoria)
                    imovel.set_id(id_imovel)
                    imovel.set_valor_venda(valor_venda)
                    imovel.set_valor_aluguel(valor_aluguel)
                    imovel.set_quant_quartos(quant_quartos)
                    imovel.set_quant_salas(quant_salas)
                    imovel.set_quant_vagas(quant_vagas)
                    imovel.set_quant_banheiros(quant_banheiros)
                    imovel.set_quant_varandas(quant_varandas)
                    imovel.set_categoria(categoria)
                    imovel.set_endereco(endereco)
                    imovel.set_status(status)
                    imovel.set_iptu(iptu)
                    imovel.set_valor_condominio(valor_condominio)
                    imovel.set_andar(andar)
                    imovel.set_estado(estado)
                    imovel.set_bloco(bloco)
                    imovel.set_ano_construcao(ano_construcao)
                    imovel.set_area_total(area_total)
                    imovel.set_area_privativa(area_privativa)
                    imovel.set_situacao(situacao)
                    imovel.set_ocupacao(ocupacao)
                    imovel.set_corretor(corretor)
                    imovel.set_captador(captador)
                    imovel.set_data_cadastro(data_cadastro)
                    imovel.set_data_modificacao(data_modificacao)
                    imovel.set_anuncio(anuncio)
                    imovel.set_condominio(condominio)

                    cursor.execute(f'''
                            SELECT cpf_cnpj_proprietario FROM proprietario_imovel 
                            WHERE id_imovel = ?
                        ''', (id_imovel,))
                    cpf_cnpj_proprietarios = cursor.fetchall()

                    proprietarios = []

                    if cpf_cnpj_proprietarios:
                        for cpf_cnpj in registros_imovel_filtros:
                            cpf_cnpj = cpf_cnpj[0]
                            proprietario = self.get_proprietario_por_cpf_cnpj(
                                cpf_cnpj)
                            if proprietario:
                                proprietarios.append(proprietario)

                    imovel.set_proprietarios(proprietarios)

                    cursor.execute(f'''
                            SELECT * FROM imovel_filtros 
                            WHERE id_imovel = ?
                        ''', (id_imovel,))
                    registros_imovel_filtros = cursor.fetchall()

                    filtros = []

                    if registros_imovel_filtros:
                        for registro in registros_imovel_filtros:
                            id_filtros_imovel = int(registro[0])
                            id_imovel = int(registro[1])
                            cursor.execute(f'''
                                SELECT nome FROM filtros_imovel 
                                WHERE id_filtros_imovel = ?
                            ''', (id_filtros_imovel,))
                            nome_filtro = cursor.fetchone()
                            if nome_filtro:
                                filtros.append(nome_filtro)

                    imovel.set_filtros(filtros)
                    lista.append(imovel)
                return lista
        except Exception as e:
            erro = f"ERRO! Banco.get_lista_imoveis_disponiveis: {e}"
            print(erro)
            return []

    def atualizar_imovel(self, imovel: Imovel.Imovel):
        try:

            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()

                categoria = imovel.get_categoria()
                if categoria:
                    categoria = categoria.value

                endereco = imovel.get_endereco()
                if endereco:
                    if endereco.get_id() != None:
                        endereco = endereco.get_id()
                    else:
                        endereco = None

                anuncio = imovel.get_anuncio()
                if anuncio:
                    if anuncio.get_id() != None:
                        anuncio = anuncio.get_id()
                    else:
                        anuncio = None

                imovel_consultado = self.get_imovel_por_id(imovel.get_id())
                if imovel_consultado.get_proprietarios():
                    for proprietario in imovel_consultado.get_proprietarios():
                        if proprietario not in imovel.get_proprietarios():
                            sql_query = f'''
                                            DELETE FROM proprietario_imovel
                                            WHERE cpf_cnpj_proprietario = ?;
                                            '''
                            cursor.execute(
                                sql_query, (proprietario.get_cpf_cnpj(),))
                    for proprietario in imovel.get_proprietarios():
                        if proprietario not in imovel_consultado.get_proprietarios():
                            sql_query = f'''
                                                    INSERT INTO proprietario_imovel (cpf_cnpj_proprietario, id_imovel)
                                                    VALUES(?, ?)
                                                    '''
                            cursor.execute(
                                sql_query, (proprietario.get_cpf_cnpj(), imovel.get_id()))

                elif imovel.get_proprietarios():
                    for proprietario in imovel.get_proprietarios():
                        sql_query = f'''
                                            INSERT INTO proprietario_imovel (cpf_cnpj_proprietario, id_imovel)
                                            VALUES(?, ?)
                                            '''
                        cursor.execute(
                            sql_query, (proprietario.get_cpf_cnpj(), imovel.get_id()))

                status = imovel.get_status()
                if status:
                    status = status.value

                estado = imovel.get_estado()
                if estado:
                    estado = estado.value

                situacao = imovel.get_situacao()
                if situacao:
                    situacao = situacao.value

                ocupacao = imovel.get_ocupacao()
                if ocupacao:
                    ocupacao = ocupacao.value

                condominio = imovel.get_condominio()
                if condominio:
                    condominio = condominio.get_id()

                corretor = imovel.get_corretor()
                if corretor:
                    corretor = corretor.get_cpf_cnpj()

                captador = imovel.get_captador()
                if captador:
                    captador = captador.get_cpf_cnpj()

                data_cadastro = imovel.get_data_cadastro()
                if data_cadastro and isinstance(data_cadastro, datetime):
                    data_cadastro = data_cadastro.strftime("%d-%m-%Y")

                data_modificacao = imovel.get_data_modificacao()
                if data_modificacao and isinstance(data_modificacao, datetime):
                    data_modificacao = data_modificacao.strftime("%d-%m-%Y")

                imovel_consulta = self.get_imovel_por_id(imovel.get_id())

                if imovel_consulta.get_filtros() and imovel_consulta.get_filtros() != imovel.get_filtros():
                    for filtro in imovel_consulta.get_filtros():
                        if filtro not in imovel.get_filtros():
                            id = self.get_id_filtro_imovel_por_nome(filtro)
                            if id is not None:
                                self.remover_filtro_do_imovel(
                                    imovel.get_id(), id)
                    if imovel.get_filtros():
                        for filtro in imovel.get_filtros():
                            if filtro not in imovel_consulta.get_filtros():
                                id = self.get_id_filtro_imovel_por_nome(filtro)
                                if id is not None:
                                    self.cadastrar_filtro_imovel(
                                        imovel.get_id(), filtro)

                query = '''
                        UPDATE Imovel SET
                            valor_venda = ?,
                            valor_aluguel = ?,
                            quant_quartos = ?,
                            quant_salas = ?,
                            quant_vagas = ?,
                            quant_banheiros = ?,
                            quant_varandas = ?,
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
                            cpf_cnpj_corretor = ?,
                            cpf_cnpj_captador = ?,
                            data_cadastro = ?,
                            data_modificacao = ?,
                            id_anuncio = ?,
                            id_condominio = ?
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
                    corretor,
                    captador,
                    data_cadastro,
                    data_modificacao,
                    anuncio,
                    condominio,
                    imovel.get_id()
                )

                cursor.execute(query, valores)
                conexao.commit()
                return True
        except Exception as e:
            erro = f"ERRO! Banco.atualizar_imovel: {e}"
            print(erro)
            return False

    def get_id_filtro_imovel_por_nome(self, nome):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT id_filtros_imovel FROM filtros_imovel 
                        WHERE nome = ?
                    ''', (nome,))
                id = cursor.fetchone()[0]
                return id
        except Exception as e:
            print(f"ERRO! Banco.get_id_filtro_imovel_por_nome: {e}")
            return None

    def cadastrar_filtro_imovel(self, id_imovel, id_filtro):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        INSERT INTO imovel_filtros (id_filtros_imovel, id_imovel)
                        VALUES(?, ?)
                    ''', (id_imovel, id_filtro))
                return True
        except Exception as e:
            print(f"ERRO! Banco.cadastrar_filtro_imovel: {e}")
            return False

    def remover_filtro_do_imovel(self, id_imovel, id_filtro):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                      DELETE FROM imovel_filtros
                    WHERE id_imovel = ? AND id_filtros_imovel = ?;
                    ''', (id_imovel, id_filtro))
        except Exception as e:
            print(f"ERRO! Banco.remover_filtro_do_imovel: {e}")
            return False

    def get_id_filtro_condominio_por_nome(self, nome):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        SELECT id_filtros_condominio FROM filtros_condominio 
                        WHERE nome = ?
                    ''', (nome,))
                id = cursor.fetchone()[0]
                return id
        except Exception as e:
            print(f"ERRO! Banco.get_id_filtro_condominio_por_nome: {e}")
            return None

    def cadastrar_filtro_condominio(self, id_condominio, id_filtro):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                        INSERT INTO condominio_filtros (id_filtros_condominio, id_condominio)
                        VALUES(?, ?)
                    ''', (id_condominio, id_filtro))
                return True
        except Exception as e:
            print(f"ERRO! Banco.cadastrar_filtro_condominio: {e}")
            return False

    def remover_filtro_do_condominio(self, id_condominio, id_filtro):
        try:
            with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()
                cursor.execute(f'''
                      DELETE FROM condominio_filtros
                    WHERE id_condominio = ? AND id_filtros_condominio = ?;
                    ''', (id_condominio, id_filtro))
        except Exception as e:
            print(f"ERRO! Banco.remover_filtro_do_condominio: {e}")
            return False

    def atualizar_anuncio(self, anuncio):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()

                query = '''
                        UPDATE anuncio SET
                            descricao = ?,
                            titulo = ?
                        WHERE id_anuncio = ?;
                    '''

                valores = (
                    anuncio.get_descricao(),
                    anuncio.get_titulo(),
                    anuncio.get_id()
                )

                cursor.execute(query, valores)

                anuncio_consulta = self.get_anuncio_por_id(anuncio.get_id())

                # if anuncio_consulta.get_imagens() and anuncio_consulta.get_imagens() != anuncio.get_imagens():
                #     for filtro in anuncio_consulta.get_imagens():
                #         if filtro not in anuncio.get_imagens():
                #             id = self.get_id_filtro_condominio_por_nome(filtro)
                #             if id is not None:
                #                 self.remover_filtro_do_condominio(
                #                     anuncio.get_id(), id)
                #     if anuncio.get_imagens():
                #         for filtro in anuncio.get_imagens():
                #             if filtro not in anuncio_consulta.get_imagens():
                #                 id = self.get_id_filtro_condominio_por_nome(filtro)
                #                 if id is not None:
                #                     self.cadastrar_filtro_condominio(
                #                         anuncio.get_id(), filtro)

                # if anuncio_consulta.get_videos() and anuncio_consulta.get_videos() != anuncio.get_videos():
                #     for filtro in anuncio_consulta.get_videos():
                #         if filtro not in anuncio.get_videos():
                #             id = self.get_id_filtro_condominio_por_nome(filtro)
                #             if id is not None:
                #                 self.remover_filtro_do_condominio(
                #                     anuncio.get_id(), id)
                #     if anuncio.get_videos():
                #         for filtro in anuncio.get_videos():
                #             if filtro not in anuncio_consulta.get_videos():
                #                 id = self.get_id_filtro_condominio_por_nome(filtro)
                #                 if id is not None:
                #                     self.cadastrar_filtro_condominio(
                #                         anuncio.get_id(), filtro)

                # if anuncio_consulta.get_anexos() and anuncio_consulta.get_anexos() != anuncio.get_anexos():
                #     for filtro in anuncio_consulta.get_anexos():
                #         if filtro not in anuncio.get_anexos():
                #             id = self.get_id_filtro_condominio_por_nome(filtro)
                #             if id is not None:
                #                 self.remover_filtro_do_condominio(
                #                     anuncio.get_id(), id)
                #     if anuncio.get_anexos():
                #         for filtro in anuncio.get_anexos():
                #             if filtro not in anuncio_consulta.get_anexos():
                #                 id = self.get_id_filtro_condominio_por_nome(filtro)
                #                 if id is not None:
                #                     self.cadastrar_filtro_condominio(
                #                         anuncio.get_id(), filtro)

                conexao.commit()
                return True
        except Exception as e:
            erro = f"ERRO! Banco.atualizar_imovel: {e}"
            print(erro)
            return False

    def atualizar_condominio(self, condominio):
        try:
            with sqlite3.connect(
                    "data\\Imobiliaria.db", check_same_thread=False) as conexao:
                cursor = conexao.cursor()

                query = '''
                        UPDATE condominio SET
                            nome = ?
                        WHERE id_condominio = ?;
                    '''

                valores = (
                    condominio.get_nome(),
                    condominio.get_id()
                )

                cursor.execute(query, valores)

                condominio_consulta = self.get_condominio_por_id(
                    condominio.get_id())

                if condominio_consulta.get_filtros() and condominio_consulta.get_filtros() != condominio.get_filtros():
                    for filtro in condominio_consulta.get_filtros():
                        if filtro not in condominio.get_filtros():
                            id = self.get_id_filtro_condominio_por_nome(filtro)
                            if id is not None:
                                self.remover_filtro_do_condominio(
                                    condominio.get_id(), id)
                    if condominio.get_filtros():
                        for filtro in condominio.get_filtros():
                            if filtro not in condominio_consulta.get_filtros():
                                id = self.get_id_filtro_condominio_por_nome(
                                    filtro)
                                if id is not None:
                                    self.cadastrar_filtro_condominio(
                                        condominio.get_id(), filtro)

                conexao.commit()
                return True
        except Exception as e:
            erro = f"ERRO! Banco.atualizar_condominio: {e}"
            print(erro)
            return False

    def atualizar_usuario(self, usuario):
        # TODO: atualizar telefones
        try:
            with sqlite3.connect(f"data/Imobiliaria.db") as conexao:
                cursor = conexao.cursor()
                sql_update_query = f"""
                UPDATE usuario
                SET username = ?,
                    senha = ?,
                    email = ?,
                    nome = ?,
                    cpf_cnpj = ?,
                    rg = ?,
                    id_endereco = ?,
                    data_nascimento = ?,
                    tipo_usuario = ?
                WHERE cpf_cnpj = ?;
                """
                endereco = usuario.get_endereco()
                if endereco:
                    endereco = endereco.get_id()

                data_nascimento = usuario.get_data_nascimento()
                if data_nascimento:
                    data_nascimento = data_nascimento.strftime("%d-%m-%Y")
                tipo_usuario = usuario.get_tipo()
                if tipo_usuario:
                    tipo_usuario = tipo_usuario.value

                senha_hash = hashlib.sha256(
                    usuario.get_senha().encode('utf-8')).hexdigest()

                dados = (usuario.get_username(), senha_hash, usuario.get_email(), usuario.get_nome(),
                         usuario.get_cpf_cnpj(), usuario.get_rg(),
                         endereco, data_nascimento, tipo_usuario, usuario.get_cpf_cnpj()
                         )
                cursor.execute(sql_update_query, dados)

                usuario_consulta = self.get_usuario_por_cpf_cnpj(
                    usuario.get_cpf_cnpj())

                if usuario_consulta.get_telefones() and usuario_consulta.get_telefones() != usuario.get_telefones():
                    for telefone in usuario_consulta.get_telefones():
                        if telefone not in usuario.get_telefones():

                            cursor.execute(f"""
                            SELECT id_telefone FROM telefone
                            WHERE numero = ?;
                            """, (telefone,))

                            id = cursor.fetchone()[0]

                            cursor.execute(f"""
                            DELETE FROM telefone
                            WHERE numero = ?;
                            """, (telefone,))

                            sql_delete_query = f"""
                            DELETE FROM telefone_usuario
                            WHERE id_telefone = ?;
                            """
                            cursor.execute(sql_delete_query, (id,))

                    if usuario.get_telefones():
                        for telefone in usuario.get_telefones():
                            if telefone not in usuario_consulta.get_telefones():
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
                                cursor.execute(
                                    sql_query, (usuario.get_id(), id_telefone))

                    match usuario.get_tipo():
                        case Usuario.Tipo.CORRETOR:
                            cursor.execute(f'''
                                        UPDATE corretor
                                        SET creci = ?
                                        WHERE id_usuario = ?;
                                    ''', (usuario.get_creci(), usuario.get_id()))
                        case Usuario.Tipo.CAPTADOR:
                            cursor.execute(f'''
                                        UPDATE captador
                                        SET salario = ?
                                        WHERE id_usuario = ?;
                                    ''', (usuario.get_salario(), usuario.get_id()))
                        case Usuario.Tipo.GERENTE:
                            cursor.execute(f'''
                                        UPDATE gerente
                                        SET salario = ?
                                        WHERE id_usuario = ?;
                                    ''', (usuario.get_salario(), usuario.get_id()))
                        # case Usuario.Tipo.CLIENTE:
                        #     cursor.execute(f'''
                        #                 UPDATE cliente (id_usuario)
                        #                 WHERE id_usuario = ?;
                        #             ''', (id,))

                conexao.commit()
                return True
        except Exception as e:
            print(f"ERRO Banco.atualizar_usuario {e}")
            return False

    def atualizar_proprietario(self, proprietario):
        # TODO: atualizar telefones
        try:
            with sqlite3.connect(f"data/Imobiliaria.db") as conexao:
                cursor = conexao.cursor()
                sql_update_query = f"""
                UPDATE proprietario
                SET email = ?,
                    nome = ?,
                    cpf_cnpj = ?,
                    rg = ?,
                    id_endereco = ?,
                    data_nascimento = ?
                WHERE cpf_cnpj = ?;
                """
                endereco = proprietario.get_endereco()
                if endereco:
                    endereco = endereco.get_id()

                data_nascimento = proprietario.get_data_nascimento()
                if data_nascimento:
                    data_nascimento = data_nascimento.strftime("%d-%m-%Y")

                dados = (proprietario.get_email(), proprietario.get_nome(),
                         proprietario.get_cpf_cnpj(), proprietario.get_rg(),
                         endereco, data_nascimento, proprietario.get_cpf_cnpj()
                         )
                cursor.execute(sql_update_query, dados)

                proprietario_consulta = self.get_proprietario_por_cpf_cnpj(
                    proprietario.get_cpf_cnpj())

                if proprietario_consulta.get_telefones() and proprietario_consulta.get_telefones() != proprietario.get_telefones():
                    for telefone in proprietario_consulta.get_telefones():
                        if telefone not in proprietario.get_telefones():

                            cursor.execute(f"""
                            SELECT id_telefone FROM telefone
                            WHERE numero = ?;
                            """, (telefone,))

                            id = cursor.fetchone()[0]

                            cursor.execute(f"""
                            DELETE FROM telefone
                            WHERE numero = ?;
                            """, (telefone,))

                            sql_delete_query = f"""
                            DELETE FROM telefone_proprietario
                            WHERE id_telefone = ?;
                            """
                            cursor.execute(sql_delete_query, (id,))

                    if proprietario.get_telefones():
                        for telefone in proprietario.get_telefones():
                            if telefone not in proprietario_consulta.get_telefones():
                                sql_query = f''' 
                                    INSERT INTO telefone (numero) 
                                    VALUES(?)
                                    '''
                                cursor.execute(sql_query, (telefone,))
                                id_telefone = cursor.lastrowid
                                sql_query = f''' 
                                    INSERT INTO telefone_proprietario (id_usuario, id_telefone) 
                                    VALUES(?, ?)
                                    '''
                                cursor.execute(
                                    sql_query, (proprietario.get_id(), id_telefone))

                conexao.commit()
                return True
        except Exception as e:
            print(f"ERRO Banco.atualizar_proprietario {e}")
            return False
