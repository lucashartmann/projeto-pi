from textual.widgets import Input, Pretty, TextArea, Button, Footer, Header
from textual.screen import Screen
from textual.containers import HorizontalGroup
from controller import Controller


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

    clientes = Controller.get_clientes_cadastrados()
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

            for palavra in palavras:
                match palavra:

                    case "NOME:":
                        index = palavras.index("NOME:")
                        if index + 1 < len(palavras):
                            nome_busca = " ".join((palavras[index+1:]))
                            if "," in nome_busca:
                                nome_busca = nome_busca[0:nome_busca.index(
                                    ",")]
                            if len(self.clientes_filtrados) > 0:
                                clientes_temp = []
                                for cliente in self.clientes_filtrados:
                                    if nome_busca in cliente.get_nome():
                                        clientes_temp.append(cliente)
                                if len(clientes_temp) > 0:
                                    self.clientes_filtrados = clientes_temp
                            else:
                                for cliente in self.clientes:
                                    if nome_busca in cliente.get_nome():
                                        self.clientes_filtrados.append(cliente)

                    case "CPF:":
                        index = palavras.index("CPF:")
                        if index + 1 < len(palavras):
                            valor_cpf = " ".join((palavras[index+1:]))
                            if "," in valor_cpf:
                                valor_cpf = valor_cpf[0:valor_cpf.index(
                                    ",")]
                            if len(self.clientes_filtrados) > 0:
                                clientes_temp = []
                                for cliente in self.clientes_filtrados:
                                    if valor_cpf in cliente.get_cpf():
                                        clientes_temp.append(cliente)
                                if len(clientes_temp) > 0:
                                    self.clientes_filtrados = clientes_temp
                            else:
                                for cliente in self.clientes:
                                    if valor_cpf in cliente.get_cpf():
                                        self.clientes_filtrados.append(
                                            cliente)

                    case "RG:":
                        index = palavras.index("RG:")
                        if index + 1 < len(palavras):
                            rg_busca = " ".join((palavras[index+1:]))
                            if "," in rg_busca:
                                rg_busca = rg_busca[0:rg_busca.index(
                                    ",")]
                            if len(self.clientes_filtrados) > 0:
                                clientes_temp = []
                                for cliente in self.clientes_filtrados:
                                    if rg_busca in cliente.get_rg():
                                        clientes_temp.append(cliente)
                                if len(clientes_temp) > 0:
                                    self.clientes_filtrados = clientes_temp
                            else:
                                for cliente in self.clientes:
                                    if rg_busca in cliente.get_rg():
                                        self.clientes_filtrados.append(cliente)

                    case "TELEFONE:":
                        index = palavras.index("TELEFONE:")
                        if index + 1 < len(palavras):
                            try:
                                telefone_busca = " ".join((palavras[index+1:]))
                                if "," in telefone_busca:
                                    telefone_busca = telefone_busca[0:telefone_busca.index(
                                        ",")]
                                telefone_busca = int(telefone_busca)
                                if len(self.clientes_filtrados) > 0:
                                    clientes_temp = []
                                    for cliente in self.clientes_filtrados:
                                        if telefone_busca == cliente.get_telefone():
                                            clientes_temp.append(cliente)
                                    if len(clientes_temp) > 0:
                                        self.clientes_filtrados = clientes_temp
                                else:
                                    for cliente in self.clientes:
                                        if telefone_busca == cliente.get_telefone():
                                            self.clientes_filtrados.append(
                                                cliente)
                            except ValueError:
                                self.notify("Valor inválido")

                    case "ENDERECO:":
                        index = palavras.index("ENDERECO:")
                        if index + 1 < len(palavras):
                            endereco_busca = " ".join((palavras[index+1:]))
                            if "," in endereco_busca:
                                endereco_busca = endereco_busca[0:endereco_busca.index(
                                    ",")]
                            if len(self.clientes_filtrados) > 0:
                                clientes_temp = []
                                for cliente in self.clientes_filtrados:
                                    if endereco_busca in cliente.get_endereco():
                                        clientes_temp.append(cliente)
                                if len(clientes_temp) > 0:
                                    self.clientes_filtrados = clientes_temp
                            else:
                                for cliente in self.clientes:
                                    if endereco_busca in cliente.get_endereco():
                                        self.clientes_filtrados.append(cliente)

                    case "EMAIL:":
                        index = palavras.index("EMAIL:")
                        if index + 1 < len(palavras) and len(palavras[index + 1]) > 3:
                            email_busca = " ".join((palavras[index+1:]))
                            if "," in email_busca:
                                email_busca = email_busca[0:email_busca.index(
                                    ",")]
                            if len(self.clientes_filtrados) > 0:
                                clientes_temp = []
                                for cliente in self.clientes_filtrados:
                                    if email_busca in cliente.get_email():
                                        clientes_temp.append(cliente)
                                if len(clientes_temp) > 0:
                                    self.clientes_filtrados = clientes_temp
                            else:
                                for cliente in self.clientes:
                                    if email_busca in cliente.get_email():
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
