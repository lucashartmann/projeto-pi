import mysql.connector
from mysql.connector import Error
from banco.conexao_banco import ConexaoBanco
from dados.cliente import Cliente

class OperacoesBanco:
    def __init__(self):
        self.quant_clientes = 0
        self.quant_produtos = 0
        self.quant_fornecedores = 0
        self.quant_funcionarios = 0

    def inserir_cliente(self, cliente: Cliente):
        sql = "INSERT INTO Cliente (nome, cpf, rg, idade) VALUES (%s, %s, %s, %s)"
        try:
            conexao = ConexaoBanco.get_connection()
            if conexao is None:
                print("Erro ao conectar ao banco de dados")
                return False
            
            cursor = conexao.cursor()
            cursor.execute(sql, (cliente.nome, cliente.cpf, cliente.rg, cliente.idade))
            conexao.commit()
            self.quant_clientes += 1
            return cursor.rowcount > 0

        except Error as e:
            if "Duplicate" in str(e) or e.errno == 1062:
                print(f"Cliente já existe no banco de dados: {e}")
            else:
                print(f"Erro ao inserir cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

        return False

    def consultar_clientes_por_nome(self, nome):
        sql = "SELECT * FROM Cliente WHERE nome LIKE %s"
        clientes = []
        try:
            conexao = ConexaoBanco.get_connection()
            if conexao is None:
                print("Erro ao conectar ao banco de dados")
                return []

            cursor = conexao.cursor(dictionary=True)
            cursor.execute(sql, (f"%{nome}%",))
            for row in cursor.fetchall():
                cliente = Cliente(row["nome"], row["cpf"], row["rg"])
                cliente.id = row["id_cliente"]
                cliente.idade = row["idade"]
                clientes.append(cliente)

        except Error as e:
            print(f"Erro ao consultar clientes: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

        return clientes

    def get_quantidade_clientes(self):
        return self.quant_clientes