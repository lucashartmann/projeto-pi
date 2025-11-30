from textual.screen import Screen
from textual.widgets import Input, MaskedInput, TextArea, Tab, Tabs

from model import Administrador, Init, Corretor


class TelaCadastroVendaAluguel(Screen):
    CSS_PATH = "css/TelaCadastroVendaAluguel.tcss"

    def compose(self):
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif isinstance(Init.usuario_atual, Corretor.Corretor):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
