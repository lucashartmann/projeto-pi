package banco;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConexaoBanco {
	public static Connection getConnection() throws SQLException {
		String servidor = "localhost";
		String porta = "3306";
		String database = "loja"; // Nome do banco;
		String usuario = "root";
		String senha = "";

		String url = "jdbc:mysql://" + servidor + ":" + porta + "/" + database;
		Connection conexao = DriverManager.getConnection(url, usuario, senha);

		return conexao;
	}

	public static void main(String[] args) {
		try {
			Connection conn = getConnection();
			System.out.println("Conexão estabelecida com sucesso!");
			conn.close();
		} catch (SQLException e) {
			System.out.println("Erro ao conectar: " + e.getMessage());
			e.printStackTrace();
		}
	}
}