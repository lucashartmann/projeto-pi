package telas;

import banco.OperacoesBanco;

public class GerenciarTelas {

    public void trocarTela(int trocaTela, OperacoesBanco operacoesBanco) {
        TelaMenuPrincipal menu = new TelaMenuPrincipal();
        TelaCadastroProduto cadastro_produto = new TelaCadastroProduto();
        TelaCadastroCliente cadastro_cliente = new TelaCadastroCliente();
        TelaLoja dadosLoja = new TelaLoja();
        TelaEditarProduto editarProduto = new TelaEditarProduto();
        TelaEditarClientes editarClientes = new TelaEditarClientes();

        switch (trocaTela) {
            case 0:
                menu.screen(operacoesBanco);
                break;
            case 1:
                cadastro_produto.screen(operacoesBanco);
                break;
            case 2:
                cadastro_cliente.screen(operacoesBanco);
                break;
            case 3:
                editarProduto.telaEditarprodutos(operacoesBanco);
                break;
            case 4:
                editarClientes.telaEditarClientes(operacoesBanco);
                break;
            case 5:
                dadosLoja.telaLoja(operacoesBanco);
                break;
            default:
                break;
        }
    }
}
