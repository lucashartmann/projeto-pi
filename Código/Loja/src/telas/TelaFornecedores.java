package telas;

import banco.OperacoesBanco;

import javax.swing.*;
import java.awt.event.*;

public class TelaFornecedores extends JDialog {
    private JPanel contentPane;
    private JButton cadastrarButton, voltarButton, editarButton;
    private JTextField campoCPF, campoResultado, campoNome;
    private GerenciarTelas gerenciarTelas;

    public void tela(OperacoesBanco operacoesBanco) {
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

        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}
