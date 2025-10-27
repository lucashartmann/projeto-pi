import sqlite3

import bcrypt
from model import Cliente, Produto, Usuario
import os


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
                CREATE TABLE IF NOT EXISTS Cliente (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Funcionario (
                    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Fornecedor (
                    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    rg TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Produto (
                    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    marca TEXT NOT NULL,
                    modelo TEXT NOT NULL,
                    cor TEXT NOT NULL,
                    preco FLOAT NOT NULL,
                    quantidade INT NULL,
                    categoria TEXT NOT NULL,
                    descricao TEXT NULL,
                    imagem BLOB NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Venda (
                    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpf_cliente TEXT,
                    FOREIGN KEY (cpf_cliente) REFERENCES Cliente (cpf)
                    );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Venda_Produtos (
                    id_venda INTEGER,
                    id_produto INTEGER,
                    FOREIGN KEY (id_venda) REFERENCES Venda (id_venda),
                    FOREIGN KEY (id_produto) REFERENCES Produto (id_produto)
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
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    tipo INTEGER NOT NULL,
                    FOREIGN KEY (tipo) REFERENCES Tipo_Usuario (id_tipo)
                    );
                    
                                ''')

            try:
                cursor.execute('''INSERT INTO Tipo_Usuario (tipo) 
                    VALUES(?)''', ("cliente",))
                cursor.execute('''INSERT INTO Tipo_Usuario (tipo) 
                    VALUES(?)''', ("funcionario",))
                cursor.execute('''INSERT INTO Tipo_Usuario (tipo) 
                    VALUES(?)''', ("administrador",))
                cursor.execute('''INSERT INTO Tipo_Usuario (tipo) 
                    VALUES(?)''', ("gerente",))
            except:
                pass

            conexao.commit()
            

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
                    registro = cursor.fetchall()
                if not registro:
                    return None

                if isinstance(registro, list):
                    for reg in registro:
                        senha_hash = reg[3]
                        print(usuario.get_senha().encode('utf-8'), senha_hash)
                        if bcrypt.checkpw(usuario.get_senha().encode('utf-8'), senha_hash):
                            return Usuario.Usuario(*reg[1:], gerar_hash_senha=False)
                else:
                    senha_hash = registro[3]
                    print(usuario.get_senha().encode('utf-8'), senha_hash)
                    if bcrypt.checkpw(usuario.get_senha().encode('utf-8'), senha_hash):
                        return Usuario.Usuario(*registro[1:], gerar_hash_senha=False)
                    else:
                        return None
            except Exception as e:
                print("Erro ao buscar usuario:", e)
                return None

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

    def remover_produto(self, id):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_delete_query = """
                    DELETE FROM Produto
                    WHERE id_produto = ?
                    """
                cursor.execute(sql_delete_query, (id,))
                conexao.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def get_produto_por_id(self, id):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Produto WHERE id_produto = ?', (id,))
            registro = cursor.fetchone()
            if not registro:
                return None
            produto = Produto.Produto(*registro[1:8])
            produto.set_descricao(registro[-2])
            produto.set_imagem(registro[-1])
            produto.set_id(registro[0])
            return produto

    def adicionar_produto(self, produto):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO Produto (codigo, nome, marca, modelo, cor, preco, quantidade, categoria, descricao, imagem) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    '''
                cursor.execute(sql_query, (
                    produto.get_codigo(),
                    produto.get_nome(),
                    produto.get_marca(),
                    produto.get_modelo(),
                    produto.get_cor(),
                    produto.get_preco(),
                    produto.get_quantidade(),
                    produto.get_categoria(),
                    produto.get_descricao(),
                    produto.get_imagem()
                ))
                conexao.commit()
                return True
            except Exception as e:
                print(f"Erro ao adicionar produto: {e}")
                return False

    def get_lista_produtos(self):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            lista = []
            cursor.execute("SELECT * FROM Produto")
            resultados = cursor.fetchall()
            for dados in resultados:
                produto = Produto.Produto(*dados[1:8])
                produto.set_descricao(dados[-2])
                produto.set_imagem(dados[-1])
                produto.set_id(dados[0])
                produto.set_codigo(dados[1])
                lista.append(produto)
            return lista

    def get_produtos_por_nome(self, nome):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Produto WHERE nome = ?', (nome,))
            lista_registros = cursor.fetchall()
            lista_produtos = []
            for registro in lista_registros:
                produto = Produto.Produto(*registro[1:8])
                produto.set_descricao(registro[-2])
                produto.set_imagem(registro[-1])
                produto.set_id(registro[0])
                produto.set_codigo(registro[1])

                lista_produtos.append(produto)
            return lista_produtos

    def get_produtos_por_marca(self, marca):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Produto WHERE marca = ?', (marca,))
            lista_registros = cursor.fetchall()
            lista_produtos = []
            for registro in lista_registros:
                produto = Produto.Produto(*registro[1:8])
                produto.set_descricao(registro[-2])
                produto.set_imagem(registro[-1])
                produto.set_id(registro[0])
                produto.set_codigo(registro[1])

                lista_produtos.append(produto)
                
            return lista_produtos

    def get_produtos_por_modelo(self, modelo):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Produto WHERE modelo = ?', (modelo,))
            lista_registros = cursor.fetchall()
            lista_produtos = []
            for registro in lista_registros:
                produto = Produto.Produto(*registro[1:8])
                produto.set_descricao(registro[-2])
                produto.set_imagem(registro[-1])
                produto.set_id(registro[0])
                produto.set_codigo(registro[1])

                lista_produtos.append(produto)
            return lista_produtos

    def get_produtos_por_categoria(self, categoria):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Produto WHERE categoria = ?', (categoria,))
            lista_registros = cursor.fetchall()
            lista_produtos = []
            for registro in lista_registros:
                produto = Produto.Produto(*registro[1:8])
                produto.set_descricao(registro[-2])
                produto.set_imagem(registro[-1])
                produto.set_id(registro[0])
                produto.set_codigo(registro[1])

                lista_produtos.append(produto)
            return lista_produtos
