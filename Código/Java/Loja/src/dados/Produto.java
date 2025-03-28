package dados;

public class Produto {
    private String nome;
    private int codigo;
    private String cor;
    private double preco;
    private String marca;
    private String modelo;

    public Produto(String nome, String marca, String modelo, String cor, double preco) {
        this.nome = nome;
        this.modelo = modelo;
        this.cor = cor;
        this.preco = preco;
        this.marca = marca;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public int getCodigo() {
        return codigo;
    }

    public void setCodigo(int codigo) {
        this.codigo = codigo;
    }

    public String getCor() {
        return cor;
    }

    public void setCor(String cor) {
        this.cor = cor;
    }

    public double getPreco() {
        return preco;
    }

    public void setPreco(double preco) {
        this.preco = preco;
    }

    public String getMarca() {
        return marca;
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }

    public String getModelo() {
        return modelo;
    }

    public void setModelo(String modelo) {
        this.modelo = modelo;
    }

    @Override
    public String toString() {
        return "Produto [nome=" + nome + ", codigo=" + codigo + ", cor=" + cor + ", preco=" + preco + ", marca=" + marca
                + ", modelo=" + modelo + "]";
    }

}
