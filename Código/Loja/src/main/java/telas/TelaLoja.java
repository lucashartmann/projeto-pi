package telas;

import dados.Loja;
import java.awt.event.*;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JPanel;
import javax.swing.JTextField;

public class TelaLoja extends JDialog {
    private JPanel contentPane;
    private JButton vehiclesButton;
    private JButton clientsButton;
    private JTextField fieldResult;
    private JButton backButton;
    private JButton allDataButton;
    private GerenciarTelas gerenciarTelas;
    private GaragemCarros garagem;

    public void telaLoja(Loja loja) {
        setVisible(true);
        setContentPane(contentPane);
        setModal(true);
        setSize(700, 600); //Tamanho da tela
        setLocationRelativeTo(null);
        gerenciarTelas = new GerenciarTelas();
        garagem = loja.getGaragem();

        backButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                gerenciarTelas.trocarTela(0, loja);
                dispose();
            }
        });
        vehiclesButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String resultadoConsulta = "Quantidade de carros: " + garagem.getQuantidadeCarros() + "\n" + garagem.listaCarros();
                fieldResult.setText(resultadoConsulta);
            }
        });
        clientsButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e){
                String resultadoConsulta = "Quantidade de clientes: " + loja.getQuantidadeClientes() + "\n" + loja.listaClientes();
                fieldResult.setText(resultadoConsulta);
            }
        });
        allDataButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e){
                String resultadoConsultaCarros = "Quantidade de carros: " + garagem.getQuantidadeCarros() + "\n" + garagem.listaCarros();
                String resultadoConsultaClientes = "Quantidade de clientes: " + loja.getQuantidadeClientes() + "\n" + loja.listaClientes();
                fieldResult.setText(resultadoConsultaCarros + "\n" + resultadoConsultaClientes);
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}
