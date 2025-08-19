from textual.widgets import Input, Label, Button, TabbedContent, TabPane, Footer, Header, Select
from textual.screen import Screen
from textual.containers import Container
from controller.Controller_Telas import Controller
from model import Init
from textual import on


class TelaCadastrar(Container):
    def compose(self):
        yield Label("Nome:")
        yield Input(placeholder="Nome aqui")
        yield Label("Marca:")
        yield Input(placeholder="Marca aqui")
        yield Label("Modelo:")
        yield Input(placeholder="Modelo aqui")
        yield Label("Cor:")
        yield Input(placeholder="Cor aqui")
        yield Label("Preço:")
        yield Input(placeholder="Preço aqui")
        yield Label("Quantidade:")
        yield Input(placeholder="Quantidade aqui")
        yield Label("Categoria:")
        yield Input(placeholder="Categoria aqui")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Cadastrar", id="bt_cadastrar")
        yield Button("Voltar", id="bt_voltar")

    def cadastro(self):
        dados = []
        for input in self.query(Input):
            if input.value == "":
                self.notify(f"{input.placeholder} está vazio, tente novamente")
                return
            dados.append(input.value.upper())
        resultado = Controller.cadastrar_produto(Controller, dados)
        self.notify(resultado)

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_cadastrar":
                self.cadastro()


class TelaRemover(Container):
    def compose(self):
        yield Label("ID do Produto:", id="lb_id")
        yield Input(placeholder="ID aqui", id="input_id")
        yield Button("Limpar", id="bt_limpar")
        yield Button("Remover", id="bt_remover")
        yield Button("Voltar", id="bt_voltar")

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_remover":
                input_id = self.query_one("#input_id").value
                if len(input_id) >= 1:
                    input_id = int(input_id)
                    produto = Init.loja.get_produto_por_id(input_id)
                    if not produto:
                        self.notify(
                            f"Produto com id {input_id} não encontrado")
                    else:
                        mensagem = Controller.remover_produto(
                            Controller, produto)
                        self.notify(mensagem)
                else:
                    self.notify("ID precisa ter no minimo 1 digitos")


class TelaEditar(Container):
    montou = False

    def compose(self):
        yield Label("ID do Produto:", id="lb_id")
        yield Input(placeholder="ID aqui", id="input_id")
        yield Label("Nome:")
        yield Input(placeholder="Nome aqui")
        yield Label("Marca:")
        yield Input(placeholder="Marca aqui")
        yield Label("Modelo:")
        yield Input(placeholder="Modelo aqui")
        yield Label("Cor:")
        yield Input(placeholder="Cor aqui")
        yield Label("Preço:")
        yield Input(placeholder="Preço aqui")
        yield Label("Quantidade:")
        yield Input(placeholder="Quantidade aqui")
        yield Select([("produto", 'produto')])
        yield Button("Limpar", id="bt_limpar")
        yield Button("Editar", id="bt_editar")
        yield Button("Voltar", id="bt_voltar")

    def on_mount(self):
        produtos = Controller.ver_produtos_estoque(Controller)
        lista_categorias = []
        for produto in produtos:
            if produto.get_categoria() not in lista_categorias:
                lista_categorias.append(produto.get_categoria())
        if "Nova categoria" not in lista_categorias:
            lista_categorias.append("Nova categoria")
        self.query_one(Select).set_options(
            [(categoria, categoria) for categoria in lista_categorias])

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        valor_select = str(evento.value)
        if valor_select == "Nova categoria":
            self.mount(Label("Categoria", id="lbl_categoria"))
            self.mount(Input(placeholder="Categoria aqui", id="inpt_categoria"))
            self.montou = True

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_editar":
                if self.montou:
                    self.montou = False
                    self.query_one("#lbl_categoria").remove()
                    self.query_one("#inpt_categoria").remove()
                input_id = self.query_one("#input_id").value
                if len(input_id) >= 1:
                    input_id = int(input_id)
                    produto = Init.loja.get_produto_por_id(input_id)
                    if not produto:
                        self.notify(
                            f"Produto com id {input_id} não encontrado")
                    else:
                        dados = []
                        for input in self.query(Input)[1:]:
                            dados.append(input.value.upper())
                        mensagem = Controller.editar_produto(
                            Controller, produto, dados)
                        self.notify(mensagem)
                else:
                    self.notify("ID precisa ter no minimo 1 digitos")


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
            case "bt_limpar":
                for input in self.query(Input):
                    input.value = ""
