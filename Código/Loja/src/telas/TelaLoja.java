package telas;

import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JPanel;
import javax.swing.JTextField;

import banco.OperacoesBanco;

public class TelaLoja extends JDialog {
    private JPanel contentPane;
    private JButton vehiclesButton;
    private JButton clientsButton;
    private JTextField fieldResult;
    private JButton backButton;
    private JButton allDataButton;
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
        vehiclesButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String resultadoConsulta = "Quantidade de produtos: " + operacoesBanco.getQuantidadeProdutos() + "\n"
                        + operacoesBanco.listaProdutos();
                fieldResult.setText(resultadoConsulta);
            }
        });
        clientsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String resultadoConsulta = "Quantidade de clientes: " + operacoesBanco.getQuantidadeClientes() + "\n"
                        + operacoesBanco.consultarClientes();
                fieldResult.setText(resultadoConsulta);
            }
        });
        allDataButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String resultadoConsultaProdutos = "Quantidade de produtos: " + operacoesBanco.getQuantidadeProdutos()
                        + "\n" + operacoesBanco.listaProdutos();
                String resultadoConsultaClientes = "Quantidade de clientes: " + operacoesBanco.getQuantidadeClientes()
                        + "\n" + operacoesBanco.consultarClientes();
                fieldResult.setText(resultadoConsultaProdutos + "\n" + resultadoConsultaClientes);
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}
