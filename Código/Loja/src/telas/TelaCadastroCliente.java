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
    private JTextField campoCPF, campoNome, campoResultado;
    private JButton voltarButton, cadastrarButton, showClientsButton;
    private JLabel nome, cpf;
    private GerenciarTelas gerenciarTelas;
    private Cliente cliente;

    public void screen(OperacoesBanco operacoesBanco) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); // Tamanho da tela
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();
        // campoNome.setBackground(Color.darkGray);

        voltarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(0, operacoesBanco);
                dispose();
            }
        });
        cadastrarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (campoNome.getName() == null) {
                    campoResultado.setText("Erro ao cadastrar o nome. Tente novamente");
                } else {
                    cliente = new Cliente(campoNome.getName());
                    campoResultado.setText(cliente.toString());
                    operacoesBanco.inserirCliente(cliente);
                }
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}