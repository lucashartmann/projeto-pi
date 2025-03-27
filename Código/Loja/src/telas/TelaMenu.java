package telas;

import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JPanel;

import banco.OperacoesBanco;

public class TelaMenu extends JDialog {
    private JPanel contentPane;
    private JButton produtosButton, clientesButton;
    private GerenciarTelas gerenciarTelas;
    private JButton lojaButton, funcionariosButton, fornecedoresButton;

    public void screen(OperacoesBanco operacoesBanco) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600);
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();

        produtosButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(3, operacoesBanco);
                dispose();
            }
        });
        clientesButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(2, operacoesBanco);
                dispose();
            }
        });
        fornecedoresButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(4, operacoesBanco);
                dispose();
            }
        });
        funcionariosButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(5, operacoesBanco);
                dispose();
            }
        });
        lojaButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(1, operacoesBanco);
                dispose();
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }

    public JPanel getJPanel() {
        return contentPane;
    }

}
