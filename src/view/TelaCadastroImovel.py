from textual.screen import Screen, ModalScreen
from textual.widgets import MaskedInput, Static, TextArea, Tab, Tabs, Select, Checkbox, Button, Header, Footer, Input
from textual.containers import Horizontal, Vertical, Grid, VerticalScroll, Center
from textual.validation import Length
import requests
import datetime

from model import Init, Imovel, Usuario, Endereco, Anuncio, Condominio
from controller import Controller

from textual_image.widget import Image


class PopUp(ModalScreen):
    def compose(self):
        yield Static("Imovel nao salvo, deseja continuar?")
        with Horizontal():
            yield Button("Confirmar", id="bt_confirmar")
            yield Button("Cancelar")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_confirmar":
            self.screen.confirmar_salvamento = True
        else:
            self.screen.confirmar_salvamento = False

        self.remove()


class PopUpApagar(ModalScreen):
    def compose(self):
        yield Static("Certeza que deseja apagar?")
        with Horizontal():
            yield Button("Confirmar", id="bt_confirmar")
            yield Button("Cancelar")

    def on_button_pressed(self, evento: Button.Pressed):
        if evento.button.id == "bt_confirmar":
            ref = int(self.query_one("#ta_ref", TextArea).text)
            remocao = Controller.remover(ref, "imovel")
            self.screen.notify(remocao)
            self.screen.acao == True

        self.remove()


class ContainerFuncionario(Horizontal):
    def compose(self):
        yield Static("Nome do cliente", id="st_nome")
        yield Static("Telefone do cliente", id="st_telefone")
        yield Static("Email do cliente", id="st_email")


class TelaCadastroImovel(Screen):

    CSS_PATH = "css/TelaCadastroImovel.tcss"

    salvo = False
    acao = False

    def __init__(self, name=None, id=None, classes=None, imovel=None):
        super().__init__(name, id, classes)
        self.imovel = imovel

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

        with Horizontal(id="h_buttons"):
            yield Button("Apagar", id="bt_apagar_cadastro")
            yield Button("Salvar", id="bt_salvar_alteracoes")

        with VerticalScroll():
            yield Tabs(Tab("Cadastro", id="tab_imovel"), Tab("Anuncio", id="tab_anuncio"), id="tabs_anuncio")

            with Grid(id="container_cadastro"):
                yield Static("ref:", id="stt_ref")
                yield TextArea(disabled=True, id="ta_ref")
                yield Static("Categoria:", id="stt_categoria")
                yield Select([(valor.value, valor) for valor in Imovel.Categoria], id="select_categoria", prompt="Selecionar")
                yield Static("Situação:", id="stt_situacao")
                yield Select([(valor.value, valor) for valor in Imovel.Situacao], id="select_situacao", prompt="Selecionar")
                yield Static("Estado:", id="stt_estado_select")
                yield Select([(valor.value, valor) for valor in Imovel.Estado], id="select_estado", prompt="Selecionar")
                yield Static("Ocupação:", id="stt_ocupacao")
                yield Select([(valor.value, valor) for valor in Imovel.Ocupacao], id="select_ocupacao", prompt="Selecionar")
                yield Static("Status:", id="stt_status")
                yield Select([(valor.value, valor) for valor in Imovel.Status], id="select_status", prompt="Selecionar")
                yield Static("Nome do Condomínio", id="stt_nome_condominio")
                yield TextArea(id="ta_nome_condominio")
                yield Static("Ano de Construção", id="stt_ano_construcao")
                yield MaskedInput(template="0000", id="ta_ano_construcao", validators=Length(minimum=10, maximum=10), valid_empty=True)
                yield Static("[red]*[/]CEP", id="stt_cep")
                yield MaskedInput(template="00000-000", id="ta_cep", validators=Length(minimum=9, maximum=9), valid_empty=False)
                yield Static("[red]*[/]Rua", id="stt_rua")
                yield TextArea(disabled=True, id="ta_rua")
                yield Static("Número", id="stt_numero")
                yield Input(id="ta_numero", type="integer", valid_empty=True)
                yield Static("Complemento", id="stt_complemento")
                yield TextArea(id="ta_complemento")
                yield Static("Bloco", id="stt_bloco")
                yield TextArea(id="ta_bloco")
                yield Static("Andar", id="stt_andar")
                yield MaskedInput(template="00", id="ta_andar",  validators=Length(minimum=1, maximum=2), valid_empty=True)
                yield Static("[red]*[/]Bairro", id="stt_bairro")
                yield TextArea(disabled=True, id="ta_bairro")
                yield Static("[red]*[/]Cidade", id="stt_cidade")
                yield TextArea(disabled=True, id="ta_cidade")
                yield Static("[red]*[/]Estado", id="stt_estado")
                yield MaskedInput(disabled=True, template="XX", id="ta_estado", validators=Length(minimum=2, maximum=2))
                yield Static("Salas", id="stt_salas")
                yield MaskedInput(template="00", id="ta_salas", validators=Length(minimum=1, maximum=2), valid_empty=True)
                yield Static("Banheiros", id="stt_banheiros")
                yield MaskedInput(template="00", id="ta_banheiros", validators=Length(minimum=1, maximum=2), valid_empty=True)
                yield Static("Vagas", id="stt_vagas")
                yield MaskedInput(template="00", id="ta_vagas", validators=Length(minimum=1, maximum=2), valid_empty=True)
                yield Static("Varandas", id="stt_varandas")
                yield MaskedInput(template="00", id="ta_varandas", validators=Length(minimum=1, maximum=2), valid_empty=True)
                yield Static("Quartos", id="stt_quartos")
                yield MaskedInput(template="00", id="ta_quartos", validators=Length(minimum=1, maximum=2), valid_empty=True)
                yield Static("Área Total", id="stt_area_total")
                yield Input(id="ta_area_total", type="number")
                yield Static("Área Privativa", id="stt_area_privativa")
                yield Input(id="ta_area_privativa", type="number")
                yield Static("Valor Venda:", id="stt_venda")
                yield Input(id="ta_venda", type="number")
                yield Static("Valor Aluguel:", id="stt_aluguel")
                yield Input(id="ta_aluguel", type="number")
                yield Static("Valor Condomínio:", id="stt_condominio")
                yield Input(id="ta_condominio", type="number")
                yield Static("Valor IPTU:", id="stt_iptu")
                yield Input(id="ta_iptu", type="number")

            with Vertical(id="container_anuncio"):
                yield Static("Titulo")
                with Center():
                    yield TextArea(id="ta_titulo_anuncio")
                yield Static("Descriçao")
                with Center():
                    yield TextArea(id="ta_descricao_anuncio")
                yield Static("Apartamento")

                with Grid(id="container_info_imovel"):
                    lista = Init.imobiliaria.get_lista_filtros_apartamento()
                    if lista:
                        for nome in lista:
                            yield Checkbox(label=nome)
                yield Static("Condomínio")
                with Grid(id="container_info_condominio"):
                    lista = Init.imobiliaria.get_lista_filtros_condominio()
                    if lista:
                        for nome in lista:
                            yield Checkbox(label=nome)

            with Grid(id="container_imagens"):
                yield Button("Editar", id="bt_editar_imagens")

                # TODO: Fazer botao para adicionar remover imagem e adicionar videos. Possibilitar adicionar mais imagens

            with Grid(id="container_anexos"):
                yield Button("Adicionar", id="bt_adicionar_anexos")

                # TODO: Pegar o widget de documento, possibilitar adicionar, remover

            with Vertical(id="container_proprietario"):
                yield Static("Proprietario: ", classes="stt_container_titulo")

            with Vertical(id="container_corretor"):
                yield Static("Corretor: ", classes="stt_container_titulo")

            with Vertical(id="container_captador"):
                yield Static("Captador: ", classes="stt_container_titulo")

        yield Footer(show_command_palette=False)

    def on_mount(self):
        container_captador = self.query_one("#container_captador", Vertical)
        container_corretor = self.query_one("#container_corretor", Vertical)

        if self.imovel is None and (Init.usuario_atual.get_tipo() == Usuario.Tipo.CAPTADOR or Init.usuario_atual.get_tipo() == Usuario.Tipo.CORRETOR):

            if Init.usuario_atual.get_tipo() == Usuario.Tipo.CAPTADOR:
                container = ContainerFuncionario()
                container_captador.mount(
                    container, after=container_captador.query_one(Static))

            elif Init.usuario_atual.get_tipo() == Usuario.Tipo.CORRETOR:
                container = ContainerFuncionario()
                container_corretor.mount(
                    container, after=container_corretor.query_one(Static))

            container.query_one("#st_nome", Static).update(
                Init.usuario_atual.get_nome())
            container.query_one("#st_telefone", Static).update(
                "".join(str(telefone for telefone in Init.usuario_atual.get_telefones())))
            container.query_one("#st_email", Static).update(
                Init.usuario_atual.get_email())

        if self.imovel:
            lista = self.imovel.get_filtros()
            if lista:
                for nome in lista:
                    for checkbox in self.query(Checkbox):
                        if checkbox.label == nome:
                            checkbox.value = True

            if self.imovel.get_condominio() and self.imovel.get_condominio().get_filtros():
                lista = self.imovel.get_condominio().get_filtros()
                if lista:
                    for nome in lista:
                        for checkbox in self.query(Checkbox):
                            if checkbox.label == nome:
                                checkbox.value = True

            self.query_one("#ta_ref", TextArea).text = str(
                self.imovel.get_id())

            container_proprietario = self.query_one(
                "#container_proprietario", Vertical)

            if self.imovel.get_proprietario():
                container = ContainerFuncionario()
                container_proprietario.mount(
                    container, after=container_proprietario.query_one(Static))
                container.query_one("#st_nome", Static).update(
                    self.imovel.get_proprietario().get_nome())
                container.query_one("#st_telefone", Static).update(
                    self.imovel.get_proprietario().get_telefone())
                container.query_one("#st_email", Static).update(
                    self.imovel.get_proprietario().get_email())

            if self.imovel.get_corretor():
                container = ContainerFuncionario()
                container_corretor.mount(
                    container, after=container_corretor.query_one(Static))
                container.query_one("#st_nome", Static).update(
                    self.imovel.get_corretor().get_nome())
                container.query_one("#st_telefone", Static).update(
                    self.imovel.get_corretor().get_telefone())
                container.query_one("#st_email", Static).update(
                    self.imovel.get_corretor().get_email())

            if self.imovel.get_captador():
                container = ContainerFuncionario()
                container_captador.mount(
                    container, after=container_captador.query_one(Static))
                container.query_one("#st_nome", Static).update(
                    self.imovel.get_captador().get_nome())
                container.query_one("#st_telefone", Static).update(
                    self.imovel.get_captador().get_telefone())
                container.query_one("#st_email", Static).update(
                    self.imovel.get_captador().get_email())

            if self.imovel.get_categoria() is not None:
                self.query_one(
                    "#select_categoria", Select).value = self.imovel.get_categoria()
            if self.imovel.get_situacao() is not None:
                self.query_one(
                    "#select_situacao", Select).value = self.imovel.get_situacao()
            if self.imovel.get_estado() is not None:
                self.query_one("#select_estado",
                               Select).value = self.imovel.get_estado()
            if self.imovel.get_ocupacao() is not None:
                self.query_one(
                    "#select_ocupacao", Select).value = self.imovel.get_ocupacao()
            if self.imovel.get_ocupacao() is not None:
                self.query_one("#select_status",
                               Select).value = self.imovel.get_ocupacao()
            if self.imovel.get_condominio() is not None and self.imovel.get_condominio().get_nome():
                self.query_one(
                    "#ta_nome_condominio", TextArea).text = self.imovel.get_condominio().get_nome()
            self.query_one(
                "#ta_rua", TextArea).text = self.imovel.get_endereco().get_rua()
            if self.imovel.get_endereco().get_numero() is not None:
                self.query_one(
                    "#ta_numero", Input).value = str(self.imovel.get_endereco().get_numero())
            if self.imovel.get_complemento() is not None:
                self.query_one(
                    "#ta_complemento", TextArea).text = self.imovel.get_complemento()
            if self.imovel.get_bloco() is not None:
                self.query_one(
                    "#ta_bloco", TextArea).text = self.imovel.get_bloco()
            cep = str(self.imovel.get_endereco().get_cep())
            cep = cep[:5] + "-" + cep[5:]
            self.query_one(
                "#ta_cep", MaskedInput).value = cep
            self.query_one(
                "#ta_bairro", TextArea).text = self.imovel.get_endereco().get_bairro()
            self.query_one(
                "#ta_cidade", TextArea).text = self.imovel.get_endereco().get_cidade()
            self.query_one(
                "#ta_estado", MaskedInput).value = self.imovel.get_endereco().get_uf()
            if self.imovel.get_quant_salas() is not None:
                self.query_one(
                    "#ta_salas", MaskedInput).value = str(self.imovel.get_quant_salas())
            if self.imovel.get_quant_banheiros() is not None:
                self.query_one(
                    "#ta_banheiros", MaskedInput).value = str(self.imovel.get_quant_banheiros())
            if self.imovel.get_quant_vagas() is not None:
                self.query_one(
                    "#ta_vagas", MaskedInput).value = str(self.imovel.get_quant_vagas())
            if self.imovel.get_quant_varandas() is not None:
                self.query_one(
                    "#ta_varandas", MaskedInput).value = str(self.imovel.get_quant_varandas())
            if self.imovel.get_quant_quartos() is not None:
                self.query_one(
                    "#ta_quartos", MaskedInput).value = str(self.imovel.get_quant_quartos())
            if self.imovel.get_area_total() is not None:
                self.query_one(
                    "#ta_area_total", Input).value = str(self.imovel.get_area_total())
            if self.imovel.get_area_privativa() is not None:
                self.query_one(
                    "#ta_area_privativa", Input).value = str(self.imovel.get_area_privativa())
            if self.imovel.get_valor_venda() is not None:
                self.query_one(
                    "#ta_venda", Input).value = str(self.imovel.get_valor_venda())
            if self.imovel.get_valor_aluguel() is not None:
                self.query_one(
                    "#ta_aluguel", Input).value = str(self.imovel.get_valor_aluguel())
            if self.imovel.get_valor_condominio() is not None:
                self.query_one(
                    "#ta_condominio", Input).value = str(self.imovel.get_valor_condominio())
            if self.imovel.get_iptu() is not None:
                self.query_one(
                    "#ta_iptu", Input).value = str(self.imovel.get_iptu())
            if self.imovel.get_andar() is not None:
                self.query_one(
                    "#ta_andar", MaskedInput).value = str(self.imovel.get_andar())
            if self.imovel.get_ano_construcao() is not None:
                self.query_one(
                    "#ta_ano_construcao", MaskedInput).value = str(self.imovel.get_ano_construcao())
            if self.imovel.get_anuncio() is not None and self.imovel.get_anuncio().get_titulo():
                self.query_one(
                    "#ta_titulo_anuncio", TextArea).text = self.imovel.get_anuncio().get_titulo()
            if self.imovel.get_anuncio() is not None and self.imovel.get_anuncio().get_descricao():
                self.query_one(
                    "#ta_descricao_anuncio", TextArea).text = self.imovel.get_anuncio().get_descricao()

            if self.imovel.get_anuncio() and self.imovel.get_anuncio().get_imagens():
                container_imagens = self.query_one("#container_imagens", Grid)
                for imagem in self.imovel.get_anuncio().get_imagens():
                    container_imagens.mount(
                        Image(imagem, id="st_imagem_anuncio"), after=container_imagens.query_one(Button))

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_cadastro_imovel", Tab).id

    def on_input_changed(self, evento: MaskedInput.Changed):
        self.salvo = False
        if evento.input.id == "ta_cep":
            cep = str(evento.input.value.strip())
            self.query_one("#ta_bairro", TextArea).clear()
            self.query_one("#ta_estado", MaskedInput).clear()
            self.query_one("#ta_rua", TextArea).clear()
            self.query_one("#ta_cidade", TextArea).clear()
            if len(cep) > 8:
                try:
                    link = f"https://viacep.com.br/ws/{cep}/json/"
                    requisicao = requests.get(link)
                    dados = requisicao.json()
                    logradouro = dados["logradouro"]
                    bairro = dados["bairro"]
                    cidade = dados["localidade"]
                    uf = dados["uf"]
                    self.query_one("#ta_bairro", TextArea).text = bairro
                    self.query_one("#ta_estado", MaskedInput).value = uf
                    self.query_one("#ta_rua", TextArea).text = logradouro
                    self.query_one("#ta_cidade", TextArea).text = cidade
                except Exception as e:
                    self.notify("ERRO! CEP inválido")

    def on_button_pressed(self, evento: Button.Pressed):

        match evento.button.id:
            case "bt_salvar_alteracoes":

                ref = self.query_one("#ta_ref", TextArea).text.strip()
                if ref:
                    int(self.query_one("#ta_ref", TextArea).text.strip())
                else:
                    ref = None

                categoria_imovel = self.query_one(
                    "#select_categoria", Select).value
                situacao_imovel = self.query_one(
                    "#select_situacao", Select).value
                estado_imovel = self.query_one("#select_estado", Select).value
                ocupacao_imovel = self.query_one(
                    "#select_ocupacao", Select).value
                status_imovel = self.query_one("#select_status", Select).value

                if status_imovel == "NoSelection" or status_imovel == Select.BLANK:
                    status_imovel = None

                if categoria_imovel == "NoSelection" or categoria_imovel == Select.BLANK:
                    categoria_imovel = None

                if situacao_imovel == "NoSelection" or situacao_imovel == Select.BLANK:
                    situacao_imovel = None

                if estado_imovel == "NoSelection" or estado_imovel == Select.BLANK:
                    estado_imovel = None

                if ocupacao_imovel == "NoSelection" or ocupacao_imovel == Select.BLANK:
                    ocupacao_imovel = None

                nome_condominio = self.query_one(
                    "#ta_nome_condominio", TextArea).text
                rua = self.query_one("#ta_rua", TextArea).text
                numero = int(self.query_one(
                    "#ta_numero", Input).value)
                complemento = self.query_one(
                    "#ta_complemento", TextArea).text.strip()
                bloco = self.query_one("#ta_bloco", TextArea).text.strip()

                cep = self.query_one(
                    "#ta_cep", MaskedInput)
                if not cep._valid:
                    self.notify("ERRO! CEP inválido")
                    return
                else:
                    cep = self.query_one(
                        "#ta_cep", MaskedInput).value.strip()
                    cep = int("".join(cep.split("-")))
                bairro = self.query_one("#ta_bairro", TextArea).text
                cidade = self.query_one("#ta_cidade", TextArea).text
                estado = self.query_one(
                    "#ta_estado", MaskedInput)
                if estado._valid:
                    estado = self.query_one(
                        "#ta_estado", MaskedInput).value.strip()
                else:
                    estado = None
                salas = self.query_one(
                    "#ta_salas", MaskedInput)
                if salas._valid:
                    salas = int(self.query_one(
                        "#ta_salas", MaskedInput).value)
                else:
                    salas = None
                banheiros = self.query_one(
                    "#ta_banheiros", MaskedInput)
                if banheiros._valid:
                    banheiros = int(self.query_one(
                        "#ta_banheiros", MaskedInput).value)
                else:
                    banheiros = None
                vagas = self.query_one(
                    "#ta_vagas", MaskedInput)
                if vagas._valid:
                    vagas = int(self.query_one(
                        "#ta_vagas", MaskedInput).value)
                else:
                    vagas = None
                varandas = self.query_one(
                    "#ta_varandas", MaskedInput)
                if varandas._valid:
                    varandas = int(self.query_one(
                        "#ta_varandas", MaskedInput).value)
                else:
                    varandas = None
                quartos = self.query_one(
                    "#ta_quartos", MaskedInput)
                if quartos._valid:
                    quartos = int(self.query_one(
                        "#ta_quartos", MaskedInput).value)
                else:
                    quartos = None
                area_total = float(self.query_one(
                    "#ta_area_total", Input).value)
                area_privativa = float(self.query_one(
                    "#ta_area_privativa", Input).value)
                venda = float(self.query_one(
                    "#ta_venda", Input).value)
                aluguel = float(self.query_one(
                    "#ta_aluguel", Input).value)
                valor_condominio = float(self.query_one(
                    "#ta_condominio", Input).value)
                iptu = float(self.query_one(
                    "#ta_iptu", Input).value)
                andar = self.query_one("#ta_andar", MaskedInput)
                if andar._valid:
                    andar = self.query_one("#ta_andar", MaskedInput).value
                else:
                    andar = None
                ano_construcao = self.query_one(
                    "#ta_ano_construcao", MaskedInput)
                if ano_construcao._valid:
                    ano_construcao = int(self.query_one(
                        "#ta_ano_construcao", MaskedInput).value)
                else:
                    ano_construcao = None
                endereco = Endereco.Endereco(rua, bairro,
                                             cep, cidade, estado)
                endereco.set_numero(numero)
                # anuncio.set_anexos()
                # anuncio.set_videos()
                # anuncio.set_fotos()
                titulo = self.query_one("#ta_titulo_anuncio", TextArea).text
                descricao = self.query_one(
                    "#ta_descricao_anuncio", TextArea).text
                if self.imovel:
                    anuncio = self.imovel.get_anuncio()
                else:
                    anuncio = Anuncio.Anuncio()

                anuncio.set_titulo(titulo)
                anuncio.set_descricao(descricao)

                if self.imovel:
                    imovel = self.imovel
                    imovel.set_endereco(endereco)
                    imovel.set_status(status_imovel)
                    imovel.set_categoria(categoria_imovel)
                else:
                    imovel = Imovel.Imovel(
                        endereco, status_imovel, categoria_imovel)

                imovel.set_complemento(complemento)
                if not self.imovel:
                    imovel.set_anuncio(anuncio)
                imovel.set_andar(andar)
                imovel.set_ano_construcao(ano_construcao)
                imovel.set_area_privativa(area_privativa)
                if Init.usuario_atual.get_tipo() == Usuario.Tipo.CAPTADOR:
                    imovel.set_captador(Init.usuario_atual)
                elif Init.usuario_atual.get_tipo() == Usuario.Tipo.CORRETOR:
                    imovel.set_corretor(Init.usuario_atual)
                imovel.set_area_total(area_total)
                imovel.set_bloco(bloco)
                imovel.set_iptu(iptu)
                imovel.set_valor_condominio(valor_condominio)
                imovel.set_valor_venda(venda)
                imovel.set_valor_aluguel(aluguel)
                imovel.set_quant_banheiros(banheiros)
                imovel.set_quant_quartos(quartos)
                imovel.set_quant_salas(salas)
                imovel.set_quant_vagas(vagas)
                imovel.set_quant_varandas(varandas)
                imovel.set_situacao(situacao_imovel)
                imovel.set_estado(estado_imovel)
                imovel.set_ocupacao(ocupacao_imovel)
                if not self.imovel:
                    imovel.set_id(ref)
                imovel.set_data_modificacao(datetime.datetime.now())
                if self.imovel:
                    condominio = self.imovel.get_condominio()
                    condominio.set_nome(nome_condominio)
                    condominio.set_endereco(endereco)
                else:
                    condominio = Condominio.Condominio(
                        nome_condominio, endereco)

                if not self.imovel:
                    imovel.set_condominio(condominio)

                if self.imovel:
                    cadastro = Controller.editar_imovel(imovel)
                else:
                    cadastro = Controller.cadastrar_imovel(imovel)

                self.notify(cadastro)
                self.salvo = True
                self.acao = True

            case "bt_apagar_cadastro":
                self.mount(PopUpApagar())

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        # if self.salvo == False:
        #     self.mount(PopUp)

        if event.tabs.id == "tabs_anuncio":
            if event.tabs.active == self.query_one("#tab_anuncio", Tab).id:
                self.query_one("#container_cadastro").display = "none"
                self.query_one("#container_anuncio").display = "block"
            else:
                self.query_one("#container_anuncio").display = "none"
                self.query_one("#container_cadastro").display = "block"
        else:
            try:
                if event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
                    self.app.switch_screen("tela_cadastro_pessoa")

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

            except:
                pass
