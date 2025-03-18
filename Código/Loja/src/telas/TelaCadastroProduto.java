package telas;

import dados.Produto;
import java.awt.event.*;
import java.util.ArrayList;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

import banco.OperacoesBanco;

public class TelaCadastroProduto extends JDialog {
    private JPanel contentPane;
    private JButton voltarButton;
    private JButton cadastrarButton;
    private JTextField campoPreco;
    private JTextField campoCor;
    private JTextField campoNome;
    private JTextField campoMarca;
    private JTextField campoResultado;
    private JLabel placaTexto;
    private JLabel marcaTexto;
    private GerenciarTelas gerenciarTelas;
    private String nome;
    private int codigo;
    private String cor;
    private double preco;
    private String marca;
    private String modelo;
    private Produto produto;
    private boolean condicao;

    public void screen(OperacoesBanco operacoesBanco) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); // Tamanho da tela
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();

        voltarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(0, operacoesBanco);
                dispose();
            }
        });

        cadastrarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                nome = campoNome.getName();
                cor = campoCor.getName();
                marca = campoMarca.getName();
                preco = campoPreco.getName();
                if (nome == null) {
                    campoResultado.setText("Erro ao cadastrar placa, tente novamente");
                } else if (marca == null) {
                    campoResultado.setText("Erro ao cadastrar marca, tente novamente");
                } else {
                    produto = new Produto(nome, marca, modelo, cor, preco);
                    condicao = operacoesBanco.inserirProduto(produto);
                    if (condicao == true) {
                        campoResultado.setText(produto.toString());
                        System.out.println("Produto inserido com sucesso");
                    } else {
                        System.out.println("Erro ao inserir o produto");
                    }
                }
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}
