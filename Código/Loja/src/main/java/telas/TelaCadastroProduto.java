package telas;

import dados.Loja;
import dados.Produto;
import java.awt.event.*;
import java.util.ArrayList;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

public class TelaCadastroProduto extends JDialog {
    private JPanel contentPane;
    private JButton voltarButton;
    private JButton cadastrarButton;
    private JTextField campoPlaca;
    private JTextField campoResultado;
    private JTextField campoMarca;
    private JLabel placaTexto;
    private JLabel marcaTexto;
    private GerenciarTelas gerenciarTelas;
    private String placa;
    private String marca;
    private Produto produto;
    private ArrayList<Produto> estoque = new ArrayList<>();

    public void screen(Loja loja) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); //Tamanho da tela
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();

        voltarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(0, loja);
                dispose();
            }
        });
        cadastrarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                placa = campoPlaca.getName();
                marca = campoPlaca.getName();
                if (placa == null) {
                    campoResultado.setText("Erro ao cadastrar placa, tente novamente");
                } else if (marca == null) {
                    campoResultado.setText("Erro ao cadastrar marca, tente novamente");
                } else if (estoque.contains(produto)) {
                    campoResultado.setText("produto já cadastrado no cinema");
                } else if (!estoque.add(produto)) {
                    campoResultado.setText("Erro ao cadastrar produto");
                } else {
                    produto = new Produto();
                    // garagemprodutos = loja.getGaragem();
                    estoque.add(produto);
                    for (produto produto1 : estoque) {
                        //garagemprodutos.adicionar(produto);
                    }
                    //campoResultado.setText(garagemprodutos.listaprodutos());
                }
            }
        });

        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }

}
