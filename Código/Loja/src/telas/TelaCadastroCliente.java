package telas;

import dados.Cliente;

import java.awt.event.*;
import java.util.ArrayList;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

import banco.OperacoesBanco;

public class TelaCadastroCliente extends JDialog {
    private JPanel contentPane;
    private JFrame clienteJFrame;
    private JTextField campoCPF, campoNome, campoResultado, campoRG;
    private JButton voltarButton, cadastrarButton, editarButton;
    private String nome, cpf, rg;
    private GerenciarTelas gerenciarTelas;
    private Cliente cliente;

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
            nome = campoNome.getName();
            rg = campoRG.getNome();
            cpf = campoCPF.getNome();
            public void actionPerformed(ActionEvent e) {
                if (nome == null || cpf == null || rg == null) {
                    campoResultado.setText("Erro ao cadastrar. Tente novamente");
                } else {
                    cliente = new Cliente(nome, cpf, rg);
                    campoResultado.setText(cliente.toString());
                    operacoesBanco.inserirCliente(cliente);
                }
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}