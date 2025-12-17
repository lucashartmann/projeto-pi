from textual.widgets import Input, TextArea, Footer, Tab, Checkbox, Tabs, Select, Static, Input, Button
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.events import Click
from textual import on
from textual.suggester import SuggestFromList
from utils.Widgets import Header

from model import Init, Imovel, Usuario, Endereco, Captador, Corretor, Condominio
from database.Banco import Banco

from textual_image.widget import Image

from view import TelaCadastroImovel, TelaCadastroPessoa


class TelaEstoque(Screen):

    CSS_PATH = "css/TelaEstoque.tcss"
    TITLE = "Estoque"

    imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()
    usuarios = Init.imobiliaria.get_lista_usuarios()
    proprietarios = Init.imobiliaria.get_lista_proprietarios()
    ruas = (imovel.get_endereco().get_rua() for imovel in imoveis)
    cidades = (imovel.get_endereco().get_cidade() for imovel in imoveis)
    bairros = (imovel.get_endereco().get_bairro() for imovel in imoveis)
    ceps = (str(imovel.get_endereco().get_cep()) for imovel in imoveis)
    lista_filtrada = []
    lista = []
    filtrou_select = False
    filtrou_input = False
    select_evento = ""
    objeto = Init.imovel_um
    tabela = "Imovel"

    def compose(self):
        yield Header()
        if Init.usuario_atual.get_tipo() == Usuario.Tipo.ADMINISTRADOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.CORRETOR:
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        elif Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
            yield Tabs(Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"),
                       Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Estoque", id="tab_estoque"))
        else:
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        yield Input(placeholder="pesquise aqui")
        yield TextArea(read_only=True, id="tx_dados")
        with Vertical(id="container_filtragem"):
            with Horizontal(id="primeiro"):
                if Init.usuario_atual.get_tipo() == Usuario.Tipo.GERENTE:
                    yield Select([("Imoveis", "Imovel"), ("Clientes", "Cliente"), ("Proprietários", "Proprietario"), ("Corretores", "Corretor"), ("Captadores", "Captador")], allow_blank=False, id="select_tabelas", prompt="Selecionar")
                else:
                    yield Select([("Imoveis", "Imovel"), ("Clientes", "Cliente"), ("Proprietários", "Proprietario")], allow_blank=False, id="select_tabelas", prompt="Selecionar")
                yield Static("Categoria:")
                yield Select([(valor.value, valor) for valor in Imovel.Categoria], prompt="Selecionar")
                yield Static("Status:")
                yield Select([(valor.value, valor) for valor in Imovel.Status], prompt="Selecionar")
            with Horizontal(id="segundo"):
                yield Static("CEP")
                yield Input(suggester=SuggestFromList(self.ceps, case_sensitive=False))
                yield Static("Número")
                yield Input()
            with Horizontal(id="h_filtro"):
                yield Select([("Data Cadastro", "Data Cadastro"), ("Valor Venda", "Valor Venda"), ("Valor Aluguel", "Valor Aluguel"), ("Data Atualização", "Data Atualização")], id="select_filtro")
                yield Button("⬇️", id="seta", flat=True)
        with Vertical(id="container_resultado"):
            pass

        yield Footer(show_command_palette=False)

    def on_button_pressed(self):
        if self.query_one(Button).label == "⬇️":
            self.query_one(Button).label = "⬆️"
        else:
            self.query_one(Button).label = "⬇️"
        self.atualizar()

    def on_mount(self):
        # self.query_one("#segundo").self.query_one(Input).BINDINGS.append(Binding(
        #     "tab",
        #     "cursor_right",
        #     "Move cursor right or accept the completion suggestion",
        #     show=False,
        # ),)
        self.lista = self.imoveis
        self.atualizar()

    def setup_dados(self):
        if len(self.lista_filtrada) > 0:
            quant = len(self.lista_filtrada)
        else:
            quant = len(self.lista)
        self.query_one("#tx_dados").text = f"Quantidade de imoveis: {quant}"

    def on_select_changed(self, evento: Select.Changed):
        if evento.select.id == "select_tabelas":
            self.tabela = evento.select.value
            select = self.query_one("#select_filtro", Select)
            select.clear()
            match evento.value:
                case "Imovel":
                    self.objeto = Init.imovel_um
                    self.query_one("#segundo").styles.display = "block"
                    select.set_options([("Data Cadastro", "Data Cadastro"), ("Valor Venda", "Valor Venda"), (
                        "Valor Aluguel", "Valor Aluguel"), ("Data Atualização", "Data Atualização")])
                    self.lista = self.imoveis
                case  "Cliente":
                    self.objeto = Init.comprador
                    self.query_one("#segundo").styles.display = "none"
                    select.set_options(
                        [("Data Cadastro", "Data Cadastro"), ("Data Atualização", "Data Atualização")])
                    self.lista = list(
                        usuario for usuario in self.usuarios if usuario.get_tipo() == Usuario.Tipo.CLIENTE)
                case "Proprietario":
                    self.objeto = Init.proprietario
                    self.query_one("#segundo").styles.display = "none"
                    select.set_options(
                        [("Data Cadastro", "Data Cadastro"), ("Data Atualização", "Data Atualização")])
                    self.lista = self.proprietarios
                case "Corretor":
                    self.objeto = Init.corretor
                    self.query_one("#segundo").styles.display = "none"
                    select.set_options(
                        [("Data Cadastro", "Data Cadastro"), ("Data Atualização", "Data Atualização")])
                    self.lista = list(usuario for usuario in self.usuarios if usuario.get_tipo(
                    ) == Usuario.Tipo.CORRETOR)
                case "Captador":
                    self.objeto = Init.captador
                    self.query_one("#segundo").styles.display = "none"
                    select.set_options(
                        [("Data Cadastro", "Data Cadastro"), ("Data Atualização", "Data Atualização")])
                    self.lista = list(usuario for usuario in self.usuarios if usuario.get_tipo(
                    ) == Usuario.Tipo.CAPTADOR)
                case "Venda":
                    self.objeto = None
                    self.query_one("#segundo").styles.display = "none"
                case "Aluguel":
                    self.objeto = None
                case "Gerente":
                    self.objeto = Init.gerente
                    self.query_one("#segundo").styles.display = "none"
                    select.set_options(
                        [("Data Cadastro", "Data Cadastro"), ("Data Atualização", "Data Atualização")])
                    self.lista = list(
                        usuario for usuario in self.usuarios if usuario.get_tipo() == Usuario.Tipo.GERENTE)
                case "Admnistrador":
                    self.objeto = Init.administrador
                    self.query_one("#segundo").styles.display = "none"
                    select.set_options(
                        [("Data Cadastro", "Data Cadastro"), ("Data Atualização", "Data Atualização")])
                    self.lista = list(usuario for usuario in self.usuarios if usuario.get_tipo(
                    ) == Usuario.Tipo.ADMINISTRADOR)

            self.lista_filtrada = []
            self.atualizar()
        elif evento.select.id == "select_filtro":
            self.atualizar()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        try:
            if event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                self.app.switch_screen("tela_cadastro_pessoa")

            elif event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                self.app.switch_screen("tela_cadastro_imovel")

            elif event.tabs.active == self.query_one("#tab_cadastro_imovel", Tab).id:
                self.app.switch_screen("tela_cadastro_imovel")

            elif event.tabs.active == self.query_one("#tab_estoque", Tab).id:
                self.app.switch_screen("tela_estoque")

            elif event.tabs.active == self.query_one("#tab_dados_imobiliaria", Tab).id:
                self.app.switch_screen("tela_dados_imobiliaria")

            elif event.tabs.active == self.query_one("#tab_servidor", Tab).id:
                self.app.switch_screen("tela_servidor")

            elif event.tabs.active == self.query_one("#tab_comprar", Tab).id:
                self.app.switch_screen("tela_estoque_cliente")

            elif event.tabs.active == self.query_one("#tab_dados_cliente", Tab).id:
                self.app.switch_screen("tela_dados_cliente")

            elif event.tabs.active == self.query_one("#tab_atendimento", Tab).id:
                self.app.switch_screen("tela_atendimento")

            elif event.tabs.active == self.query_one("#tab_cadastro_venda_aluguel", Tab).id:
                self.app.switch_screen("tela_cadastro_venda_aluguel")

        except Exception as e:
            pass

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one("#tab_estoque", Tab).id

        # imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis()
        # usuarios = Init.imobiliaria.get_lista_usuarios()
        # proprietarios = Init.imobiliaria.get_lista_proprietarios()
        ruas = (imovel.get_endereco().get_rua() for imovel in self.imoveis)
        cidades = (imovel.get_endereco().get_cidade()
                   for imovel in self.imoveis)
        bairros = (imovel.get_endereco().get_bairro()
                   for imovel in self.imoveis)
        ceps = (str(imovel.get_endereco().get_cep())
                for imovel in self.imoveis)

        # condicao = False

        # if imoveis != self.imoveis:
        #     self.imoveis = imoveis
        #     if self.tabela == "Imovel":
        #         condicao = True

        # if usuarios != self.usuarios:
        #     self.usuarios = usuarios
        #     if self.tabela == "Usuario":
        #         condicao = True

        if ceps != self.ceps:
            self.ceps = ceps

        if ruas != self.ruas:
            self.ruas = ruas

        if bairros != self.bairros:
            self.bairros = bairros

        if cidades != self.cidades:
            self.cidades = cidades

        # if proprietarios != self.proprietarios:
        #     self.proprietarios = proprietarios
        #     if self.tabela == "Proprietario":
        #         condicao = True

        # if condicao:
        #     self.atualizar()

    @on(Click)
    def on_click(self, evento: Click):
        widget = ""
        try:
            if "dados0" in evento.widget.parent.parent.classes:
                widget = evento.widget.parent.parent.parent
            elif "dados1" in evento.widget.parent.parent.classes:
                widget = evento.widget.parent.parent.parent.parent
            else:
                widget = evento.widget.parent.parent

            if widget and widget.classes:
                if "imovel" in widget.classes:
                    banco = Banco()
                    if widget.name and self.tabela == "Imovel":
                        imovel = banco.get_imovel_por_id(int(widget.name))
                        if imovel:
                            self.app.switch_screen(
                                TelaCadastroImovel.TelaCadastroImovel(imovel=imovel))
                        else:
                            self.screen.notify("ERRO. Imóvel não encontrado.")
                    elif widget.name:
                        pessoa = None
                        if self.tabela == "Proprietario":
                            pessoa = banco.get_proprietario_por_cpf_cnpj(
                                widget.name)
                        else:
                            pessoa = banco.get_usuario_por_cpf_cnpj(
                                widget.name)

                        if pessoa:
                            self.app.switch_screen(
                                TelaCadastroPessoa.TelaCadastroPessoa(pessoa=pessoa))
                        else:
                            self.screen.notify("ERRO. Pessoa não encontrada.")

        except Exception:
            pass

    def atualizar(self):
        self.query_one("#container_resultado").remove_children()

        lista = []

        if self.lista_filtrada:
            lista = self.lista_filtrada
        else:
            lista = self.lista

        lista_filtrada = []

        match self.query_one("#select_filtro", Select).value:
            case "Data Cadastro":
                for objeto in lista:
                    if objeto.get_data_cadastro():
                        lista_filtrada.append(objeto)
                if lista_filtrada:
                    for objeto in lista:
                        for objeto2 in lista_filtrada:
                            if objeto.get_data_cadastro() and objeto.get_data_cadastro() >= objeto2.get_data_cadastro():
                                lista_filtrada.append(objeto)
                                break
            case "Valor Venda":
                for imovel in lista:
                    if imovel.get_data_cadastro():
                        lista_filtrada.append(imovel)
                if lista_filtrada:
                    for imovel in lista:
                        for imovel2 in lista_filtrada:
                            if imovel.get_valor_venda() and imovel.get_valor_venda() >= imovel2.get_valor_venda():
                                lista_filtrada.append(imovel)
                                break
            case "Valor Aluguel":
                for imovel in lista:
                    if imovel.get_valor_aluguel():
                        lista_filtrada.append(imovel)
                if lista_filtrada:
                    for imovel in lista:
                        for imovel2 in lista_filtrada:
                            if imovel.get_valor_aluguel() and imovel.get_valor_aluguel() >= imovel2.get_valor_aluguel():
                                lista_filtrada.append(imovel)
                                break
            case "Data Atualização":
                for objeto in lista:
                    if objeto.get_data_modificacao():
                        lista_filtrada.append(objeto)
                if lista_filtrada:
                    for objeto in lista:
                        for objeto2 in lista_filtrada:
                            if objeto.get_data_modificacao() and objeto.get_data_modificacao() >= objeto2.get_data_modificacao():
                                lista_filtrada.append(objeto)
                                break
        if lista_filtrada:
            lista = lista_filtrada

        if self.tabela == "Imovel":
            for imovel in lista:
                container = Horizontal(classes="imovel", name=imovel.get_id())
                self.query_one("#container_resultado").mount(container)

                container.mount(Checkbox())
                if imovel.get_anuncio() and imovel.get_anuncio().get_imagens():
                    container.mount(
                        Image(imovel.get_anuncio().get_imagens()[0]))

                container2 = Vertical(classes="dados0")
                container.mount(container2)
                container3 = Vertical(classes="dados1")
                container2.mount(container3)
                container3.mount(
                    Static(imovel.get_endereco().get_bairro(), classes="stt_bairro"))
                container3.mount(
                    Static(f"Referência {imovel.get_id()}", classes="stt_ref"))
                if imovel.get_condominio():
                    container3.mount(
                        Static(f"{imovel.get_status().value} - {imovel.get_condominio().get_nome()}", classes="stt_status"))

                container3.mount(Static(
                    f"{imovel.get_endereco().get_rua()}, {imovel.get_endereco().get_numero()}/{imovel.get_complemento()}"))
                container3.mount(
                    Static(f"{imovel.get_endereco().get_cidade()}"))
                if imovel.get_status():
                    container3.mount(Static(f"{imovel.get_status().value}"))
                if imovel.get_valor_venda():
                    container3.mount(
                        Static(f"{imovel.get_valor_venda()}", classes="valor"))
                if imovel.get_valor_aluguel():
                    container3.mount(
                        Static(f"{imovel.get_valor_aluguel()}", classes="valor"))
                container4 = Horizontal(classes="dados2")
                container3.mount(container4)
                container4.mount(Static(f"{imovel.get_area_privativa()}"))
                container4.mount(Static(f"{imovel.get_area_total()}"))
                if imovel.get_quant_banheiros():
                    container4.mount(
                        Static(f"{imovel.get_quant_banheiros()} banheiros"))
                if imovel.get_quant_quartos():
                    container4.mount(
                        Static(f"{imovel.get_quant_quartos()} quartos"))
                if imovel.get_quant_vagas():
                    container4.mount(
                        Static(f"{imovel.get_quant_vagas()} vagas"))
        else:
            for pessoa in lista:
                container = Horizontal(
                    classes="imovel", name=pessoa.get_cpf_cnpj())
                self.query_one("#container_resultado").mount(container)

                container.mount(Checkbox())
                container2 = Vertical(classes="dados0")
                container.mount(container2)
                container3 = Vertical(classes="dados1")
                container2.mount(container3)

                container3.mount(
                    Static(f"Nome {pessoa.get_nome()}", classes="stt_ref"))
                container3.mount(
                    Static(f"CPF-CNPJ {pessoa.get_cpf_cnpj()}", classes="stt_ref"))
                if pessoa.get_email():
                    container3.mount(
                        Static(f"Email {pessoa.get_email()}", classes="stt_bairro"))
                if pessoa.get_telefones():
                    for telefone in pessoa.get_telefones():
                        container3.mount(
                            Static(f"Telefone: {telefone}", classes="stt_bairro"))

        self.setup_dados()

    def on_input_changed(self, evento: Input.Changed):
        texto = evento.value
        palavras = texto.split()
        if len(palavras) > 0 and self.objeto:
            self.lista_filtrada = []
            for palavra in palavras:
                if palavra[:-1].lower() in self.objeto.__dict__.keys():
                    index = palavras.index(palavra)
                    self.filtro(palavras, index, palavra[:-1].lower())
                    self.atualizar()
                elif "endereco" in self.objeto.__dict__.keys():
                    endereco = Endereco.Endereco()
                    if palavra[:-1].lower() in endereco.__dict__.keys():
                        index = palavras.index(palavra)
                        self.filtro(palavras, index,
                                    f"endereco().{palavra[:-1].lower()}")
                        self.atualizar()
                elif "condominio" in self.objeto.__dict__.keys():
                    condominio = Condominio.Condominio()
                    if palavra[:-1].lower() in condominio.__dict__.keys():
                        index = palavras.index(palavra)
                        self.filtro(palavras, index,
                                    f"condominio().{palavra[:-1].lower()}")
                        self.atualizar()
                    elif "endereco" in self.objeto.__dict__.keys():
                        endereco = Endereco.Endereco()
                        if palavra[:-1].lower() in endereco.__dict__.keys():
                            index = palavras.index(palavra)
                            self.filtro(
                                palavras, index, f"condominio().endereco().{palavra[:-1].lower()}")
                            self.atualizar()
                elif "captador" in self.objeto.__dict__.keys():
                    captador = Captador.Captador()
                    if palavra[:-1].lower() in captador.__dict__.keys():
                        index = palavras.index(palavra)
                        self.filtro(palavras, index,
                                    f"captador().{palavra[:-1].lower()}")
                        self.atualizar()
                    elif "endereco" in self.objeto.__dict__.keys():
                        endereco = Endereco.Endereco()
                        if palavra[:-1].lower() in endereco.__dict__.keys():
                            index = palavras.index(palavra)
                            self.filtro(
                                palavras, index, f"captador().endereco().{palavra[:-1].lower()}")
                            self.atualizar()
                elif "corretor" in self.objeto.__dict__.keys():
                    corretor = Corretor.Corretor()
                    if palavra[:-1].lower() in corretor.__dict__.keys():
                        index = palavras.index(palavra)
                        self.filtro(palavras, index,
                                    f"corretor().{palavra[:-1].lower()}")
                        self.atualizar()
                    elif "endereco" in self.objeto.__dict__.keys():
                        endereco = Endereco.Endereco()
                        if palavra[:-1].lower() in endereco.__dict__.keys():
                            index = palavras.index(palavra)
                            self.filtro(
                                palavras, index, f"corretor().endereco().{palavra[:-1].lower()}")
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

            if len(self.lista_filtrada) > 0:
                objetos_temp = []
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for objeto in self.lista_filtrada:
                            try:
                                if p in getattr(objeto, campo)() and objeto not in objetos_temp:
                                    objetos_temp.append(
                                        objeto)
                            except:
                                if p == getattr(objeto, campo)() and objeto not in objetos_temp:
                                    objetos_temp.append(
                                        objeto)
                else:
                    for objeto in self.lista_filtrada:
                        try:
                            if filtro in getattr(objeto, campo)() and objeto not in objetos_temp:
                                objetos_temp.append(objeto)
                        except:
                            if filtro == getattr(objeto, campo)() and objeto not in objetos_temp:
                                objetos_temp.append(objeto)

                if len(objetos_temp) > 0:
                    self.lista_filtrada = objetos_temp
            else:
                if len(nova_lista) > 0:
                    for p in nova_lista:
                        for objeto in self.imoveis:
                            try:
                                if p in getattr(objeto, campo)() and objeto not in self.lista_filtrada:
                                    self.lista_filtrada.append(
                                        objeto)
                            except:
                                if p == getattr(objeto, campo)() and objeto not in self.lista_filtrada:
                                    self.lista_filtrada.append(
                                        objeto)

                else:
                    for objeto in self.imoveis:
                        try:
                            if filtro in getattr(objeto, campo)() and objeto not in self.lista_filtrada:
                                self.lista_filtrada.append(objeto)
                        except:
                            if filtro == getattr(objeto, campo)() and objeto not in self.lista_filtrada:
                                self.lista_filtrada.append(objeto)
