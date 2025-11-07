import sqlite3
import hashlib
import os

from model import Cliente, Imovel, Usuario


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
                CREATE TABLE IF NOT EXISTS Comprador (
                    id_comprador INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT NOT NULL
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Proprietario (
                    id_proprietario INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    idade INTEGER NULL,
                    data_nascimento TEXT NOT NULL
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
                    matricula TEXT NULL,
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
                    matricula TEXT NULL,
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
                    endereco TEXT NOT NULL,
                    status TEXT NULL,
                    iptu REAL NULL,
                    valor_condominio REAL NULL,
                    andar INTEGER NULL,
                    estado TEXT NULL,
                    numero INTEGER NULL,
                    complemento TEXT NULL,
                    bloco TEXT NULL,
                    ano_construcao INTEGER NULL,
                    area_total REAL NULL,
                    area_privativa REAL NULL,
                    bairro TEXT NOT NULL, 
                    rua TEXT NOT NULL,
                    cidade TEXT NULL,
                    situacao TEXT NULL,
                    ocupacao TEXT NULL,
                    cpf_proprietario TEXT NOT NULL,
                    cpf_corretor TEXT NOT NULL,
                    FOREIGN KEY (cpf_proprietario) references Proprietario (cpf),
                    FOREIGN KEY (cpf_corretor) references Corretor (cpf)
                );
                                ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Midia_Imovel (
                    id_imovel INTEGER PRIMARY KEY AUTOINCREMENT,
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

    def verificar_usuario(self, usuario, tabela):
        with sqlite3.connect("data\\Imobiliaria.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                registro = None
                if usuario.get_email():
                    cursor.execute(f'''
                        SELECT * FROM {tabela} WHERE email = ?
                    ''', (usuario.get_email(),))
                    registro = cursor.fetchone()
                else:
                    cursor.execute(f'''
                        SELECT * FROM {tabela} WHERE username = ?
                    ''', (usuario.get_username(),))
                    registro = cursor.fetchone()
                if not registro:
                    raise Exception("Usuário não encontrado")

                senha_hash_banco = registro[3]

                senha_hash = hashlib.sha256(
                    usuario.get_senha().encode('utf-8')).hexdigest()

                if senha_hash_banco == senha_hash:
                    return Usuario.Usuario(*registro[1:]), ""
                else:
                    raise Exception("Senha errada!")

            except Exception as e:
                erro = "Banco.verificar_usuario: ERRO!", e
                return None, erro

    def cadastrar_proprietario(self, proprietario):
        with sqlite3.connect(
                "data\\Imobiliaria.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                if isinstance(proprietario, Cliente.Proprietario):

                    sql_query = f''' 
                    INSERT INTO Proprietario (email, nome, cpf, email, rg, telefone, endereco, idade, data_nascimento) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                erro = f"Banco.cadastrar_cliente: ERRO! {e}"
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
                erro = f"Banco.cadastrar_cliente: ERRO! {e}"
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
                    imovel.get_numero(),
                    imovel.get_complemento(),
                    imovel.get_ano_construcao(),
                    imovel.get_area_total(),
                    imovel.get_area_privativa(),
                    imovel.get_bairro(),
                    imovel.get_rua(),
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
                    imovel.set_preco(float(imovel.get_preco()))
                    imovel.set_quantidade(int(imovel.get_quantidade()))
                    imovel.set_descricao(dados[-2])
                    imovel.set_imagem(dados[-1])
                    imovel.set_id(int(dados[0]))
                    imovel.set_codigo(dados[1])
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
                    imovel.set_preco(float(imovel.get_preco()))
                    imovel.set_quantidade(int(imovel.get_quantidade()))
                    imovel.set_descricao(registro[-2])
                    imovel.set_imagem(registro[-1])
                    imovel.set_id(int(registro[0]))
                    imovel.set_codigo(registro[1])

                    lista_imoveis.append(imovel)
                return lista_imoveis
            except Exception as e:
                erro = f"Banco.get_imoveis_por_categoria: ERRO! {e}"
                return [], erro
