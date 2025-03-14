package telas;

import dados.Loja;

public class GerenciarTelas {

    public void trocarTela(int trocaTela, Loja loja) {
        TelaMenuPrincipal menu = new TelaMenuPrincipal();
        TelaCadastroProduto cadastro_produto = new TelaCadastroProduto();
        TelaCadastroCliente cadastro_cliente = new TelaCadastroCliente();
        TelaLoja dadosLoja = new TelaLoja();
        TelaEditarProduto editarProduto = new TelaEditarProduto();
        TelaEditarClientes editarClientes = new TelaEditarClientes();

        switch (trocaTela) {
            case 0:
                menu.screen(loja);
                break;
            case 1:
                cadastro_produto.screen(loja);
                break;
            case 2:
                cadastro_cliente.screen(loja);
                break;
            case 3:
                editarProduto.telaEditarprodutos(loja);
                break;
            case 4:
                editarClientes.telaEditarClientes(loja);
                break;
            case 5:
                dadosLoja.TelaLoja(loja);
                break;
            default:
                break;
        }
    }
}
