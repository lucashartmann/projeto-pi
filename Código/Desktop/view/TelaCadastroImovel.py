from textual.screen import Screen, ModalScreen
from textual.widgets import MaskedInput, Static, TextArea, Tab, Tabs, Select, Checkbox, Button, Header, Footer
from textual.containers import Horizontal, Vertical, Grid, VerticalScroll, Center

import requests
import datetime

from model import Init, Imovel, Administrador, Corretor, Gerente, Endereco, Anuncio, Condominio, Captador
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
            remocao = Controller.remover_imovel(ref)
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
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"),  Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"), Tab("Servidor", id="tab_servidor"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"))
        elif isinstance(Init.usuario_atual, Corretor.Corretor):
            yield Tabs(Tab('Atendimento', id="tab_atendimento"), Tab("Cadastro de Venda/Aluguel", id="tab_cadastro_venda_aluguel"), Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"))
        elif isinstance(Init.usuario_atual, Gerente.Gerente):
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
                yield Select([(valor.value, valor) for valor in Imovel.Categoria], id="select_categoria")
                yield Static("Situação:", id="stt_situacao")
                yield Select([(valor.value, valor) for valor in Imovel.Situacao], id="select_situacao")
                yield Static("Estado:", id="stt_estado_select")
                yield Select([(valor.value, valor) for valor in Imovel.Estado], id="select_estado")
                yield Static("Ocupação:", id="stt_ocupacao")
                yield Select([(valor.value, valor) for valor in Imovel.Ocupacao], id="select_ocupacao")
                yield Static("Status:", id="stt_status")
                yield Select([(valor.value, valor) for valor in Imovel.Status], id="select_status")
                yield Static("Nome do Condomínio", id="stt_nome_condominio")
                yield TextArea(id="ta_nome_condominio")
                yield Static("Ano de Construção", id="stt_ano_construcao")
                yield MaskedInput(template="00/00/0000", id="ta_ano_construcao")
                yield Static("Andar", id="stt_andar")
                yield MaskedInput(template="00", id="ta_andar")
                yield Static("Rua", id="stt_rua")
                yield TextArea(disabled=True, id="ta_rua")
                yield Static("Número", id="stt_numero")
                yield TextArea(id="ta_numero")
                yield Static("Complemento", id="stt_complemento")
                yield TextArea(id="ta_complemento")
                yield Static("Bloco", id="stt_bloco")
                yield TextArea(id="ta_bloco")
                yield Static("CEP", id="stt_cep")
                yield MaskedInput(template="00000-000", id="ta_cep")
                yield Static("Bairro", id="stt_bairro")
                yield TextArea(disabled=True, id="ta_bairro")
                yield Static("Cidade", id="stt_cidade")
                yield TextArea(disabled=True, id="ta_cidade")
                yield Static("Estado", id="stt_estado")
                yield MaskedInput(template="00", disabled=True, id="ta_estado")
                yield Static("Salas", id="stt_salas")
                yield MaskedInput(template="00", id="ta_salas")
                yield Static("Banheiros", id="stt_banheiros")
                yield MaskedInput(template="00", id="ta_banheiros")
                yield Static("Vagas", id="stt_vagas")
                yield MaskedInput(template="00", id="ta_vagas")
                yield Static("Varandas", id="stt_varandas")
                yield MaskedInput(template="00", id="ta_varandas")
                yield Static("Quartos", id="stt_quartos")
                yield MaskedInput(template="00", id="ta_quartos")
                yield Static("Área Total", id="stt_area_total")
                yield MaskedInput(template="000.000m²", id="ta_area_total")
                yield Static("Área Privativa", id="stt_area_privativa")
                yield MaskedInput(template="000.000m²", id="ta_area_privativa")
                yield Static("Valor Venda:", id="stt_venda")
                yield MaskedInput(template="000.000.000", id="ta_venda")
                yield Static("Valor Aluguel:", id="stt_aluguel")
                yield MaskedInput(template="000.000.000", id="ta_aluguel")
                yield Static("Valor Condomínio:", id="stt_condominio")
                yield MaskedInput(template="000.000.000", id="ta_condominio")
                yield Static("Valor IPTU:", id="stt_iptu")
                yield MaskedInput(template="000.000.000", id="ta_iptu")

            with Vertical(id="container_anuncio"):
                yield Static("Titulo")
                with Center():
                    yield TextArea(id="ta_titulo_anuncio")
                yield Static("Descriçao")
                with Center():
                    yield TextArea(id="ta_descricao_anuncio")
                yield Static("Apartamento")

                with Grid(id="container_info_imovel"):
                    yield Checkbox("Aceita Pet", id="imovel_pet")
                    yield Checkbox("Churrasqueira", id="imovel_churrasqueira")
                    yield Checkbox("Armarios Embutidos", id="imovel_armarios_embutidos")
                    yield Checkbox("Cozinha Americana", id="imovel_cozinha_americana")
                    yield Checkbox("Area de Servico", id="imovel_area_servico")
                    yield Checkbox("Suite Master", id="imovel_suite_master")
                    yield Checkbox("Banheiro com janela", id="imovel_banheiro_janela")
                    yield Checkbox("Piscina", id="imovel_piscina")
                    yield Checkbox("Lareira", id="imovel_lareira")
                    yield Checkbox("Ar-condicionado", id="imovel_ar")
                    yield Checkbox("Semi-Mobiliado", id="imovel_semi_mobiliado")
                    yield Checkbox("Mobiliado", id="imovel_mobiliado")
                    yield Checkbox("Dependencia de Empregada", id="imovel_dependencia_empregada")
                    yield Checkbox("Dispensa", id="imovel_dispensa")
                    yield Checkbox("Deposito", id="imovel_deposito")

                yield Static("Condomínio")
                with Grid(id="container_info_condominio"):
                    yield Checkbox("Churrasqueira Coletiva", id="condominio_churrasqueira")
                    yield Checkbox("Piscina", id="condominio_piscina")
                    yield Checkbox("Piscina Infantil", id="condominio_piscina_infantil")
                    yield Checkbox("Piscina Aquecida", id="condominio_piscina_aquecida")
                    yield Checkbox("Quiosque", id="condominio_quiosque")
                    yield Checkbox("Sauna", id="condominio_sauna")
                    yield Checkbox("Quadra de Esportes", id="condominio_quadra_esportes")
                    yield Checkbox("Jardim", id="condominio_jardim")
                    yield Checkbox("Salão de Festas", id="condominio_salao_festas")
                    yield Checkbox("Academia", id="condominio_academia")
                    yield Checkbox("Sala de Jogos", id="condominio_sala_jogos")
                    yield Checkbox("Playground", id="condominio_playground")
                    yield Checkbox("Brinquedoteca", id="condominio_brinquedoteca")
                    yield Checkbox("Vaga Coberta", id="condominio_vaga_coberta")
                    yield Checkbox("Estacionamento", id="condominio_estacionamento")
                    yield Checkbox("Vaga para Visitantes", id="condominio_vaga_visitantes")
                    yield Checkbox("Mercado", id="condominio_mercado")
                    yield Checkbox("Mesa de Sinuca", id="condominio_sinuca")
                    yield Checkbox("Mesa de Ping-Pong", id="condominio_ping_pong")
                    yield Checkbox("Mesa de Pebolim", id="condominio_pebolim")
                    yield Checkbox("Quadra de Tenis", id="condominio_tenis")
                    yield Checkbox("Quadra de Futebol", id="condominio_futebol")
                    yield Checkbox("Quadra de Basquete", id="condominio_basquete")
                    yield Checkbox("Quadra de Volei", id="condominio_volei")
                    yield Checkbox("Quadra de Areia", id="condominio_areia")
                    yield Checkbox("Bicicletario", id="condominio_bicicletario")
                    yield Checkbox("Heliponto", id="condominio_heliponto")
                    yield Checkbox("Elevador de Serviço", id="condominio_elevador_servico")

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

        if self.imovel and self.imovel.get_captador():
            container = ContainerFuncionario()
            container_captador.mount(container, after=container_captador.query_one(Static))
            container.query_one("#st_nome", Static).update(
                self.imovel.get_captador().get_nome())
            container.query_one("#st_telefone", Static).update(
                self.imovel.get_captador().get_telefone())
            container.query_one("#st_email", Static).update(
                self.imovel.get_captador().get_email())
        elif self.imovel is None and isinstance(Init.usuario_atual, Captador.Captador):
            container = ContainerFuncionario()
            container_captador.mount(container, after=container_captador.query_one(Static))
            container.query_one("#st_nome", Static).update(
                Init.usuario_atual.get_nome())
            container.query_one("#st_telefone", Static).update(
                Init.usuario_atual.get_telefone())
            container.query_one("#st_email", Static).update(
                Init.usuario_atual.get_email())

        container_corretor = self.query_one("#container_corretor", Vertical)

        if self.imovel and self.imovel.get_corretor():
            container = ContainerFuncionario()
            container_corretor.mount(container, after=container_corretor.query_one(Static))
            container.query_one("#st_nome", Static).update(
                self.imovel.get_corretor().get_nome())
            container.query_one("#st_telefone", Static).update(
                self.imovel.get_corretor().get_telefone())
            container.query_one("#st_email", Static).update(
                self.imovel.get_corretor().get_email())

        elif self.imovel is None and isinstance(Init.usuario_atual, Corretor.Corretor):
            container = ContainerFuncionario()
            container_corretor.mount(container, after=container_corretor.query_one(Static))
            container.query_one("#st_nome", Static).update(
                Init.usuario_atual.get_nome())
            container.query_one("#st_telefone", Static).update(
                Init.usuario_atual.get_telefone())
            container.query_one("#st_email", Static).update(
                Init.usuario_atual.get_email())

        container_proprietario = self.query_one(
            "#container_proprietario", Vertical)

        if self.imovel:
            container = ContainerFuncionario()
            container_proprietario.mount(container, after=container_proprietario.query_one(Static))
            container.query_one("#st_nome", Static).update(
                self.imovel.get_proprietario().get_nome())
            container.query_one("#st_telefone", Static).update(
                self.imovel.get_proprietario().get_telefone())
            container.query_one("#st_email", Static).update(
                self.imovel.get_proprietario().get_email())

        container_imagens = self.query_one("#container_imagens", Grid)

        if self.imovel and self.imovel.get_anuncio().get_imagens():
            for imagem in self.imovel.get_anuncio().get_imagens():
                container_imagens.mount(Image(imagem, id="st_imagem_anuncio"), after=container_imagens.query_one(Button))

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_cadastro_imovel", Tab).id

    def converter(self, string, dado, dadosejado, evento):
        if dado == "":
            return ""

        try:
            dado = dadosejado(dado.strip())
            return dado
        except Exception as e:
            self.notify(
                f"ERRO! Não foi possivel converter '{string} - {dado}' para {dadosejado}")
            evento.stop
            return

    def on_input_changed(self, evento: MaskedInput.Changed):
        self.salvo = False
        if evento.input.id == "ta_cep":
            cep = str(evento.input.value.strip().strip("-"))
            self.query_one("#ta_bairro", TextArea).clear()
            self.query_one("#ta_estado", MaskedInput).clear()
            self.query_one("#ta_rua", TextArea).clear()
            self.query_one("#ta_cidade", TextArea).clear()

            if len(cep) > 7:
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
                numero = self.converter("número", self.query_one(
                    "#ta_numero", TextArea).text, int, evento)
                complemento = self.query_one(
                    "#ta_complemento", TextArea).text.strip()
                bloco = self.query_one("#ta_bloco", TextArea).text.strip()

                cep = self.query_one(
                    "#ta_cep", MaskedInput).value.strip().strip("-")
                if not cep:
                    self.notify("ERRO! CEP inválido")
                    return
                cep = self.converter("CEP", cep, int, evento)
                bairro = self.query_one("#ta_bairro", TextArea).text
                cidade = self.query_one("#ta_cidade", TextArea).text
                estado = self.query_one(
                    "#ta_estado", MaskedInput).value.strip()
                salas = self.converter("salas", self.query_one(
                    "#ta_salas", MaskedInput).value, int, evento)
                banheiros = self.converter("banheiros", self.query_one(
                    "#ta_banheiros", MaskedInput).value, int, evento)
                vagas = self.converter("vagas", self.query_one(
                    "#ta_vagas", MaskedInput).value, int, evento)
                varandas = self.converter("varandas", self.query_one(
                    "#ta_varandas", MaskedInput).value, int, evento)
                quartos = self.converter("quartos", self.query_one(
                    "#ta_quartos", MaskedInput).value, int, evento)
                area_total = self.converter("area_total", self.query_one(
                    "#ta_area_total", MaskedInput).value.strip("m²"), float, evento)
                area_privativa = self.converter("area_privativa", self.query_one(
                    "#ta_area_privativa", MaskedInput).value.strip("m²"), float, evento)
                venda = self.converter("venda", self.query_one(
                    "#ta_venda", MaskedInput).value.strip("m²"), float, evento)
                aluguel = self.converter("aluguel", self.query_one(
                    "#ta_aluguel", MaskedInput).value.strip("m²"), float, evento)
                valor_condominio = self.converter("valor_condominio", self.query_one(
                    "#ta_condominio", MaskedInput).value.strip("m²"), float, evento)
                iptu = self.converter("iptu", self.query_one(
                    "#ta_iptu", MaskedInput).value.strip("m²"), float, evento)
                andar = self.query_one("#ta_andar", MaskedInput).value
                ano_construcao = self.query_one(
                    "#ta_ano_construcao", MaskedInput).value.split("/")
                if ano_construcao:
                    if ano_construcao[-1] and ano_construcao[1] and ano_construcao[0]:
                        ano_construcao = datetime.datetime(year=int(
                        ano_construcao[-1]), month=int(ano_construcao[1]), day=int(ano_construcao[0]))
                else:
                    ano_construcao = None

                endereco = Endereco.Endereco(rua, numero, bairro,
                                    cep, complemento, cidade)
                endereco.set_estado(estado)
                # anuncio.set_anexos()
                # anuncio.set_videos()
                # anuncio.set_fotos()
                titulo = self.query_one("#ta_titulo_anuncio", TextArea).text
                descricao = self.query_one(
                    "#ta_descricao_anuncio", TextArea).text
                anuncio = Anuncio.Anuncio()
                anuncio.set_titulo(titulo)
                anuncio.set_descricao(descricao)
                imovel = Imovel.Imovel(
                    endereco, status_imovel, categoria_imovel)
                imovel.set_anuncio(anuncio)
                imovel.set_andar(andar)
                imovel.set_ano_construcao(ano_construcao)
                imovel.set_area_privativa(area_privativa)
                # imovel.set_captador()
                imovel.set_area_total(area_total)
                imovel.set_bloco(bloco)
                # imovel.set_corretor()
                imovel.set_iptu(iptu)
                imovel.set_valor_condominio(valor_condominio)
                imovel.set_nome_condominio(nome_condominio)
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
                imovel.set_id(ref)
                imovel.set_data_modificacao(datetime.datetime.now)
                imovel.aceita_pet = self.query_one(
                    "#imovel_pet", Checkbox).value
                imovel.churrasqueira = self.query_one(
                    "#imovel_churrasqueira", Checkbox).value
                imovel.armarios_embutidos = self.query_one(
                    "#imovel_armarios_embutidos", Checkbox).value
                imovel.cozinha_americana = self.query_one(
                    "#imovel_cozinha_americana", Checkbox).value
                imovel.area_de_servico = self.query_one(
                    "#imovel_area_servico", Checkbox).value
                imovel.suite_master = self.query_one(
                    "#imovel_suite_master", Checkbox).value
                imovel.banheiro_com_janela = self.query_one(
                    "#imovel_banheiro_janela", Checkbox).value
                imovel.piscina = self.query_one(
                    "#imovel_piscina", Checkbox).value
                imovel.lareira = self.query_one(
                    "#imovel_lareira", Checkbox).value
                imovel.ar_condicionado = self.query_one(
                    "#imovel_ar", Checkbox).value
                imovel.semi_mobiliado = self.query_one(
                    "#imovel_semi_mobiliado", Checkbox).value
                imovel.mobiliado = self.query_one(
                    "#imovel_mobiliado", Checkbox).value
                imovel.dependencia_de_empregada = self.query_one(
                    "#imovel_dependencia_empregada", Checkbox).value
                imovel.dispensa = self.query_one(
                    "#imovel_dispensa", Checkbox).value
                imovel.deposito = self.query_one(
                    "#imovel_deposito", Checkbox).value
                cadastro = Controller.cadastrar_imovel(imovel)
                if nome_condominio:
                    condominio = Condominio.Condominio(
                        nome_condominio, endereco)
                    condominio.churrasqueira_coletiva = self.query_one(
                        "#condominio_churrasqueira", Checkbox).value
                    condominio.piscina = self.query_one(
                        "#condominio_piscina", Checkbox).value
                    condominio.piscina_infantil = self.query_one(
                        "#condominio_piscina_infantil", Checkbox).value
                    condominio.piscina_aquecida = self.query_one(
                        "#condominio_piscina_aquecida", Checkbox).value
                    condominio.quiosque = self.query_one(
                        "#condominio_quiosque", Checkbox).value
                    condominio.sauna = self.query_one(
                        "#condominio_sauna", Checkbox).value
                    condominio.quadra_de_esportes = self.query_one(
                        "#condominio_quadra_esportes", Checkbox).value
                    condominio.jardim = self.query_one(
                        "#condominio_jardim", Checkbox).value
                    condominio.salao_de_festas = self.query_one(
                        "#condominio_salao_festas", Checkbox).value
                    condominio.academia = self.query_one(
                        "#condominio_academia", Checkbox).value
                    condominio.sala_de_jogos = self.query_one(
                        "#condominio_sala_jogos", Checkbox).value
                    condominio.playground = self.query_one(
                        "#condominio_playground", Checkbox).value
                    condominio.brinquedoteca = self.query_one(
                        "#condominio_brinquedoteca", Checkbox).value
                    condominio.vaga_coberta = self.query_one(
                        "#condominio_vaga_coberta", Checkbox).value
                    condominio.estacionamento = self.query_one(
                        "#condominio_estacionamento", Checkbox).value
                    condominio.vaga_para_visitantes = self.query_one(
                        "#condominio_vaga_visitantes", Checkbox).value
                    condominio.mercado = self.query_one(
                        "#condominio_mercado", Checkbox).value
                    condominio.mesa_de_sinuca = self.query_one(
                        "#condominio_sinuca", Checkbox).value
                    condominio.mesa_de_ping_pong = self.query_one(
                        "#condominio_ping_pong", Checkbox).value
                    condominio.mesa_de_pebolim = self.query_one(
                        "#condominio_pebolim", Checkbox).value
                    condominio.quadra_de_tenis = self.query_one(
                        "#condominio_tenis", Checkbox).value
                    condominio.quadra_de_futebol = self.query_one(
                        "#condominio_futebol", Checkbox).value
                    condominio.quadra_de_basquete = self.query_one(
                        "#condominio_basquete", Checkbox).value
                    condominio.quadra_de_volei = self.query_one(
                        "#condominio_volei", Checkbox).value
                    condominio.quadra_de_areia = self.query_one(
                        "#condominio_areia", Checkbox).value
                    condominio.bicicletario = self.query_one(
                        "#condominio_bicicletario", Checkbox).value
                    condominio.heliponto = self.query_one(
                        "#condominio_heliponto", Checkbox).value
                    condominio.elevador_de_serviço = self.query_one(
                        "#condominio_elevador_servico", Checkbox).value

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

            except:
                pass
