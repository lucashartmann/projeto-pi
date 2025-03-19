package telas;

import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

import banco.OperacoesBanco;

public class TelaEditarClientes extends JDialog {
    private JPanel contentPane;
    private JLabel cpfText;
    private JTextField fieldCPF, fieldName, fieldResult, newFieldCPF,newFieldName;
    private JLabel nameText;
    private JLabel newCpfText, newNameText;
    private JButton buttonOK, buttonCancel, backButton, editButton;
    private GerenciarTelas gerenciarTelas;

    public void telaEditarClientes(OperacoesBanco operacoesBanco) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); // Tamanho da tela
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();

        backButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(0, operacoesBanco);
                dispose();
            }
        });
        editButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {

            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }

}
