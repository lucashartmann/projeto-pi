package telas;

import banco.OperacoesBanco;
import dados.Cliente;
import dados.Funcionario;

import javax.swing.*;
import java.awt.event.*;

public class TelaFuncionarios extends JDialog {
    private JPanel contentPane;
    private JButton cadastrarButton, voltarButton, editarButton;
    private JTextField campoNome, campoResultado, campoCPF, campoRG;
    private GerenciarTelas gerenciarTelas;
    private String nome, cpf, rg;
    private Funcionario funcionario;

    public void tela(OperacoesBanco operacoesBanco) {
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
        cadastrarButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                nome = campoNome.getText();
                cpf = campoCPF.getText();
                rg = campoRG.getText();
                if (nome == null || cpf == null || rg == null) {
                    campoResultado.setText("Erro ao cadastrar. Tente novamente. " +
                            "\nFuncionário: Nome: " + nome + ", CPF: " + cpf + ", RG: " + rg);
                } else {
                    funcionario = new Funcionario(nome, cpf, rg);
                    campoResultado.setText(funcionario.toString());
                    // operacoesBanco.inserirFuncionario(funcionario);
                }
            }
        });
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }
}