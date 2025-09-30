from textual.widgets import Input, Pretty, TextArea, Button, Select
from textual.containers import HorizontalGroup, Container
from textual import on
from model import Init


class TelaEstoque(Container):

    def compose(self):
        with HorizontalGroup(id="hg_pesquisa"):
            yield Select([("produto", 'produto')])
            yield Input()
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        with HorizontalGroup(id="container"):
            pass

    produtos = Init.loja.get_estoque().get_lista_produtos()
    produtos_filtrados = []
    filtrou_select = False
    filtrou_input = False
    select_evento = ""

    def setup_dados(self):
        if len(self.produtos_filtrados) > 0:
            quant = len(self.produtos_filtrados)
        else:
            quant = len(self.produtos)
        self.query_one(TextArea).text = f"Quantidade de produtos: {quant}"

    def on_mount(self):
        self.produtos = Init.loja.get_estoque().get_lista_produtos()
        produtos_str = [str(produto) for produto in self.produtos]
        self.mount(Pretty(produtos_str))
        self.setup_dados()

    def on_button_pressed(self):
        self.screen.app.switch_screen("tela_inicial")

    def atualizar(self):
        resultado = self.query_one(Pretty)

        if len(self.produtos_filtrados) > 0 and self.filtrou_select == False:
            produtos_str = [str(produto)
                            for produto in self.produtos_filtrados]
            resultado.update(produtos_str)
            self.setup_dados()
        elif self.filtrou_select:
            self.select_changed(self.select_evento)
        else:
            produtos_str = [str(produto) for produto in self.produtos]
            resultado.update(produtos_str)
            self.setup_dados()

    @on(Select.Changed)
    def select_changed(self, evento: Select.Changed):
        if evento.select.is_blank():
            if self.filtrou_input == False and self.filtrou_select:
                self.produtos_filtrados = []
            produtos_str = [str(produto) for produto in self.produtos]
            self.query_one(Pretty).update(produtos_str)
            self.setup_dados()
            self.filtrou_select = False
        else:
            valor_select = str(evento.value)
            valor_antigo = ""
            if valor_select != valor_antigo and self.filtrou_input == False and self.filtrou_select:
                self.produtos_filtrados = []
                valor_antigo = valor_select
            if len(self.produtos_filtrados) == 0:
                for produto in self.produtos:
                    if produto.get_categoria() == valor_select:
                        self.produtos_filtrados.append(produto)
            else:
                produtos_temp = []
                for produto in self.produtos_filtrados:
                    if produto.get_categoria() == valor_select:
                        produtos_temp.append(produto)
                if len(produtos_temp) > 0:
                    self.produtos_filtrados = produtos_temp

            produtos_str = [str(produto)for produto in self.produtos_filtrados]
            self.query_one(Pretty).update(produtos_str)
            self.setup_dados()
            self.filtrou_select = True
            self.select_evento = evento

    def filtro(self, palavras, index, filtro_recebido):
        lista_filtros = ["valor", "quantidade", "id"]
        campo = f"get_{filtro_recebido}"
        nova_lista = []

        if index + 1 < len(palavras):
            filtro = " ".join((palavras[index+1:]))

            if "," in filtro:
                filtro = filtro[0:filtro.index(
                    ",")]
            if "-" in filtro.split():
                for palavraa in filtro.split("-"):
                    if filtro.index("-")+1 < len(filtro) and palavraa not in nova_lista:
                        nova_lista.append(palavraa.strip())

            if filtro_recebido in lista_filtros:
                try:
                    if filtro_recebido == "valor":
                        filtro = float(filtro)
                    else:
                        filtro = int(filtro)
                except ValueError:
                    self.notify("Valor Inválido")
                    return

            if len(self.produtos_filtrados) > 0:
                produtos_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.produtos_filtrados:
                            if not isinstance(filtro, str):
                                if p == getattr(produto, campo)() and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                            else:
                                if p in getattr(produto, campo)() and produto not in produtos_temp:
                                    produtos_temp.append(
                                        produto)
                else:
                    for produto in self.produtos_filtrados:
                        if not isinstance(filtro, str):
                            if filtro == getattr(produto, campo)() and produto not in produtos_temp:
                                produtos_temp.append(produto)
                        else:
                            if filtro in getattr(produto, campo)() and produto not in produtos_temp:
                                produtos_temp.append(produto)
                if len(produtos_temp) > 0:
                    self.produtos_filtrados = produtos_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for produto in self.produtos:
                            if not isinstance(filtro, str):
                                if p == getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                    self.produtos_filtrados.append(
                                        produto)
                            else:
                                if p in getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                    self.produtos_filtrados.append(
                                        produto)
                else:
                    for produto in self.produtos:
                        if not isinstance(filtro, str):
                            if filtro == getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)
                        else:
                            if filtro in getattr(produto, campo)() and produto not in self.produtos_filtrados:
                                self.produtos_filtrados.append(produto)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        palavras = texto.split()

        if len(palavras) > 0:
            if self.filtrou_select == False:
                self.produtos_filtrados = []

            for palavra in palavras:
                match palavra:

                    case "MARCA:":
                        index = palavras.index("MARCA:")
                        self.filtro(palavras, index, "marca")

                    case "VALOR:":
                        index = palavras.index("VALOR:")
                        self.filtro(palavras, index, "valor")

                    case "NOME:":
                        index = palavras.index("NOME:")
                        self.filtro(palavras, index, "nome")

                    case "QUANTIDADE:":
                        index = palavras.index("QUANTIDADE:")
                        self.filtro(palavras, index, "quantidade")

                    case "MODELO:":
                        index = palavras.index("MODELO:")
                        self.filtro(palavras, index, "modelo")

                    case "COR:":
                        index = palavras.index("COR:")
                        self.filtro(palavras, index, "cor")

                    case "ID:":
                        index = palavras.index("ID:")
                        self.filtro(palavras, index, "id")

                    case "CATEGORIA:":
                        index = palavras.index("CATEGORIA:")
                        self.filtro(palavras, index, "categoria")

                self.atualizar()
        else:

            self.atualizar()
