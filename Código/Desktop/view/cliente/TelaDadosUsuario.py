# Compras recentes de usuario
# Dados de login

from textual.screen import Screen
from textual.widgets import TextArea, Pretty
from textual.containers import HorizontalGroup

from textual_image.widget import Image

from model import Init


class TelaDadosUsuario(Screen):

    CSS_PATH = "css/TelaDadosUsuario.css"

    dados = f'''
    Username {Init.usuario.get_nome()}
    Nome {Init.cliente_atual.get_nome()}
    CPF {Init.cliente_atual.get_cpf()}
    RG {Init.cliente_atual.get_rg()}
    Telefone {Init.cliente_atual.get_telefone()}
    Endereco {Init.cliente_atual.get_endereco()}
    Email {Init.usuario.get_email()}
    Senha {Init.usuario.get_senha()}
    '''

    compras = Init.loja.get_compras_usuario_por_cpf(
        Init.cliente_atual.get_cpf())

    def dados_compra(self):
        for chave, valor in self.compras.items():
            dados = ''

            dados += f"Data da Compra: {chave}\n"
            for produto in valor:
                dados += f"{produto}\n"

            if dados:
                self.mount(Pretty(dados))

    def atualizar_compras(self):
        self.compras = Init.loja.get_compras_usuario_por_cpf(
            Init.cliente_atual.get_cpf())

    def compose(self):
        with HorizontalGroup():
            yield Image("assets/usuario.png")
            yield TextArea(self.dados)
        yield TextArea("Compras recentes do usuário")
