package dados;

import banco.OperacoesBanco;
import telas.GerenciarTelas;

public class App {
    public void executar() {
        OperacoesBanco operacoesBanco = new OperacoesBanco();
        GerenciarTelas gerenciarTelas = new GerenciarTelas();
        gerenciarTelas.trocarTela(0, operacoesBanco);
    }
}
