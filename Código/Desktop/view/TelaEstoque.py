from textual.widgets import Input, TextArea, Footer, Header, Tab, Checkbox, Tabs, Select, Static
from textual.containers import Horizontal, Vertical
from textual.screen import Screen

from model import Init, Corretor, Administrador, Imovel, Gerente

from textual_image.widget import Image


class TelaEstoque(Screen):

    CSS_PATH = "css/TelaEstoque.tcss"
    TITLE = "Estoque"

    imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()
    imoveis_filtrados = []
    filtrou_select = False
    filtrou_input = False
    select_evento = ""

    objeto = Init.um_imovel

    def compose(self):
        yield Header()
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"), Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))

        elif isinstance(Init.usuario_atual, Corretor.Corretor):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))
        else:
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))

        yield Input(placeholder="pesquise aqui")
        yield TextArea(read_only=True, id="tx_dados")
        with Vertical(id="container_filtragem"):
            with Horizontal(id="primeiro"):
                yield Select([("Imoveis", "Imovel"), ("Compradores", "Comprador"), ("Proprietários", "Proprietario"), ("Corretores", "Corretor"), ("Captadores", "Captador"), ("Vendas", "Venda"), ("Alugueis", "Aluguel")], allow_blank=False, id="select_tabelas")
                yield Static("Categoria:")
                yield Select([(valor.value, valor) for valor in Imovel.Categoria])
                yield Static("Status:")
                yield Select([(valor.value, valor) for valor in Imovel.Status])
            with Horizontal(id="segundo"):
                yield Static("Rua")
                yield TextArea()
                yield Static("Bairro")
                yield TextArea()
                yield Static("Cidade")
                yield TextArea()
                yield Static("Complemento")
                yield TextArea()
                yield Static("CEP")
                yield TextArea()
        with Vertical(id="container_resultado"):
            pass

        yield Footer(show_command_palette=False)

    def setup_dados(self):
        if len(self.imoveis_filtrados) > 0:
            quant = len(self.imoveis_filtrados)
        else:
            quant = len(self.imoveis)
        self.query_one("#tx_dados").text = f"Quantidade de imoveis: {quant}"

    def on_select_changed(self, evento: Select.Changed):
        if evento.select.id == "select_tabelas":
            self.tabela = evento.select.value.lower()

            match evento.value:
                case "Imovel":
                    self.imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()
                    self.objeto = Init.um_imovel
                case  "Comprador":
                    self.imoveis = Init.imobiliaria.get_lista_compradores()
                    self.objeto = Init.comprador
                case "Proprietario":
                    self.imoveis = Init.imobiliaria.get_lista_proprietarios()
                    self.objeto = Init.proprietario
                case "Corretor":
                    self.imoveis = Init.imobiliaria.get_lista_corretores()
                    self.objeto = Init.corretor
                case "Captador":
                    self.imoveis = Init.imobiliaria.get_lista_captadores()
                    self.objeto = Init.captador
                case "Venda":
                    self.imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()  # TODO
                    self.objeto = Init.um_imovel
                case "Aluguel":
                    self.imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()  # TODO
                    self.objeto = Init.um_imovel

            self.imoveis_filtrados = []
            self.atualizar()

    def on_mount(self):
        self.atualizar()
        self.setup_dados()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:
            if event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                self.app.switch_screen("tela_cadastro_imovel")
            elif event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                self.app.switch_screen("tela_cadastro_pessoa")
            elif isinstance(Init.usuario_atual, Gerente.Gerente):
                if event.tabs.active == self.query_one("#tab_dados_imobiliaria", Tab).id:
                    self.app.switch_screen("tela_dados_imobiliaria")
            elif isinstance(Init.usuario_atual, Administrador.Administrador):
                if event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                    self.app.switch_screen("tela_servidor")
            elif event.tabs.active == self.query_one("#tab_comprar", Tab).id:
                self.app.switch_screen("tela_estoque_cliente")
            elif event.tabs.active == self.query_one("#tab_dados_cliente", Tab).id:
                self.app.switch_screen("tela_dados_cliente")
        except:
            pass

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_estoque", Tab).id

    def atualizar(self):
        self.query_one("#container_resultado", Vertical).remove_children()

        lista = []

        if self.imoveis_filtrados:
            lista = self.imoveis_filtrados
        else:
            lista = self.imoveis

        for imovel in lista:
            container = Horizontal(classes="imovel")
            self.query_one("#container_resultado").mount(container)

            container.mount(Checkbox())
            if imovel.get_imagens():
                container.mount(Image(imovel.get_imagens()[0]))

            container2 = Vertical(classes="dados0")
            container.mount(container2)
            container3 = Vertical(classes="dados1")
            container2.mount(container3)
            container3.mount(
                Static(imovel.get_endereco().get_bairro(), classes="stt_bairro"))
            container3.mount(Static(f"Referência {imovel.get_id()}", classes="stt_ref"))
            container3.mount(
                Static(f"{imovel.get_status().value} - {imovel.get_nome_condominio()}", classes="stt_status"))
            container3.mount(Static(
                f"{imovel.get_endereco().get_rua()}, {imovel.get_endereco().get_numero()}/{imovel.get_endereco().get_complemento()}"))
            container3.mount(Static(f"{imovel.get_endereco().get_cidade()}"))
            container3.mount(Static(f"{imovel.get_status().value}"))
            if imovel.get_valor_venda():
                container3.mount(
                    Static(f"{imovel.get_valor_venda()}", classes="valor"))
            if imovel.get_valor_aluguel():
                container3.mount(
                    Static(f"{imovel.get_valor_aluguel()}", classes="valor"))
            caomtainer4 = Horizontal(classes="dados2")
            container3.mount(caomtainer4)
            caomtainer4.mount(Static(f"{imovel.get_area_privativa()}"))
            caomtainer4.mount(Static(f"{imovel.get_area_total()}"))
            if imovel.get_quant_banheiros():
                caomtainer4.mount(
                    Static(f"{imovel.get_quant_banheiros()} banheiros"))
            if imovel.get_quant_quartos():
                caomtainer4.mount(
                    Static(f"{imovel.get_quant_quartos()} quartos"))
            if imovel.get_quant_vagas():
                caomtainer4.mount(Static(f"{imovel.get_quant_vagas()} vagas"))

        self.setup_dados()

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value
        palavras = texto.split()

        if len(palavras) > 0:
            self.imoveis_filtrados = []
            for palavra in palavras:
                if palavra[:-1].lower() in self.objeto.__dict__.keys():
                    index = palavras.index(palavra)
                    self.filtro(palavras, index, palavra[:-1].lower())
                    self.atualizar()
        else:
            self.atualizar()

    def filtro(self, palavras, index, filtro_recebido):
        nova_lista = []
        campo = f"get_{filtro_recebido}"

        if index + 1 < len(palavras):
            filtro = " ".join((palavras[index+1:]))

            if "," in filtro:
                filtro = filtro[0:filtro.index(
                    ",")]
            if "-" in filtro.split():
                for palavraa in filtro.split("-"):
                    if filtro.index("-")+1 < len(filtro) and palavraa not in nova_lista:
                        nova_lista.append(palavraa.strip())

            if len(self.imoveis_filtrados) > 0:
                imoveis_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for imovel in self.imoveis_filtrados:
                            try:
                                if p in getattr(imovel, campo)() and imovel not in imoveis_temp:
                                    imoveis_temp.append(
                                        imovel)
                            except:
                                if p == getattr(imovel, campo)() and imovel not in imoveis_temp:
                                    imoveis_temp.append(
                                        imovel)
                else:
                    for imovel in self.imoveis_filtrados:
                        try:
                            if filtro in getattr(imovel, campo)() and imovel not in imoveis_temp:
                                imoveis_temp.append(imovel)
                        except:
                            if filtro == getattr(imovel, campo)() and imovel not in imoveis_temp:
                                imoveis_temp.append(imovel)

                if len(imoveis_temp) > 0:
                    self.imoveis_filtrados = imoveis_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for imovel in self.imoveis:
                            try:
                                if p in getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                    self.imoveis_filtrados.append(
                                        imovel)
                            except:
                                if p == getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                    self.imoveis_filtrados.append(
                                        imovel)

                else:
                    for imovel in self.imoveis:
                        try:
                            if filtro in getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                self.imoveis_filtrados.append(imovel)
                        except:
                            if filtro == getattr(imovel, campo)() and imovel not in self.imoveis_filtrados:
                                self.imoveis_filtrados.append(imovel)
