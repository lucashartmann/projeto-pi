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

public class TelaCliente extends JDialog {
    private JPanel contentPane;
    private JTextField campoCPF, campoNome, campoResultado, campoRG;
    private JButton voltarButton, cadastrarButton, editarButton;
    private String nome, cpf, rg;
    private GerenciarTelas gerenciarTelas;
    private Cliente cliente;

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
                cpf = campoCPF.getText();
                rg = campoRG.getText();
                if (nome == null || cpf == null || rg == null) {
                    campoResultado.setText("Erro ao cadastrar. Tente novamente. " +
                            "\nCliente: Nome: " + nome + ", CPF: " + cpf + ", RG: " + rg);
                } else {
                    cliente = new Cliente(nome, cpf, rg);
                    campoResultado.setText(cliente.toString());
                    operacoesBanco.inserirCliente(cliente);
                }
            }
        });
        editarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {}
            // Falta implementar
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}