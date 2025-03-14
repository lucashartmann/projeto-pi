package telas;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import dados.Loja;

public class TelaEditarFornecedores extends JDialog {
    private JPanel contentPane;
    private JButton editButton;
    private JLabel cpfText;
    private JTextField fieldCPF;
    private JTextField fieldName;
    private JButton backButton;
    private JTextField fieldResult;
    private JLabel nameText;
    private JTextField newFieldCPF;
    private JTextField newFieldName;
    private JLabel newCpfText;
    private JLabel newNameText;
    private JButton buttonOK;
    private JButton buttonCancel;
    private GerenciarTelas gerenciarTelas;

    public void telaEditarClientes(Loja loja) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); //Tamanho da tela
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();

        backButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(0, loja);
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
