from textual.widgets import Input, Pretty, TextArea, Button, Footer, Header, Select
from textual.screen import Screen
from textual.containers import HorizontalGroup
from model import Init


class TelaClientela(Screen):

    CSS_PATH = "css/TelaClientela.tcss"

    def compose(self):
        yield Header()
        with HorizontalGroup(id="hg_pesquisa"):
            yield Input()
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        with HorizontalGroup(id="container"):
            pass
        yield Footer()

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

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value.upper()
        resultado = self.query_one(Pretty)
        palavras = texto.split()

        if len(palavras) > 0:
            self.clientes_filtrados = []

            if "NOME:" in palavras:
                index = palavras.index("NOME:")
                if index + 1 < len(palavras):
                    nome_busca = palavras[index + 1]
                    if len(self.clientes_filtrados) > 0:
                        clientes_temp = []
                        for cliente in self.clientes_filtrados:
                            if cliente.get_nome() == nome_busca:
                                clientes_temp.append(cliente)
                        if len(clientes_temp) > 0:
                            self.clientes_filtrados = clientes_temp
                    else:
                        for cliente in self.clientes:
                            if cliente.get_nome() == nome_busca:
                                self.clientes_filtrados.append(cliente)

            if "CPF:" in palavras:
                index = palavras.index("CPF:")
                if index + 1 < len(palavras):
                    try:
                        valor_cpf = float(palavras[index + 1])
                        if len(self.clientes_filtrados) > 0:
                            clientes_temp = []
                            for cliente in self.clientes_filtrados:
                                if cliente.get_cpf() == valor_cpf:
                                    clientes_temp.append(cliente)
                            if len(clientes_temp) > 0:
                                self.clientes_filtrados = clientes_temp
                        else:
                            for cliente in self.clientes:
                                if cliente.get_cpf() == valor_cpf:
                                    self.clientes_filtrados.append(cliente)
                    except ValueError:
                        self.notify("Valor inválido")

            if "RG:" in palavras:
                index = palavras.index("RG:")
                if index + 1 < len(palavras):
                    rg_busca = palavras[index + 1]
                    if len(self.clientes_filtrados) > 0:
                        clientes_temp = []
                        for cliente in self.clientes_filtrados:
                            if cliente.get_rg() == rg_busca:
                                clientes_temp.append(cliente)
                        if len(clientes_temp) > 0:
                            self.clientes_filtrados = clientes_temp
                    else:
                        for cliente in self.clientes:
                            if cliente.get_rg() == rg_busca:
                                self.clientes_filtrados.append(cliente)

            if "TELEFONE:" in palavras:
                index = palavras.index("TELEFONE:")
                if index + 1 < len(palavras):
                    try:
                        telefone_busca = int(palavras[index + 1])
                        if len(self.clientes_filtrados) > 0:
                            clientes_temp = []
                            for cliente in self.clientes_filtrados:
                                if cliente.get_telefone() == telefone_busca:
                                    clientes_temp.append(cliente)
                            if len(clientes_temp) > 0:
                                self.clientes_filtrados = clientes_temp
                        else:
                            for cliente in self.clientes:
                                if cliente.get_telefone() == telefone_busca:
                                    self.clientes_filtrados.append(cliente)
                    except ValueError:
                        self.notify("Valor inválido")

            if "ENDERECO:" in palavras:
                index = palavras.index("ENDERECO:")
                if index + 1 < len(palavras):
                    endereco_busca = palavras[index + 1].upper()
                    if len(self.clientes_filtrados) > 0:
                        clientes_temp = []
                        for cliente in self.clientes_filtrados:
                            if cliente.get_endereco() == endereco_busca:
                                clientes_temp.append(cliente)
                        if len(clientes_temp) > 0:
                            self.clientes_filtrados = clientes_temp
                    else:
                        for cliente in self.clientes:
                            if cliente.get_endereco() == endereco_busca:
                                self.clientes_filtrados.append(cliente)

            if "EMAIL:" in palavras:
                index = palavras.index("EMAIL:")
                if index + 1 < len(palavras) and len(palavras[index + 1]) > 3:
                    email_busca = palavras[index + 1]
                    if len(self.clientes_filtrados) > 0:
                        clientes_temp = []
                        for cliente in self.clientes_filtrados:
                            if cliente.get_email() == email_busca:
                                clientes_temp.append(cliente)
                        if len(clientes_temp) > 0:
                            self.clientes_filtrados = clientes_temp
                    else:
                        for cliente in self.clientes:
                            if cliente.get_email() == email_busca:
                                self.clientes_filtrados.append(cliente)

            if len(self.clientes_filtrados) > 0:
                clientes_str = [str(cliente)
                                for cliente in self.clientes_filtrados]
                resultado.update(clientes_str)
                self.setup_dados()
            else:
                clientes_str = [str(cliente) for cliente in self.clientes]
                resultado.update(clientes_str)
                self.setup_dados()
        else:
            if len(self.clientes_filtrados) > 0:
                clientes_str = [str(cliente)
                                for cliente in self.clientes_filtrados]
                resultado.update(clientes_str)
                self.setup_dados()
            else:
                clientes_str = [str(cliente) for cliente in self.clientes]
                resultado.update(clientes_str)
                self.setup_dados()
