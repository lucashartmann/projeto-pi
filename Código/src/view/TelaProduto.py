from textual.widgets import Input, Pretty, TextArea, Label, Button
from textual.screen import Screen
from textual.containers import HorizontalGroup, VerticalGroup
from controller.Controller import Controller


class TelaProduto(Screen):
    def compose(self):
        with HorizontalGroup():
            yield Label("Nome:")
            yield Input(placeholder="Nome aqui")
        with HorizontalGroup():
            yield Label("Marca:")
            yield Input(placeholder="Marca aqui")
        with HorizontalGroup():
            yield Label("Modelo:")
            yield Input(placeholder="Modelo aqui")
        with HorizontalGroup():
            yield Label("Cor:")
            yield Input(placeholder="Cor aqui")
        with HorizontalGroup():
            yield Label("Preço:")
            yield Input(placeholder="Preço aqui")
        with HorizontalGroup():
            yield Label("Quantidade:")
            yield Input(placeholder="Quantidade aqui")
        yield Button("Cadastrar")
        yield Button("Voltar", id="bt_voltar")
        
    def on_button_pressed(self):
        self.screen.app.switch_screen("tela_inicial")

    def cadastro(self):
        dados = []
        for input in self.query(Input):
            dados.append(input.value)
        try:
            preco = float(dados[4])
            quant = int(dados[5])
        except ValueError:
            self.notify(
                f"Um dos valores seguintes estão errados: {dados[4]} ou {dados[5]}")
        resultado = Controller.cadastrar_produto(
            dados[0], dados[1], dados[2], dados[3], preco, quant)
        self.notify(resultado)
