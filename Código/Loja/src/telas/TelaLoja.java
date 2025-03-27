package telas;

import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JPanel;
import javax.swing.JTextField;

import banco.OperacoesBanco;

public class TelaLoja extends JDialog {
    private JPanel contentPane;
    private JButton voltarButton, allDataButton, pesquisarButton;
    private GerenciarTelas gerenciarTelas;
    private JTextField campoPesquisa, campoResultado;

    public void telaLoja(OperacoesBanco operacoesBanco) {
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
        allDataButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
               // String resultadoConsulta = "Quantidade de produtos: " + operacoesBanco.getQuantProdutos() +
               //         "\nQuantidade de clientes:" + operacoesBanco.getQuantidadeClientes() + "\nQuantidade de fornecedores" +
               //         operacoesBanco.getQuantFornecedores() +"\nQuantidade de funcionarios" + operacoesBanco.getQuantFuncionarios();
               // campoResultado.setText(resultadoConsulta);
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}
