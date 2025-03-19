package telas;

import dados.Produto;
import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

import banco.OperacoesBanco;

public class TelaEditarProduto extends JDialog {
    private JPanel contentPane;
    private JButton editButton, backButton;
    private JLabel placaTexto, marcaTexto;
    private JTextField campoPlaca, campoResultado, campoMarca, fieldNewPlaca, fieldNewMarca;
    private GerenciarTelas gerenciarTelas;
    private String nome, marca, modelo, cor, preco;
    private String novoNome, novaMarca, novoModelo, novaCor, novoPreco;
    private double precoConvertido;

    public void telaEditarprodutos(OperacoesBanco operacoesBanco) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); // Tamanho da tela
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();

        backButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(0, operacoesBanco);
                dispose();
            }
        });
        editButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                nome = campoPlaca.getText();
                modelo = campoPlaca.getText();
                cor = campoPlaca.getText();
                preco = campoPlaca.getText();
                marca = campoMarca.getText();
                if (nome != null && marca != null) {
                    Produto produto = operacoesBanco.consultarprodutoPorPlacaMarca(placa, marca);
                    campoResultado.setText("produto antes: " + produto.toString());
                    novaMarca = fieldNewMarca.getText();
                    novoNome = campoNovoNome.getText();
                    novoModelo = campoNovoModelo.getText();
                    novaCor = campoNovaCor.getText();
                    novoPreco = campoNovoPreco.getText();
                    precoConvertido = Double.parseDouble(preco);
                    produto.setMarca(novaMarca);
                    produto.setModelo(novoModelo);
                    produto.setPreco(precoConvertido);
                    produto.setCor(novaCor);
                    produto.setNome(novoNome);
                    campoResultado.setText("produto depois: " + produto.toString());
                }
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}
