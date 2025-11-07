import sqlite3
import bcrypt
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
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Comprador (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
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
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
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
                    categoria = TEXT NULL,
                    descricao TEXT NULL,
                    endereco TEXT NOT NULL,
                    status = TEXT NULL,
                    iptu REAL NULL,
                    valor_condominio REAL NULL,
                    andar INTEGER NULL,
                    estado = TEXT NULL,
                    numero INTEGER NULL,
                    complemento TEXT NULL,
                    bloco TEXT NULL,
                    ano_construcao INTEGER NULL,
                    area_total REAL NULL,
                    area_privativa REAL NULL,
                    bairro TEXT NOT NULL, 
                    rua TEXT NOT NULL,
                    cidade TEXT NULL,
                    situacao = TEXT NULL,
                    ocupacao = TEXT NULL,
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
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Tipo_Usuario (
                    id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT UNIQUE NOT NULL
                    );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Usuario (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    tipo INTEGER NOT NULL,
                    FOREIGN KEY (tipo) REFERENCES Tipo_Usuario (id_tipo)
                    );
                    
                                ''')

            try:
                self.init_tabelas()

            except:
                pass

            conexao.commit()

    def init_tabelas(self):
        with sqlite3.connect("data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute('''INSERT INTO Tipo_Usuario (tipo) 
                        VALUES(?)''', ("Administrador",))
            cursor.execute('''INSERT INTO Tipo_Usuario (tipo) 
                        VALUES(?)''', ("Corretor",))
            cursor.execute('''INSERT INTO Tipo_Usuario (tipo) 
                        VALUES(?)''', ("Cliente",))
            cursor.execute('''INSERT INTO Tipo_Usuario (tipo) 
                        VALUES(?)''', ("Captador",))

    def atualizar_dado_cliente(self, cpf, campo, dado):
        with sqlite3.connect("data\\Loja.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(f'''
                    UPDATE Cliente
                    SET {campo} = ?
                    WHERE cpf = ?
                ''', (dado, cpf))
                conexao.commit()
                return True
            except Exception as e:
                print("Erro ao atualizar dado do cliente:", e)
                return False

    def get_lista_imoveis_carrinho(self, cpf):
        with sqlite3.connect("data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Carrinho_Compras WHERE cpf_cliente = ?', (cpf,))
            lista_registros = cursor.fetchall()
            if not lista_registros:
                return []
            lista_imoveis = []
            for registro in lista_registros:
                lista_imoveis.append(self.get_imovel_por_id(registro[1]))
            return lista_imoveis

    def get_item_carrinho_por_id(self, cpf, id_imovel):
        with sqlite3.connect("data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Carrinho_Compras WHERE cpf_cliente = ? AND id_imovel = ?', (cpf, id_imovel))
            registro = cursor.fetchone()
            if not registro:
                return None
            else:
                return self.get_imovel_por_id(registro[1])

    def get_quantidade_item_carrinho(self, id_imovel):
        with sqlite3.connect("data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT quantidade FROM Carrinho_Compras WHERE id_imovel = ?', (id_imovel,))
            registro = cursor.fetchone()
            if not registro:
                return 0
            else:
                return registro[0]

    def remover_item_carrinho(self, cpf, id_imovel):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_delete_query = """
                    DELETE FROM Carrinho_Compras
                    WHERE cpf_cliente = ? AND id_imovel = ?
                    """
                cursor.execute(sql_delete_query, (cpf, id_imovel))
                conexao.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def atualizar_quantidade_item_carrinho(self, cpf, id_imovel, quantidade):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_update_query = """
                    UPDATE Carrinho_Compras
                    SET quantidade = ?
                    WHERE cpf_cliente = ? AND id_imovel = ?
                    """
                cursor.execute(sql_update_query, (quantidade, cpf, id_imovel))
                conexao.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def get_compras_usuario_por_cpf(self, cpf):
        with sqlite3.connect("data\\Loja.db", check_same_thread=False) as conexao:

            try:
                cursor = conexao.cursor()
                cursor.execute('''
                    SELECT id_venda FROM Venda WHERE cpf_cliente = ?
                ''', (cpf,))
                vendas = cursor.fetchall()

                dicionario_venda = {}

                for id in vendas:

                    cursor.execute('''
                        SELECT * FROM Venda_imoveis WHERE id_venda = ?
                    ''', (id,))
                    imoveis = cursor.fetchall()
                    lista = []
                    for imovel in imoveis:
                        lista.append(imovel)

                    if lista:
                        dicionario_venda[id[1]] = lista

                if not dicionario_venda:
                    return {}

                return dicionario_venda
            except Exception as e:
                print("Erro ao buscar compras do usuário:", e)
                return {}

    def get_lista_usuarios(self):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:

            try:
                cursor = conexao.cursor()
                lista = []
                cursor.execute("SELECT * FROM Usuario")
                resultados = cursor.fetchall()
                if not resultados:
                    return []
                for dados in resultados:
                    usuario = Usuario.Usuario(*dados[1:])
                    usuario.set_id(dados[0])
                    lista.append(usuario)
                return lista
            except Exception as e:
                print("Erro ao buscar usuarios:", e)
                return []

    def verificar_usuario(self, usuario):
        with sqlite3.connect("data\\Loja.db", check_same_thread=False) as conexao:
            try:
                cursor = conexao.cursor()
                registro = None
                if usuario.get_email():
                    cursor.execute('''
                        SELECT * FROM Usuario WHERE email = ?
                    ''', (usuario.get_email(),))
                    registro = cursor.fetchone()
                else:
                    cursor.execute('''
                        SELECT * FROM Usuario WHERE nome = ?
                    ''', (usuario.get_nome(),))
                    registro = cursor.fetchone()
                if not registro:
                    return None

                senha_hash = registro[3]
                print(usuario.get_senha().encode('utf-8'), senha_hash)
                if bcrypt.checkpw(usuario.get_senha().encode('utf-8'), senha_hash):
                    return Usuario.Usuario(*registro[1:], gerar_hash_senha=False)
                else:
                    return None
            except Exception as e:
                print("Erro ao buscar usuario:", e)
                return None

    def adicionar_carrinho(self, cpf_cliente, id_imovel, quantidade):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO Carrinho_Compras (cpf_cliente, id_imovel, quantidade) 
                VALUES(?, ?, ?)
                '''

                cursor.execute(sql_query, (
                    cpf_cliente,
                    id_imovel,
                    quantidade
                ))
                conexao.commit()
                return True
            except Exception as e:
                print("Erro ao adicionar no carrinho:", e)
                return False

    def cadastrar_usuario(self, usuario):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO Usuario (nome, email, senha, tipo) 
                VALUES(?, ?, ?, ?)
                '''

                cursor.execute(sql_query, (
                    usuario.get_nome(),
                    usuario.get_email(),
                    usuario.get_senha(),
                    usuario.get_tipo().value
                ))
                conexao.commit()
                return True
            except Exception as e:
                print("Erro ao cadastrar usuario:", e)
                return False

    def cadastrar_pessoa(self, cliente):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = f''' 
                INSERT INTO {cliente.__class__.__name__} (nome, cpf, rg, telefone, endereco, email) 
                VALUES(?, ?, ?, ?, ?, ?)
                '''
                cursor.execute(sql_query, (
                    cliente.get_nome(),
                    cliente.get_cpf(),
                    cliente.get_rg(),
                    cliente.get_telefone(),
                    cliente.get_endereco(),
                    cliente.get_email()
                ))
                conexao.commit()
                return True
            except Exception as e:
                print("Erro ao cadastrar cliente:", e)
                return False

    def remove_pessoa_por_cpf(self, cpf):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_delete_query = """
                    DELETE FROM Cliente
                    WHERE cpf = ?
                    """
                cursor.execute(sql_delete_query, (cpf,))
                conexao.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def get_lista_clientes(self):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            lista = []
            cursor.execute("SELECT * FROM Cliente")
            resultados = cursor.fetchall()
            for dados in resultados:
                cliente = Cliente.Cliente(*dados[1:])
                cliente.set_id(dados[0])
                lista.append(cliente)
            return lista

    def get_pessoa_por_email(self, email):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Cliente WHERE email = ?', (email,))
            registro = cursor.fetchone()
            if not registro:
                return None

            cliente = Cliente.Cliente(*registro[1:])
            cliente.set_id(registro[0])

            return cliente

    def get_pessoa_por_cpf(self, cpf):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Cliente WHERE cpf = ?', (cpf,))
            registro = cursor.fetchone()
            if not registro:
                return None
            cliente = Cliente.Cliente(*registro[1:])
            cliente.set_id(registro[0])
            return cliente

    def remover_imovel(self, id):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_delete_query = """
                    DELETE FROM imovel
                    WHERE id_imovel = ?
                    """
                cursor.execute(sql_delete_query, (id,))
                conexao.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def get_imovel_por_id(self, id):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM imovel WHERE id_imovel = ?', (id,))
            registro = cursor.fetchone()
            if not registro:
                return None
            imovel = Imovel.imovel(*registro[2:9])
            imovel.set_preco(float(imovel.get_preco()))
            imovel.set_quantidade(int(imovel.get_quantidade()))
            imovel.set_descricao(registro[-2])
            imovel.set_imagem(registro[-1])
            imovel.set_id(int(registro[0]))
            imovel.set_codigo(registro[1])
            return imovel

    def adicionar_imovel(self, imovel):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO imovel (codigo, nome, marca, modelo, cor, preco, quantidade, categoria, descricao, imagem) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    '''
                cursor.execute(sql_query, (
                    imovel.get_codigo(),
                    imovel.get_nome(),
                    imovel.get_marca(),
                    imovel.get_modelo(),
                    imovel.get_cor(),
                    imovel.get_preco(),
                    imovel.get_quantidade(),
                    imovel.get_categoria(),
                    imovel.get_descricao(),
                    imovel.get_imagem()
                ))
                conexao.commit()
                return True
            except Exception as e:
                print(f"Erro ao adicionar imovel: {e}")
                return False

    def get_lista_imoveis(self):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            lista = []
            cursor.execute("SELECT * FROM imovel")
            resultados = cursor.fetchall()
            for dados in resultados:
                imovel = Imovel.imovel(*dados[2:9])
                imovel.set_preco(float(imovel.get_preco()))
                imovel.set_quantidade(int(imovel.get_quantidade()))
                imovel.set_descricao(dados[-2])
                imovel.set_imagem(dados[-1])
                imovel.set_id(int(dados[0]))
                imovel.set_codigo(dados[1])
                lista.append(imovel)
            return lista

    def get_lista_imoveis_disponiveis(self):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            lista = []
            cursor.execute("SELECT * FROM imovel WHERE quantidade > 0")
            resultados = cursor.fetchall()
            for dados in resultados:
                imovel = Imovel.imovel(*dados[2:9])
                imovel.set_preco(float(imovel.get_preco()))
                imovel.set_quantidade(int(imovel.get_quantidade()))
                imovel.set_descricao(dados[-2])
                imovel.set_imagem(dados[-1])
                imovel.set_id(int(dados[0]))
                imovel.set_codigo(dados[1])
                lista.append(imovel)
            return lista

    def get_imoveis_por_nome(self, nome):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM imovel WHERE nome = ?', (nome,))
            lista_registros = cursor.fetchall()
            lista_imoveis = []
            for registro in lista_registros:
                imovel = Imovel.imovel(*registro[2:9])
                imovel.set_preco(float(imovel.get_preco()))
                imovel.set_quantidade(int(imovel.get_quantidade()))
                imovel.set_descricao(registro[-2])
                imovel.set_imagem(registro[-1])
                imovel.set_id(int(registro[0]))
                imovel.set_codigo(registro[1])

                lista_imoveis.append(imovel)
            return lista_imoveis

    def get_imoveis_por_marca(self, marca):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM imovel WHERE marca = ?', (marca,))
            lista_registros = cursor.fetchall()
            lista_imoveis = []
            for registro in lista_registros:
                imovel = Imovel.imovel(*registro[2:9])
                imovel.set_preco(float(imovel.get_preco()))
                imovel.set_quantidade(int(imovel.get_quantidade()))
                imovel.set_descricao(registro[-2])
                imovel.set_imagem(registro[-1])
                imovel.set_id(int(registro[0]))
                imovel.set_codigo(registro[1])

                lista_imoveis.append(imovel)

            return lista_imoveis

    def get_imoveis_por_modelo(self, modelo):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM imovel WHERE modelo = ?', (modelo,))
            lista_registros = cursor.fetchall()
            lista_imoveis = []
            for registro in lista_registros:
                imovel = Imovel.imovel(*registro[2:9])
                imovel.set_preco(float(imovel.get_preco()))
                imovel.set_quantidade(int(imovel.get_quantidade()))
                imovel.set_descricao(registro[-2])
                imovel.set_imagem(registro[-1])
                imovel.set_id(int(registro[0]))
                imovel.set_codigo(registro[1])

                lista_imoveis.append(imovel)
            return lista_imoveis

    def get_imoveis_por_categoria(self, categoria):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM imovel WHERE categoria = ?', (categoria,))
            lista_registros = cursor.fetchall()
            lista_imoveis = []
            for registro in lista_registros:
                imovel = Imovel.imovel(*registro[2:9])
                imovel.set_preco(float(imovel.get_preco()))
                imovel.set_quantidade(int(imovel.get_quantidade()))
                imovel.set_descricao(registro[-2])
                imovel.set_imagem(registro[-1])
                imovel.set_id(int(registro[0]))
                imovel.set_codigo(registro[1])

                lista_imoveis.append(imovel)
            return lista_imoveis
