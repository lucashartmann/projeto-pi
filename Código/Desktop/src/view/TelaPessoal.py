from textual.widgets import Input, Pretty, TextArea, Button, Select
from textual.containers import HorizontalGroup, Container
from model import Init


class TelaPessoal(Container):

    def compose(self):
        with HorizontalGroup(id="hg_pesquisa"):
            yield Select([("Cliente", "Cliente"), ("Funcionário", "Funcionário")])
            yield Input()
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        with HorizontalGroup(id="container"):
            pass

    clientes = Init.loja.get_lista_clientes()
    clientes_filtrados = []

    def setup_dados(self):
        if len(self.clientes_filtrados) > 0:
            quant = len(self.clientes_filtrados)
        else:
            quant = len(self.clientes)
        self.query_one(TextArea).text = f"Quantidade de clientes: {quant}"

    def on_mount(self):
        clientes_str = [str(cliente) for cliente in self.clientes]
        self.mount(Pretty(clientes_str))
        self.setup_dados()

    def on_button_pressed(self):
        self.screen.app.switch_screen("tela_inicial")

    def atualizar(self):
        resultado = self.query_one(Pretty)

        if len(self.clientes_filtrados) > 0:
            clientes_str = [str(cliente)
                            for cliente in self.clientes_filtrados]
            resultado.update(clientes_str)
            self.setup_dados()
        else:
            clientes_str = [str(cliente) for cliente in self.clientes]
            resultado.update(clientes_str)
            self.setup_dados()

    def filtro(self, palavras, index, filtro_recebido):
        lista_filtros = []
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

            if len(self.clientes_filtrados) > 0:
                clientes_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for cliente in self.clientes_filtrados:
                            if not isinstance(filtro, str):
                                if p == getattr(cliente, campo)() and cliente not in clientes_temp:
                                    clientes_temp.append(
                                        cliente)
                            else:
                                if p in getattr(cliente, campo)() and cliente not in clientes_temp:
                                    clientes_temp.append(
                                        cliente)
                else:
                    for cliente in self.clientes_filtrados:
                        if not isinstance(filtro, str):
                            if filtro == getattr(cliente, campo)() and cliente not in clientes_temp:
                                clientes_temp.append(cliente)
                        else:
                            if filtro in getattr(cliente, campo)() and cliente not in clientes_temp:
                                clientes_temp.append(cliente)
                if len(clientes_temp) > 0:
                    self.clientes_filtrados = clientes_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for cliente in self.clientes:
                            if not isinstance(filtro, str):
                                if p == getattr(cliente, campo)() and cliente not in self.clientes_filtrados:
                                    self.clientes_filtrados.append(
                                        cliente)
                            else:
                                if p in getattr(cliente, campo)() and cliente not in self.clientes_filtrados:
                                    self.clientes_filtrados.append(
                                        cliente)
                else:
                    for cliente in self.clientes:
                        if not isinstance(filtro, str):
                            if filtro == getattr(cliente, campo)() and cliente not in self.clientes_filtrados:
                                self.clientes_filtrados.append(cliente)
                        else:
                            if filtro in getattr(cliente, campo)() and cliente not in self.clientes_filtrados:
                                self.clientes_filtrados.append(cliente)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        palavras = texto.split()

        if len(palavras) > 0:
            self.clientes_filtrados = []

            for palavra in palavras:
                match palavra:

                    case "NOME:":
                        index = palavras.index("NOME:")
                        self.filtro(palavras, index, "nome")

                    case "CPF:":
                        index = palavras.index("CPF:")
                        self.filtro(palavras, index, "cpf")

                    case "RG:":
                        index = palavras.index("RG:")
                        self.filtro(palavras, index, "rg")

                    case "TELEFONE:":
                        index = palavras.index("TELEFONE:")
                        self.filtro(palavras, index, "telefone")

                    case "ENDERECO:":
                        index = palavras.index("ENDERECO:")
                        self.filtro(palavras, index, "endereco")

                    case "EMAIL:":
                        index = palavras.index("EMAIL:")
                        self.filtro(palavras, index, "email")

                self.atualizar()
        else:
            self.atualizar()
