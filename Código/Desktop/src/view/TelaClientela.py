from textual.widgets import Input, TextArea, Button, Select, Tab, Tabs, DataTable
from textual.containers import HorizontalGroup
from textual.screen import Screen

from model import Init, Pessoa


class TelaClientela(Screen):
    
    CSS_PATH = "css/TelaClientela.tcss"

    def compose(self):
        # TODO
        yield Tabs(Tab("TelaPerfil", id="tab_perfil"), Tab("TelaCadastrar", id="tab_cadastrar"), Tab("TelaConsultar", id="tab_consultar"))
        with HorizontalGroup(id="hg_pesquisa"):
            yield Select([("Cliente", "Cliente"), ("Funcionário", "Funcionário")])
            yield Input()
            yield Button("Voltar", id="bt_voltar")
        yield TextArea(disabled=True)
        yield DataTable()

    clientes = Init.loja.get_lista_clientes()
    clientes_filtrados = []

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        # TODO
        if event.tabs.active == self.query_one("#tab_consultar", Tab).id:
            self.app.switch_screen("tela_consultar")
        elif event.tabs.active == self.query_one("#tab_perfil", Tab).id:
            self.app.switch_screen("tela_perfil")

    def on_screen_resume(self):
        # TODO
        self.query_one(Tabs).active = self.query_one("#tab_cadastrar", Tab).id

    def setup_dados(self):
        if len(self.clientes_filtrados) > 0:
            quant = len(self.clientes_filtrados)
        else:
            quant = len(self.clientes)
        self.query_one(TextArea).text = f"Quantidade de clientes: {quant}"

    def on_button_pressed(self):
        self.screen.app.switch_screen("tela_inicial")

    def on_mount(self):
        self.ROWS = list(Pessoa.Pessoa.__dict__.keys())
        
        

    def atualizar(self):
        self.clientes = Init.loja.get_lista_clientes()
        
        if len(self.clientes_filtrados) > 0:
            lista = self.clientes_filtrados
        else:

            lista = self.clientes

        for pessoa in lista:
            lista = []
            for valor in pessoa.__dict__.values():
                lista.append(valor)
            self.ROWS.append(lista)

        table = self.query_one(DataTable)
        table.clear(columns=True)

        table.add_columns(*self.ROWS[0])

        for row in self.ROWS[1:]:
            table.add_row(*row, height=3)

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value
        palavras = texto.split()

        if len(palavras) > 0:
            self.clientes_filtrados = []
            for palavra in palavras:
                if palavra[:-1].lower() in self.ROWS[0]:
                    index = palavras.index(palavra)
                    self.filtro(palavras, index, palavra[:-1].lower())
                    self.atualizar()
        else:
            self.atualizar()

    def filtro(self, palavras, index, filtro_recebido):
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

            if len(self.clientes_filtrados) > 0:
                clientes_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for cliente in self.clientes_filtrados:
                            try:
                                if p in cliente[filtro_recebido] and cliente not in clientes_temp:
                                    clientes_temp.append(
                                        cliente)
                            except:
                                if p == cliente[filtro_recebido] and cliente not in clientes_temp:
                                    clientes_temp.append(
                                        cliente)
                else:
                    for cliente in self.clientes_filtrados:
                        try:
                            if filtro in cliente[filtro_recebido] and cliente not in clientes_temp:
                                clientes_temp.append(cliente)
                        except:
                            if filtro == cliente[filtro_recebido] and cliente not in clientes_temp:
                                clientes_temp.append(cliente)

                if len(clientes_temp) > 0:
                    self.clientes_filtrados = clientes_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for cliente in self.clientes:
                            try:
                                if p in cliente[filtro_recebido] and cliente not in self.clientes_filtrados:
                                    self.clientes_filtrados.append(
                                        cliente)
                            except:
                                if p == cliente[filtro_recebido] and cliente not in self.clientes_filtrados:
                                    self.clientes_filtrados.append(
                                        cliente)

                else:
                    for cliente in self.clientes:
                        try:
                            if filtro in cliente[filtro_recebido] and cliente not in self.clientes_filtrados:
                                self.clientes_filtrados.append(cliente)
                        except:
                            if filtro == cliente[filtro_recebido] and cliente not in self.clientes_filtrados:
                                self.clientes_filtrados.append(cliente)
