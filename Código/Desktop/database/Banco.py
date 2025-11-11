import sqlite3
import hashlib
import os

from model import Cliente, Imovel, Administrador, Captador, Corretor


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
                    rua TEXT NOT NULL,
                    numero INTEGER NULL,
                    bairro TEXT NOT NULL,
                    cep INTEGER NULL,
                    complemento TEXT NULL,
                    cidade TEXT NOT NULL,
                    estado TEXT NOT NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Administrador (
                    id_administrador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    email TEXT NULL UNIQUE
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Comprador (
                    id_comprador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    email TEXT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NULL,
                    endereco TEXT NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Proprietario (
                    id_proprietario INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NULL,
                    endereco TEXT NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Captador (
                    id_captador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT NOT NULL,
                    turno TEXT NULL,
                    salario REAL NULL,
                    matricula TEXT NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Corretor (
                    id_corretor INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT NOT NULL,
                    turno TEXT NULL,
                    salario REAL NULL,
                    matricula TEXT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Imovel (
                    id_imovel INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT NOT NULL UNIQUE,
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
                    id_endereco INT NOT NULL,
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
                    cpf_proprietario TEXT NOT NULL,
                    cpf_corretor TEXT NOT NULL,
                    FOREIGN KEY (id_endereco) REFERENCES Endereco(id_endereco),
                    FOREIGN KEY (cpf_proprietario) REFERENCES Proprietario(cpf),
                    FOREIGN KEY (cpf_corretor) REFERENCES Corretor(cpf)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Midia_Imovel (
                    id_imovel INTEGER NOT NULL,
                    midia BLOB NOT NULL,
                    tipo TEXT NOT NULL,
                    FOREIGN KEY (id_imovel) references Imovel (id_imovel)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Venda_Aluguel (
                    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpf_cliente TEXT NOT NULL,
                    cpf_proprietario TEXT NOT NULL, 
                    cpf_captador TEXT NULL,
                    cpf_corretor TEXT NOT NULL,
                    data_venda TEXT NOT NULL,
                    id_imovel INTEGER NOT NULL,
                    comissao_captador REAL NULL,
                    comissao_corretor REAL NULL,
                    FOREIGN KEY (id_imovel) REFERENCES Imovel (id_imovel),
                    FOREIGN KEY (cpf_cliente) REFERENCES Cliente (cpf),
                    FOREIGN KEY (cpf_proprietario) references Proprietario (cpf),
                    FOREIGN KEY (cpf_corretor) references Corretor (cpf)
                    );
                                ''')

            conexao.commit()

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

                return registros, ""
            except Exception as e:
                erro = "Banco.get_lista_compradores: ERRO!", e
                return [], erro

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

                return registros, ""
            except Exception as e:
                erro = "Banco.get_lista_proprietarios: ERRO!", e
                return [], erro

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
                    return pessoa, ""
                else:
                    raise Exception("Senha errada!")

            except Exception as e:
                erro = "Banco.verificar_usuario: ERRO!", e
                return None, erro

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
                return True, ""
            except Exception as e:
                erro = f"Banco.cadastrar_endereco: ERRO! {e}"
                return False, erro

    def cadastrar_corretor(self, corretor):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                senha_hash = hashlib.sha256(
                    corretor.get_senha().encode('utf-8')).hexdigest()
                sql_query = f''' 
                    INSERT INTO Corretor (username, senha, email, nome, cpf, rg, telefone, endereco, idade, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    corretor.get_username(),
                    senha_hash,
                    corretor.get_email(),
                    corretor.get_nome(),
                    corretor.get_cpf(),
                    corretor.get_rg(),
                    corretor.get_telefone(),
                    corretor.get_endereco(),
                    corretor.get_idade(),
                    corretor.get_data_nascimento()
                ))
                conexao.commit()
                return True, ""
            except Exception as e:
                erro = f"Banco.cadastrar_corretor: ERRO! {e}"
                return False, erro

    def cadastrar_captador(self, captador):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                senha_hash = hashlib.sha256(
                    captador.get_senha().encode('utf-8')).hexdigest()
                sql_query = f''' 
                    INSERT INTO Captador (username, senha, email, nome, cpf, rg, telefone, endereco, idade, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                cursor.execute(sql_query, (
                    captador.get_username(),
                    senha_hash,
                    captador.get_email(),
                    captador.get_nome(),
                    captador.get_cpf(),
                    captador.get_rg(),
                    captador.get_telefone(),
                    captador.get_endereco(),
                    captador.get_idade(),
                    captador.get_data_nascimento()
                ))
                conexao.commit()
                return True, ""
            except Exception as e:
                erro = f"Banco.cadastrar_captador: ERRO! {e}"
                return False, erro

    def cadastrar_proprietario(self, proprietario):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                if isinstance(proprietario, Cliente.Proprietario):

                    sql_query = f''' 
                    INSERT INTO Proprietario (email, nome, cpf, rg, telefone, endereco, idade, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    cursor.execute(sql_query, (
                        proprietario.get_email(),
                        proprietario.get_nome(),
                        proprietario.get_cpf(),
                        proprietario.get_rg(),
                        proprietario.get_telefone(),
                        proprietario.get_endereco(),
                        proprietario.get_idade(),
                        proprietario.get_data_nascimento()
                    ))
                    conexao.commit()
                    return True, ""
            except Exception as e:
                erro = f"Banco.cadastrar_proprietario: ERRO! {e}"
                return False, erro

    def cadastrar_comprador(self, comprador):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                if isinstance(comprador, Cliente.Comprador):
                    senha_hash = hashlib.sha256(
                        comprador.get_senha().encode('utf-8')).hexdigest()
                    sql_query = f''' 
                    INSERT INTO Comprador (username, senha, email, nome, cpf, rg, telefone, endereco, idade, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    cursor.execute(sql_query, (
                        comprador.get_username(),
                        senha_hash,
                        comprador.get_email(),
                        comprador.get_nome(),
                        comprador.get_cpf(),
                        comprador.get_rg(),
                        comprador.get_telefone(),
                        comprador.get_endereco(),
                        comprador.get_idade(),
                        comprador.get_data_nascimento()
                    ))

                    conexao.commit()
                    return True, ""
            except Exception as e:
                erro = f"Banco.cadastrar_comprador: ERRO! {e}"
                return False, erro

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
                return True, ""
            except Exception as e:
                erro = f"Banco.remover_imovel: ERRO! {e}"
                return False, erro

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
                imovel = Imovel.Imovel(*registro[2:9])
                imovel.set_preco(float(imovel.get_preco()))
                imovel.set_quantidade(int(imovel.get_quantidade()))
                imovel.set_descricao(registro[-2])
                imovel.set_imagem(registro[-1])
                imovel.set_id(int(registro[0]))
                imovel.set_codigo(registro[1])
                return imovel
            except Exception as e:
                erro = f"Banco.get_imovel_por_id: ERRO! {e}"
                return None, erro

    def cadastrar_imovel(self, imovel):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO Imovel(codigo, valor_venda, valor_aluguel, quant_quartos, quant_salas, quant_vagas, quant_banheiros, quant_varandas, nome_condominio, cor, categoria, descricao, endereço, status, iptu, valor_condominio, andar, estado, numero, complemento, bloco, ano_construcao, area_total, area_privativa, bairro, rua, cidade, situacao, ocupacao, cpf_proprietario, cpf_corretor) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    '''
                cursor.execute(sql_query, (
                    imovel.get_codigo(),
                    imovel.get_valor_venda(),
                    imovel.get_valor_aluguel(),
                    imovel.get_quant_quartos(),
                    imovel.get_quant_salas(),
                    imovel.get_quant_vagas(),
                    imovel.get_quant_banheiros(),
                    imovel.get_quant_varandas(),
                    imovel.get_nome_condominio(),
                    imovel.get_cor(),
                    imovel.get_categoria(),
                    imovel.get_descricao(),
                    imovel.get_endereço(),
                    imovel.get_status(),
                    imovel.get_iptu(),
                    imovel.get_estado(),
                    imovel.get_valor_condominio(),
                    imovel.get_andar(),
                    imovel.get_estado(),
                    imovel.get_ano_construcao(),
                    imovel.get_area_total(),
                    imovel.get_area_privativa(),
                    imovel.get_situacao(),
                    imovel.get_ocupacao(),
                    imovel.get_cpf_proprietario(),
                    imovel.get_cpf_corretor(),
                ))
                conexao.commit()
                return True, ""
            except Exception as e:
                erro = f"Banco.cadastrar_imovel: ERRO! {e}"
                return False, erro

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
                    imovel = Imovel.Imovel(*dados[2:9])
                    imovel.set_preco(float(imovel.get_preco()))
                    imovel.set_quantidade(int(imovel.get_quantidade()))
                    imovel.set_descricao(dados[-2])
                    imovel.set_imagem(dados[-1])
                    imovel.set_id(int(dados[0]))
                    imovel.set_codigo(dados[1])
                    lista.append(imovel)
                return lista
            except Exception as e:
                erro = f"Banco.get_lista_imoveis: ERRO! {e}"
                return [], erro

    def get_lista_imoveis_disponiveis(self):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                lista = []
                cursor.execute("SELECT * FROM Imovel WHERE quantidade > 0")
                resultados = cursor.fetchall()
                if not resultados:
                    raise Exception(f"Tabela imovel esta vázia")
                for dados in resultados:
                    imovel = Imovel.Imovel(*dados[2:9])
                    imovel.set_codigo(dados[1])
                    imovel.set_valor_venda(float(dados[1]))
                    imovel.set_valor_aluguel(float(dados[1]))
                    imovel.set_quant_quartos(int(dados[1]))
                    imovel.set_quant_salas(int(dados[1]))
                    imovel.set_quant_vagas(int(dados[1]))
                    imovel.set_quant_banheiros(int(dados[1]))
                    imovel.set_quant_varandas(int(dados[1]))
                    imovel.set_nome_condominio(dados[1])
                    imovel.set_cor(dados[1])
                    imovel.set_categoria(dados[1])
                    imovel.set_descricao(dados[1])
                    imovel.set_endereço(dados[1])
                    imovel.set_status(dados[1])
                    imovel.set_iptu(float(dados[1]))
                    imovel.set_estado(dados[1])
                    imovel.set_valor_condominio(float(dados[1]))
                    imovel.set_andar(dados[1])
                    imovel.set_estado(dados[1])
                    imovel.set_ano_construcao(dados[1])
                    imovel.set_area_total(float(dados[1]))
                    imovel.set_area_privativa(float(dados[1]))
                    imovel.set_situacao(dados[1])
                    imovel.set_ocupacao(dados[1])
                    imovel.set_cpf_proprietario(dados[1])
                    imovel.set_cpf_corretor(dados[1])
                    lista.append(imovel)
                return lista
            except Exception as e:
                erro = f"Banco.get_lista_imoveis_disponiveis: ERRO! {e}"
                return [], erro

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
                    imovel = Imovel.Imovel(*registro[2:9])
                    imovel.set_codigo(registro[1])
                    imovel.set_valor_venda(float(registro[1]))
                    imovel.set_valor_aluguel(float(registro[1]))
                    imovel.set_quant_quartos(int(registro[1]))
                    imovel.set_quant_salas(int(registro[1]))
                    imovel.set_quant_vagas(int(registro[1]))
                    imovel.set_quant_banheiros(int(registro[1]))
                    imovel.set_quant_varandas(int(registro[1]))
                    imovel.set_nome_condominio(registro[1])
                    imovel.set_cor(registro[1])
                    imovel.set_categoria(registro[1])
                    imovel.set_descricao(registro[1])
                    imovel.set_endereço(registro[1])
                    imovel.set_status(registro[1])
                    imovel.set_iptu(float(registro[1]))
                    imovel.set_estado(registro[1])
                    imovel.set_valor_condominio(float(registro[1]))
                    imovel.set_andar(registro[1])
                    imovel.set_estado(registro[1])
                    imovel.set_ano_construcao(registro[1])
                    imovel.set_area_total(float(registro[1]))
                    imovel.set_area_privativa(float(registro[1]))
                    imovel.set_situacao(registro[1])
                    imovel.set_ocupacao(registro[1])
                    imovel.set_cpf_proprietario(registro[1])
                    imovel.set_cpf_corretor(registro[1])
                    lista_imoveis.append(imovel)
                return lista_imoveis
            except Exception as e:
                erro = f"Banco.get_imoveis_por_categoria: ERRO! {e}"
                return [], erro
