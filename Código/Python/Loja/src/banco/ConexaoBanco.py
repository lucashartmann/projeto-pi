import mysql.connector

class ConexaoBanco:
    @staticmethod
    def get_connection():
        servidor = "localhost"
        porta = "3306"
        database = "loja"
        usuario = "root"
        senha = ""
        try:
            conexao = mysql.connector.connect(
                host=servidor,
                port=porta,
                database=database,
                user=usuario,
                password=senha
            )
            return conexao
        except mysql.connector.Error as e:
            print(f"Erro ao conectar: {e}")
            return None

if __name__ == "__main__":
    conexao = ConexaoBanco.get_connection()
    if conexao:
        print("Conexão estabelecida com sucesso!")
        conexao.close()