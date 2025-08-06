from textual.widgets import Input, Label, Button, TabbedContent, TabPane, Footer, Header
from textual.screen import Screen
from textual.containers import HorizontalGroup, Container, VerticalGroup
from controller.Controller import Controller


class TelaCadastrar(Container):
    def compose(self):
        with HorizontalGroup():
            with VerticalGroup():
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
            with VerticalGroup():
                yield Button("Limpar", id="bt_limpar")
                yield Button("Cadastrar", id="bt_cadastrar")
                yield Button("Voltar", id="bt_voltar")


class TelaRemover(Container):
    def compose(self):
        yield Button("Limpar", id="bt_limpar")
        yield Button("Remover", id="bt_remover")
        yield Button("Voltar", id="bt_voltar")


class TelaEditar(Container):
    produto = None

    def compose(self):
        with HorizontalGroup():
            with VerticalGroup():
                with HorizontalGroup():
                    yield Label("ID do Produto:", id="lb_id")
                    yield Input(placeholder="ID aqui")
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
            with VerticalGroup():
                yield Button("Limpar", id="bt_limpar")
                yield Button("Editar", id="bt_editar")
                yield Button("Voltar", id="bt_voltar")

    def on_input_changed(self, evento: Input.Changed):
        if len(evento.value) == 2:
            for produto in Controller.get_lista_produtos():
                if produto.get_id() == evento.value:
                    self.produto = produto
                    break

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_editar":
                if self.produto is not None:
                    dados = []
                    for input in self.query(Input):
                        dados.append(input.value)
                    if dados[4] != "":
                        try:
                            float(dados[4])
                        except ValueError:
                            self.notify(f"O valor {dados[4]} está incorreto")
                            return
                    if dados[5] != "":
                        try:
                            int(dados[5])
                        except ValueError:
                            self.notify(f"O valor {dados[5]} está incorreto")
                            return
                    mensagem = Controller.editar_produto(self.produto, dados)
                    self.notify(mensagem)
                    self.produto = None


class TelaProduto(Screen):
    CSS_PATH = "css/TelaProduto.tcss"
    
    def compose(self):
        yield Header()
        with TabbedContent():
            with TabPane("Cadastrar"):
                yield TelaCadastrar()
            with TabPane("Editar"):
                yield TelaEditar()
            with TabPane("Remover"):
                yield TelaRemover()
        yield Footer()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_voltar":
                self.screen.app.switch_screen("tela_inicial")
            case "bt_cadastrar":
                self.cadastro()
            case "bt_limpar":
                for input in self.query(Input):
                    input.value = ""

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
            return
        resultado = Controller.cadastrar_produto(
            dados[0], dados[1], dados[2], dados[3], preco, quant)
        self.notify(resultado)
