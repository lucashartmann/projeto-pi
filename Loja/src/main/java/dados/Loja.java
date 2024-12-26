package dados;

import java.util.ArrayList;

public class Loja {
    private String nome;
    private int quantClientes;
    private int quantProdutos;
    private int quantFornecedores;
    private int quantFuncionarios;
    private ArrayList<Produto> estoque;
    private ArrayList<Cliente> clientela;
    private ArrayList<Funcionario> equipe;

    public Loja(String nome) {
        this.nome = nome;
        estoque = new ArrayList<>();
        clientela = new ArrayList<>();
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public boolean addCliente(Cliente cliente) {
        if (!clientela.contains(cliente)) {
            clientela.add(cliente);
            quantClientes++;
            return true;
        }
        return false;
    }

    public boolean addProduto(Produto produto) {
        if (!estoque.contains(produto)) {
            estoque.add(produto);
            quantProdutos++;
            return true;
        }
        return false;
    }

    public boolean addFuncionario(Funcionario funcionario) {
        if (!equipe.contains(funcionario)) {
            equipe.add(funcionario);
            quantFuncionarios++;
            return true;
        }
        return false;
    }

    public boolean removeCliente(Cliente cliente) {
        if (clientela.contains(cliente)) {
            clientela.remove(cliente);
            return true;
        }
        return false;
    }

    public boolean removeProduto(Produto produto) {
        if (estoque.contains(produto)) {
            estoque.remove(produto);
            return true;
        }
        return false;
    }

    public boolean removeFuncionario(Funcionario funcionario) {
        if (equipe.contains(funcionario)) {
            equipe.remove(funcionario);
            return true;
        }
        return false;
    }

    public Produto getProdutoPorCodigo(int codigo) {
        for (Produto produto : estoque) {
            if (produto.getCodigo() == codigo) {
                return produto;
            }
        }
        return null;
    }

    public Cliente getClientePorId(int id) {
        for (Cliente cliente : clientela) {
            if (cliente.getId() == id) {
                return cliente;
            }
        }
        return null;
    }

    public Funcionario getFuncionarioPorId(int id) {
        for (Funcionario funcionario : equipe) {
            if (funcionario.getId() == id) {
                return funcionario;
            }
        }
        return null;
    }

    public int getQuantClientes() {
        return quantClientes;
    }

    public int getQuantProdutos() {
        return quantProdutos;
    }

    public int getQuantFornecedores() {
        return quantFornecedores;
    }

    public int getQuantFuncionarios() {
        return quantFuncionarios;
    }

}
