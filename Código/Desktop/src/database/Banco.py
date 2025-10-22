import sqlite3
from model import Cliente, Produto
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
                    nome TEXT NOT NULL,
                    cpf TEXT PRIMARY KEY,
                    rg TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Produto (
                    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    marca TEXT NOT NULL,
                    modelo TEXT NOT NULL,
                    cor TEXT NOT NULL,
                    preco FLOAT NOT NULL,
                    quantidade INT NOT NULL,
                    categoria TEXT NOT NULL
                );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Venda (
                    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpf_cliente INTEGER,
                    FOREIGN KEY cpf_cliente REFERENCES Cliente (cpf_cliente)
                    );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Venda_Produtos (
                    FOREIGN KEY id_venda REFERENCES Venda (id_venda),
                    FOREIGN KEY id_produto REFERENCES Produto (id_produto)
                    );
                                ''')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS Usuario (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('Cliente', 'Gerente', 'Funcionario', 'Administrador'))
                    );
                                ''')

            conexao.commit()
            
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
                    usuario.get_tipo()
                ))
                conexao.commit()
                return True
            except Exception as e:
                print("Erro ao cadastrar usuario:", e)
                return False


    def cadastrar_cliente(self, cliente):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO Cliente (nome, cpf, rg, telefone, endereco, email) 
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

    def remove_cliente(self, cpf):
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

    # def set_quantidade(self):
    #     self.quantidade_clientes = 0
    #     self.quantidade_fornecedores = 0
    #     self.quantidade_funcionarios = 0

    #     for pessoa in self.pessoas:
    #         if isinstance(pessoa, Cliente):
    #             self.quantidade_clientes += 1
    #         elif isinstance(pessoa, Fornecedor):
    #             self.quantidade_fornecedores += 1
    #         self.quantidade_funcionarios += 1

    def get_lista_clientes(self):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            lista = []
            cursor.execute("SELECT * FROM Cliente")
            resultados = cursor.fetchall()
            for dados in resultados:
                cliente = Cliente.Cliente(*dados)
                lista.append(cliente)
            return lista

    def get_cliente_por_email(self, email):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Cliente WHERE email = ?', (email,))
            registro = cursor.fetchone()
            if not registro:
                return None
            cliente = Cliente.Cliente(*registro)
            return cliente

    def get_cliente_por_cpf(self, cpf):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Cliente WHERE cpf = ?', (cpf,))
            registro = cursor.fetchone()
            if not registro:
                return None
            cliente = Cliente.Cliente(*registro)
            return cliente

    def get_produto_por_id(self, id):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f'SELECT * FROM Produto WHERE id_produto = ?', (id,))
            registro = cursor.fetchone()
            if not registro:
                return None
            produto = Produto.Produto(*registro[1:])
            produto.set_id(registro[0])
            return produto

    def adicionar_produto(self, produto):
        with sqlite3.connect(
                "data\\Loja.db", check_same_thread=False) as conexao:
            cursor = conexao.cursor()
            try:
                sql_query = ''' 
                INSERT INTO Produto (nome, marca, modelo, cor, preco, quantidade, categoria) 
                VALUES(?, ?, ?, ?, ?, ?, ?)
                                    '''
                cursor.execute(sql_query, (
                    produto.get_nome(),
                    produto.get_marca(),
                    produto.get_modelo(),
                    produto.get_cor(),
                    produto.get_preco(),
                    produto.get_quantidade(),
                    produto.get_categoria()
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
                produto = Produto.Produto(*dados[1:])
                produto.set_id(dados[0])
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
                produto = Produto.Produto(*registro[1:])
                produto.set_id(registro[0])
                lista_produtos.append(registro)
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
                produto = Produto.Produto(*registro[1:])
                produto.set_id(registro[0])
                lista_produtos.append(registro)
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
                produto = Produto.Produto(*registro[1:])
                produto.set_id(registro[0])
                lista_produtos.append(registro)
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
                produto = Produto.Produto(*registro[1:])
                produto.set_id(registro[0])
                lista_produtos.append(registro)
            return lista_produtos

    def get_quantidade_produto_por_marca(self, marca):
        return len(self.get_produtos_por_marca(marca))

    def get_quantidade_produto_por_modelo(self, modelo):
        return len(self.get_produtos_por_marca(modelo))

    def get_quantidade_produto_por_categoria(self, categoria):
        return len(self.get_produtos_por_marca(categoria))

    def get_quantidade_produtos(self):
        return len(self.get_lista_produtos())
