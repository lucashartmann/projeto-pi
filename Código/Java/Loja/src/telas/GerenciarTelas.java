package telas;

import banco.OperacoesBanco;

public class GerenciarTelas {

    public void trocarTela(int trocaTela, OperacoesBanco operacoesBanco) {
        TelaMenu menu = new TelaMenu();
        TelaProduto produto = new TelaProduto();
        TelaCliente cliente = new TelaCliente();
        TelaLoja loja = new TelaLoja();
        TelaFornecedores fornecedores = new TelaFornecedores();
        TelaFuncionarios funcionarios = new TelaFuncionarios();

        switch (trocaTela) {
            case 0:
                menu.screen(operacoesBanco);
                break;
            case 1:
                loja.telaLoja(operacoesBanco);
                break;
            case 2:
                cliente.screen(operacoesBanco);
                break;
            case 3:
                produto.screen(operacoesBanco);
                break;
            case 4:
                fornecedores.tela(operacoesBanco);
                break;
            case 5:
                funcionarios.tela(operacoesBanco);
                break;
            default:
                break;
        }
    }
}
