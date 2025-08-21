from textual.widgets import Input, Label, Button, TabbedContent, TabPane, Footer, Header, Select
from textual.screen import Screen
from textual.containers import Container, HorizontalGroup
from controller import Controller
from textual import on


class TelaCadastrar(Container):
    def compose(self):
        with HorizontalGroup():
            yield Label("Nome:", id="lbl_nome")
            yield Input(placeholder="Nome aqui", id="inpt_nome")
            yield Label("Marca:")
            yield Input(placeholder="Marca aqui", id="inpt_marca")
        with HorizontalGroup():
            yield Label("Modelo:", id="lbl_modelo")
            yield Input(placeholder="Modelo aqui", id="inpt_modelo")
            yield Label("Cor:", id="lbl_cor")
            yield Input(placeholder="Cor aqui", id="inpt_cor")
        with HorizontalGroup():
            yield Label("Preço:", id="lbl_preco")
            yield Input(placeholder="Preço aqui", id="inpt_preco")
            yield Label("Quantidade:", id="lbl_quant")
            yield Input(placeholder="Quantidade aqui", id="inpt_quant")
        with HorizontalGroup(id="categoria_slot"):
            yield Select([("produto", 'produto')])
        with HorizontalGroup():
            yield Button("Limpar", id="bt_limpar")
            yield Button("Cadastrar", id="bt_cadastrar")
            yield Button("Voltar", id="bt_voltar")

    def cadastro(self):
        dados = []
        for input in self.query(Input):
            dados.append(input.value.upper())
        if self.screen.valor_select != "Nova categoria":
            dados.append(self.screen.valor_select)
        elif self.screen.montou:
            dados.append(self.query_one("#inpt_categoria", Input).value)
        else:
            dados.append("")
        resultado = Controller.cadastrar_produto(Controller, dados)
        self.notify(str(resultado), markup=False)
        self.screen.on_mount()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_cadastrar":
                if self.screen.montou:
                    self.screen.montou = False
                    self.query_one("#lbl_categoria").remove()
                    self.query_one("#inpt_categoria").remove()
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
                mensagem = Controller.remover_produto(
                    Controller, input_id)
                self.notify(str(mensagem), markup=False)


class TelaEditar(Container):

    def compose(self):
        with HorizontalGroup():
            yield Label("ID do Produto:", id="lbl_id")
            yield Input(placeholder="ID aqui", id="input_id")
            yield Label("Nome:", id="lbl_nome")
            yield Input(placeholder="Nome aqui", id="inpt_nome")
        with HorizontalGroup():
            yield Label("Marca:", id="lbl_marca")
            yield Input(placeholder="Marca aqui", id="inpt_marca")
            yield Label("Modelo:", id="lbl_modelo")
            yield Input(placeholder="Modelo aqui", id="inpt_modelo")
        with HorizontalGroup():
            yield Label("Cor:", id="lbl_cor")
            yield Input(placeholder="Cor aqui", id="inpt_cor")
            yield Label("Preço:", id="lbl_preco")
            yield Input(placeholder="Preço aqui", id="inpt_preco")
        with HorizontalGroup():
            yield Label("Quantidade:", id="lbl_quant")
            yield Input(placeholder="Quantidade aqui", id="inpt_quant")
        with HorizontalGroup(id="categoria_slot"):
            yield Select([("produto", 'produto')])
        with HorizontalGroup():
            yield Button("Editar", id="bt_editar")
            yield Button("Limpar", id="bt_limpar")
            yield Button("Voltar", id="bt_voltar")

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_editar":
                if self.screen.montou:
                    self.screen.montou = False
                    self.query_one("#lbl_categoria").remove()
                    self.query_one("#inpt_categoria").remove()
                input_id = self.query_one("#input_id", Input).value
                dados = []
                for input in self.query(Input)[1:]:
                    dados.append(input.value.upper())
                if self.screen.valor_select != "Nova categoria":
                    dados.append(self.screen.valor_select)
                elif self.screen.montou:
                    dados.append(self.query_one(
                        "#inpt_categoria", Input).value)
                else:
                    dados.append("")
                mensagem = Controller.editar_produto(
                    Controller, input_id, dados)
                self.notify(str(mensagem), markup=False)
                self.screen.on_mount()


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

    montou = False
    valor_select = ""

    def on_mount(self):
        produtos = Controller.ver_produtos_estoque(Controller)
        lista_categorias = []
        for produto in produtos:
            if produto.get_categoria() not in lista_categorias:
                lista_categorias.append(produto.get_categoria())
        if "Nova categoria" not in lista_categorias:
            lista_categorias.append("Nova categoria")
        for select in self.query(Select):
            select.set_options(
                [(categoria, categoria) for categoria in lista_categorias])

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        self.valor_select = str(evento.value)
        select = evento._sender
        container = select.parent
        if self.valor_select == "Nova categoria" and not self.montou:
            container.mount(Label("Categoria:", id="lbl_categoria"))
            container.mount(
                Input(placeholder="Categoria aqui", id="inpt_categoria"))
            self.montou = True
        elif self.valor_select != "Nova categoria" and self.montou:
            self.query_one("#lbl_categoria").remove()
            self.query_one("#inpt_categoria").remove()
            self.montou = False
