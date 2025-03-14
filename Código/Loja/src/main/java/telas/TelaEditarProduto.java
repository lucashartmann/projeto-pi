package telas;

import dados.Loja;
import dados.Produto;
import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

public class TelaEditarProduto extends JDialog {
    private JPanel contentPane;
    private JButton editButton, backButton;
    private JLabel placaTexto, marcaTexto;
    private JTextField campoPlaca, campoResultado, campoMarca, fieldNewPlaca, fieldNewMarca;
    private GerenciarTelas gerenciarTelas;
    private Garagemprodutos garagemprodutos;
    private String placa, marca, novaPlaca, novaMarca;

    public void telaEditarprodutos(Loja loja) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); //Tamanho da tela
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();
        garagemprodutos = loja.getGaragem();

        backButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(0, loja);
                dispose();
            }
        });
        editButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                placa = campoPlaca.getText();
                marca = campoMarca.getText();
                if (placa != null && marca != null) {
                    Produto produto = garagemprodutos.consultarprodutoPorPlacaMarca(placa, marca);
                    campoResultado.setText("produto antes: " + produto.toString());
                    novaMarca = fieldNewMarca.getText();
                    novaPlaca = fieldNewPlaca.getText();
                    produto.setMarca(novaMarca);
                    produto.setPlaca(novaPlaca);
                    campoResultado.setText("produto depois: " + produto.toString());
                }
                if (placa != null && marca == null) {
                    Produto produto = garagemprodutos.consultarprodutoPorPlaca(placa);
                    campoResultado.setText("produto antes: " + produto.toString());
                    novaMarca = fieldNewMarca.getText();
                    novaPlaca = fieldNewPlaca.getText();
                    produto.setMarca(novaMarca);
                    produto.setPlaca(novaPlaca);
                    campoResultado.setText("produto depois: " + produto.toString());
                }
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}
