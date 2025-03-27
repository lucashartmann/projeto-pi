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

public class TelaProduto extends JDialog {
    private JPanel contentPane;
    private JButton voltarButton, cadastrarButton, editarButton;
    private JTextField campoMarca, campoResultado, campoNome, campoCor, campoPreco, campoModelo;
    private JLabel placaTexto, marcaTexto;
    private GerenciarTelas gerenciarTelas;
    private int codigo;
    private String cor, preco, marca, modelo, nome;
    private double precoConvertido;
    private Produto produto;
    private boolean condicao;

    public void screen(OperacoesBanco operacoesBanco) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600);
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
                nome = campoNome.getText();
                cor = campoCor.getText();
                marca = campoMarca.getText();
                preco = campoPreco.getText();
                modelo = campoModelo.getText();
                precoConvertido = Double.parseDouble(preco);
                if (nome == null || cor == null || marca == null || preco == null || modelo == null) {
                    campoResultado.setText("Erro ao cadastrar placa, tente novamente");
                } else {
                    produto = new Produto(nome, marca, modelo, cor, precoConvertido);
                    //condicao = operacoesBanco.inserirProduto(produto);
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
