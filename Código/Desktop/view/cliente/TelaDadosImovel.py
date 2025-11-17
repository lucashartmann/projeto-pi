from textual.widgets import Static, Button, ListItem, ListView, Footer, Header, Select, Checkbox, Input, Tab, Tabs
from textual import on
from textual.screen import Screen
from textual.containers import VerticalScroll, HorizontalGroup, Container, VerticalGroup, Grid

from textual_image.widget import Image 

from model import Init, Administrador, Corretor, Cliente, Imovel
from controller import Controller

from io import BytesIO


class TelaDadosImovel(Screen):
    TITLE = "Dados do Imóvel"
    
    CSS_PATH = "css/TelaDadosImovel.tcss"
    
    def compose(self):
        yield Header()
        if isinstance(Init.usuario_atual, Administrador.Administrador):
            yield Tabs(Tab("Cadastro de Imoveis", id="tab_cadastro_imovel"), Tab("Cadastro de Pessoas", id="tab_cadastro_pessoa"), Tab("Estoque", id="tab_estoque"), Tab("Servidor", id="tab_servidor"), Tab("Dados Cliente", id="tab_dados_cliente"), Tab("Estoque Cliente", id="tab_comprar"), Tab("Dados da imobiliaria", id="tab_dados_imobiliaria"))
        else:
            yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Dados", id="tab_dados_cliente"))
        
        with HorizontalGroup(id="titulo"):
            yield Static("Sala Comercial a venda no Centro de Porto Alegre", classes="titulo")
            yield Static("R$ 255.000,00", classes="valor")
        yield Static("Centro Histórico, Porto Alegre - RS")
        
        with HorizontalGroup():
            with VerticalScroll(id="dados_imovel"):
                yield Image(r"assets\apartamento1\5661162882.jpg")
                with HorizontalGroup(id="galeria_fotos"):
                    yield Image(r"assets\apartamento1\5661162882.jpg")
                    yield Image(r"assets\apartamento1\5661162882.jpg")
                    yield Image(r"assets\apartamento1\5661162882.jpg")
                    yield Image(r"assets\apartamento1\5661162882.jpg")
                    yield Image(r"assets\apartamento1\5661162882.jpg")
                yield Static("Descrição", id="stt_descricao", classes="titulo")
                yield Static("Excelente sala comercial na rua Demétrio Ribeiro, bairro Centro Histórico. A sala está distribuída em sala de recepção, atendimento, cozinha e lavabo. Ficam os móveis fixos. Edifício com elevador, portaria, interfone e câmera de monitoramento. Andar Baixo", id="descricao")
                yield Static("Infraestrutura", id="stt_infraestrutura", classes="titulo")
                with Grid(id="container_checkbox"):
                    yield Checkbox("Piscina")
                    yield Checkbox("Churrasqueira")
                yield Static("Mapa", id="mapa", classes="titulo")
            with VerticalScroll(id="entrar_contato"):
                with HorizontalGroup():
                    yield Button("Agendar Visita")
                    yield Button("Whatsapp", id="whatsapp")
                yield Static("Valor Venda:")
                yield Static("R$ 255.000,00", classes="valor")
                with HorizontalGroup():
                    yield Static("Condominio:")
                    yield Static("R$ 360,00", classes="valor")
                with HorizontalGroup():
                    yield Static("IPTU:")
                    yield Static("R$ 10,00", classes="valor")
                yield Button("Entrar em contato", id="bt_contato")
                yield Static("Um especialista irá entrar em contato por email ou whatsapp")
            
            
        
        yield Footer(show_command_palette=False)