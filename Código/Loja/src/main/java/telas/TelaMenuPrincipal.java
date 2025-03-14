package telas;

import dados.Loja;
import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class TelaMenuPrincipal extends JDialog {
    private JPanel contentPane;
    private JButton cadastroCarroButton;
    private JButton cadastroClienteButton;
    private GerenciarTelas gerenciarTelas;
    private JLabel titulo;
    private JButton editCarsButton;
    private JButton editClientsButton;
    private JButton dealershipButton;

    public void screen(Loja loja) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); // Definindo o tamanho da tela
        setLocationRelativeTo(null); // Centralizando a tela
        gerenciarTelas = new GerenciarTelas();

         cadastroCarroButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(1, loja);
                dispose();
            }
        });
        cadastroClienteButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(2, loja);
                dispose();
            }
        });
        editCarsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(3, loja);
                dispose();
            }
        });
        editClientsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(4, loja);
                dispose();
            }
        });
        dealershipButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(5, loja);
                dispose();
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }

    public JPanel getJPanel() {
        return contentPane;
    }

}
