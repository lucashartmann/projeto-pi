package banco;

import java.sql.Connection;
import java.sql.DriverManager;
import  java.sql.SQLException;

public class conexaoBanco {
    public static Connection createConnection() throws SQLException{
		String url = "jdbc:mysql://localhost:3306/loja"; //Nome da base de dados
		String user = "root"; //nome do usuário do MySQL
		String password = ""; //senha do MySQL

		Connection conexao = null;
		conexao = DriverManager.getConnection(url, user, password);

		return conexao;
	}
}
