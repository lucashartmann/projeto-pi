from textual.app import App
from view import TelaLogin
from database import Banco
from view import TelaCadastro, TelaConsulta, TelaPerfil
from controller import Controller
from model import Init

class App(App):

    SCREENS = {
        "tela_login": TelaLogin.Login,
        "tela_cadastro": TelaCadastro.TelaCadastro,
        "tela_consultar": TelaConsulta.TelaConsulta,
        "tela_perfil": TelaPerfil.TelaPerfil
    }

    def on_mount(self):

        dados = Banco.Banco.carregar_login()
        if dados:
            logon = Controller.carregar_login(dados)
            Init.inicializar()
            if "ERRO!" in logon:
                self.notify(logon)
            else:
                self.push_screen("tela_cadastro")
        else:
            self.push_screen("tela_login")

  