package banco;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import dados.Cliente;
import dados.Produto;

public class OperacoesBanco {

    private int quantClientes, quantProdutos, quantFornecedores, quantFucionarios;
    private Connection conexao = null;
    private PreparedStatement stmt = null;
    private ResultSet rs = null;
    private String sql;

    public boolean inserirCliente(Cliente cliente) {
        sql = "INSERT INTO Cliente (nome, cpf, rg, idade) VALUES (?, ?, ?, ?)";
        try {
            conexao = ConexaoBanco.getConnection();
            stmt = conexao.prepareStatement(sql);
            stmt.setString(1, cliente.getNome());
            stmt.setString(2, cliente.getCpf());
            stmt.setString(3, cliente.getRg());
            int linhasAfetadas = stmt.executeUpdate();
            quantClientes++;
            return linhasAfetadas > 0;
        } catch (SQLException e) {
            if (e.getMessage().contains("Duplicate") || e.getErrorCode() == 1062) {
                System.out.println("Cliente já existe no banco de dados: " + e.getMessage());
            } else {
                System.out.println("Erro ao inserir cliente: " + e.getMessage());
            }
            e.printStackTrace();
            return false;
        } finally {
            try {
                if (stmt != null)
                    stmt.close();
                if (conexao != null)
                    conexao.close();
            } catch (SQLException e) {
                System.out.println("Erro ao fechar recursos: " + e.getMessage());
            }
        }
    }

    public boolean inserirProduto(Produto produto) {
    }

    public List<Cliente> consultarClientesPorNome(String nome) {
        List<Cliente> clientes = new ArrayList<>();
        sql = "SELECT * FROM Cliente WHERE nome LIKE ?";
        try {
            conexao = ConexaoBanco.getConnection();
            stmt = conexao.prepareStatement(sql);
            stmt.setString(1, "%" + nome + "%");
            rs = stmt.executeQuery();
            while (rs.next()) {
                Cliente cliente = new Cliente();
                cliente.setId(rs.getInt("id_cliente"));
                cliente.setNome(rs.getString("nome"));
                cliente.setCpf(rs.getString("cpf"));
                cliente.setRg(rs.getString("rg"));
                cliente.setIdade(rs.getInt("idade"));
                clientes.add(cliente);
            }
        } catch (SQLException e) {
            System.out.println("Erro ao consultar clientes: " + e.getMessage());
            e.printStackTrace();
        } finally {
            try {
                if (rs != null)
                    rs.close();
                if (stmt != null)
                    stmt.close();
                if (conexao != null)
                    conexao.close();
            } catch (SQLException e) {
                System.out.println("Erro ao fechar recursos: " + e.getMessage());
            }
        }
        return clientes;
    }

    public int getQuantidadeClientes() {
        return quantClientes;
    }

}
