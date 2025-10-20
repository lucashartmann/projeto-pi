from textual.app import App
from view import TelaLogin
from database import Shelve
from view import TelaCadastro, TelaConsulta, TelaPerfil
from controller import Controller

class App(App):

    SCREENS = {
        "tela_login": TelaLogin.Login,
        "tela_cadastro": TelaCadastro.TelaCadastro,
        "tela_consultar": TelaConsulta.TelaConsulta,
        "tela_perfil": TelaPerfil.TelaPerfil
    }

    def on_mount(self):
        dados = Shelve.carregar("dados.db", "login")
        if dados:
            logon = Controller.carregar_login(dados)
            if "ERRO!" in logon:
                self.notify(logon)
            else:
                self.push_screen("tela_cadastro")
        else:
            self.push_screen("tela_login")

  