import sqlite3
from model import Cliente, Produto
import os


class Banco:
    def __init__(self):
        diretorio = "data"
        if not os.path.isdir(diretorio):
            os.makedirs(diretorio)
        self.conexao = sqlite3.connect(
            "data\\Loja.db", check_same_thread=False)
        self.cursor = self.conexao.cursor()
        self.init_tabelas()

    def init_tabelas(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS Cliente (
                nome TEXT NOT NULL,
                cpf TEXT PRIMARY KEY,
                rg TEXT NOT NULL,
                telefone TEXT NOT NULL,
                endereco TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
                            ''')
        self.cursor.execute(f'''
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

        self.conexao.commit()

    def cadastrar_cliente(self, cliente):
        try:
            sql_query = ''' 
            INSERT INTO Cliente (nome, cpf, rg, telefone, endereco, email) 
            VALUES(?, ?, ?, ?, ?, ?)
            '''
            self.cursor.execute(sql_query, (
                cliente.get_nome(),
                cliente.get_cpf(),
                cliente.get_rg(),
                cliente.get_telefone(),
                cliente.get_endereco(),
                cliente.get_email()
            ))
            self.conexao.commit()
            return True
        except Exception as e:
            print("Erro ao cadastrar cliente:", e)
            return False

    def remove_cliente(self, cpf):
        try:
            sql_delete_query = """
                DELETE FROM Cliente
                WHERE cpf = ?
                """
            self.cursor.execute(sql_delete_query, (cpf,))
            self.conexao.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def remover_produto(self, id):
        try:
            sql_delete_query = """
                DELETE FROM Produto
                WHERE id_produto = ?
                """
            self.cursor.execute(sql_delete_query, (id,))
            self.conexao.commit()
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
        lista = []
        self.cursor.execute("SELECT * FROM Cliente")
        resultados = self.cursor.fetchall()
        for dados in resultados:
            cliente = Cliente.Cliente(*dados)
            lista.append(cliente)
        return lista

    def get_cliente_por_email(self, email):
        self.cursor.execute(
            f'SELECT * FROM Cliente WHERE email = ?', (email,))
        registro = self.cursor.fetchone()
        if not registro:
            return None
        cliente = Cliente.Cliente(*registro)
        return cliente

    def get_cliente_por_cpf(self, cpf):
        self.cursor.execute(
            f'SELECT * FROM Cliente WHERE cpf = ?', (cpf,))
        registro = self.cursor.fetchone()
        if not registro:
            return None
        cliente = Cliente.Cliente(*registro)
        return cliente

    def get_produto_por_id(self, id):
        self.cursor.execute(
            f'SELECT * FROM Produto WHERE id_produto = ?', (id,))
        registro = self.cursor.fetchone()
        if not registro:
            return None
        produto = Produto.Produto(*registro[1:])
        produto.set_id(registro[0])
        return produto

    def adicionar_produto(self, produto):
        try:
            sql_query = ''' 
            INSERT INTO Produto (nome, marca, modelo, cor, preco, quantidade, categoria) 
            VALUES(?, ?, ?, ?, ?, ?, ?)
                                '''
            self.cursor.execute(sql_query, (
                produto.get_nome(),
                produto.get_marca(),
                produto.get_modelo(),
                produto.get_cor(),
                produto.get_preco(),
                produto.get_quantidade(),
                produto.get_categoria()
            ))
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")
            return False

    def get_lista_produtos(self):
        lista = []
        self.cursor.execute("SELECT * FROM Produto")
        resultados = self.cursor.fetchall()
        for dados in resultados:
            produto = Produto.Produto(*dados[1:])
            produto.set_id(dados[0])
            lista.append(produto)
        return lista

    def get_produtos_por_nome(self, nome):
        self.cursor.execute(
            f'SELECT * FROM Produto WHERE nome = ?', (nome,))
        lista_registros = self.cursor.fetchall()
        lista_produtos = []
        for registro in lista_registros:
            produto = Produto.Produto(*registro[1:])
            produto.set_id(registro[0])
            lista_produtos.append(registro)
        return lista_produtos

    def get_produtos_por_marca(self, marca):
        self.cursor.execute(
            f'SELECT * FROM Produto WHERE marca = ?', (marca,))
        lista_registros = self.cursor.fetchall()
        lista_produtos = []
        for registro in lista_registros:
            produto = Produto.Produto(*registro[1:])
            produto.set_id(registro[0])
            lista_produtos.append(registro)
        return lista_produtos

    def get_produtos_por_modelo(self, modelo):
        self.cursor.execute(
            f'SELECT * FROM Produto WHERE modelo = ?', (modelo,))
        lista_registros = self.cursor.fetchall()
        lista_produtos = []
        for registro in lista_registros:
            produto = Produto.Produto(*registro[1:])
            produto.set_id(registro[0])
            lista_produtos.append(registro)
        return lista_produtos

    def get_produtos_por_categoria(self, categoria):
        self.cursor.execute(
            f'SELECT * FROM Produto WHERE categoria = ?', (categoria,))
        lista_registros = self.cursor.fetchall()
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
