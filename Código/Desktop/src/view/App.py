from textual.app import App
from view import TelaCadastro, TelaConsulta
from view import TelaLogin


class App(App):
    SCREENS = {
        "tela_consulta": TelaCadastro.TelaCadastro,
        "tela_cadastro": TelaConsulta.TelaConsulta,
        "tela_login": TelaLogin.Login
    }

    def on_mount(self):
        self.push_screen("tela_login")
