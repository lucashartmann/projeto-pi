package telas;

import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JPanel;
import javax.swing.JTextField;

import banco.OperacoesBanco;

public class TelaLoja extends JDialog {
    private JPanel contentPane;
    private JButton vehiclesButton, clientsButton;
    private JButton backButton, allDataButton;
    private JTextField fieldResult;
    private GerenciarTelas gerenciarTelas;

    public void telaLoja(OperacoesBanco operacoesBanco) {
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
        dadosButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String resultadoConsulta = "Quantidade de produtos: " + operacoesBanco.getQuantidadeProdutos() +
                        "\nQuantidade de clientes:" + "\nQuantidade de fornecedores" +
                        ;
                fieldResult.setText(resultadoConsulta);
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}
