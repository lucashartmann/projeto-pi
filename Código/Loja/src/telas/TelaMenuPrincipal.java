package telas;

import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;

import banco.OperacoesBanco;

public class TelaMenuPrincipal extends JDialog {
    private JPanel contentPane;
    private JButton cadastroCarroButton;
    private JButton cadastroClienteButton;
    private GerenciarTelas gerenciarTelas;
    private JLabel titulo;
    private JButton editCarsButton;
    private JButton editClientsButton;
    private JButton dealershipButton;

    public void screen(OperacoesBanco operacoesBanco) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); // Definindo o tamanho da tela
        setLocationRelativeTo(null); // Centralizando a tela
        gerenciarTelas = new GerenciarTelas();

        cadastroCarroButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(1, operacoesBanco);
                dispose();
            }
        });
        cadastroClienteButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(2, operacoesBanco);
                dispose();
            }
        });
        editCarsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(3, operacoesBanco);
                dispose();
            }
        });
        editClientsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(4, operacoesBanco);
                dispose();
            }
        });
        dealershipButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(5, operacoesBanco);
                dispose();
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }

    public JPanel getJPanel() {
        return contentPane;
    }

}
