package telas;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

import banco.OperacoesBanco;

public class TelaEditarFornecedores extends JDialog {
    private JPanel contentPane;
    private JTextField fieldCPF, fieldName, fieldResult;
    private JLabel nameText, cpfText;
    private JTextField newFieldCPF, newFieldName;
    private JLabel newCpfText, newNameText;
    private JButton buttonOK, buttonCancel, editButton, backButton;
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
