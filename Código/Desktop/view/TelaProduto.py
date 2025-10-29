from textual.widgets import Input, Label, Button, Footer, Header, Select, Tab, Tabs
from textual.screen import Screen
from textual.containers import HorizontalGroup, Grid
from controller import Controller
from model.Usuario import TipoUsuario
from model import Init


class TelaProduto(Screen):

    CSS_PATH = "css/TelaProduto.tcss"

    def compose(self):
        yield Header()
        if Init.usuario.get_tipo() == TipoUsuario.ADMINISTRADOR:

            yield Tabs(Tab("Cadastro Produto", id="tab_cadastro_produto"), Tab("Estoque", id="tab_estoque"), Tab("Cadastro Pessoa", id="tab_cadastro_pessoa"), Tab("Clientela", id="tab_clientela"), Tab("Cadastro Usuario", id="tab_cadastro_usuario"), Tab("Usuarios Cadastrados", id="tab_usuario_cadastrados"), Tab("Dados da Loja", id="tab_dados_loja"))
        else:
            yield Tabs(Tab("Cadastro Produto", id="tab_cadastro_produto"), Tab("Estoque", id="tab_estoque"), Tab("Cadastro Pessoa", id="tab_cadastro_pessoa"), Tab("Clientela", id="tab_clientela"), Tab("Dados da Loja", id="tab_dados_loja"))

        with Grid():
            yield Label("ID do Produto:", id="lb_id")
            yield Input(placeholder="ID aqui", id="input_id")
            yield Label("Nome:", id="lbl_nome")
            yield Input(placeholder="Nome aqui", id="inpt_nome")
            yield Label("Marca:")
            yield Input(placeholder="Marca aqui", id="inpt_marca")
            yield Label("Modelo:", id="lbl_modelo")
            yield Input(placeholder="Modelo aqui", id="inpt_modelo")
            yield Label("Cor:", id="lbl_cor")
            yield Input(placeholder="Cor aqui", id="inpt_cor")
            yield Label("Preço:", id="lbl_preco")
            yield Input(placeholder="Preço aqui", id="inpt_preco")
            yield Label("Quantidade:", id="lbl_quant")
            yield Input(placeholder="Quantidade aqui", id="inpt_quant")
            yield Select([("produto", 'produto')])
        with HorizontalGroup(id="hg_operacoes"):
            yield Button("Limpar", id="bt_limpar")
            yield Button("Cadastrar", id="bt_cadastrar")
            yield Button("Voltar", id="bt_voltar")
        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_estoque", Tab).id:
            self.app.switch_screen("tela_estoque")
        elif event.tabs.active == self.query_one("#tab_cadastro_pessoa", Tab).id:
            self.app.switch_screen("tela_pessoa")
        elif event.tabs.active == self.query_one("#tab_clientela", Tab).id:
            self.app.switch_screen("tela_clientela")
        elif event.tabs.active == self.query_one("#tab_cadastro_usuario", Tab).id:
            self.app.switch_screen("tela_usuario")
        elif event.tabs.active == self.query_one("#tab_usuarios_cadastrados", Tab).id:
            self.app.switch_screen("tela_usuarios_cadastrados")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_cadastro_produto", Tab).id

    def cadastro(self):
        dados = []
        for input in self.query(Input):
            dados.append(input.value.upper())
        if self.screen.valor_select != "Nova categoria":
            dados.append(self.screen.valor_select)
        elif self.screen.montou:
            dados.append(self.query_one("#inpt_categoria", Input).value)
        else:
            dados.append("")
        resultado = Controller.cadastrar_produto(dados)
        self.notify(str(resultado), markup=False)
        self.screen.on_mount()

    def on_button_pressed(self, evento: Button.Pressed):
        match evento.button.id:
            case "bt_cadastrar":
                if self.screen.montou:
                    self.screen.montou = False
                    self.query_one("#lbl_categoria").remove()
                    self.query_one("#inpt_categoria").remove()
                self.cadastro()
            case "bt_remover":
                input_id = self.query_one("#input_id").value
                mensagem = Controller.remover_produto(input_id)
                self.notify(str(mensagem), markup=False)
            case "bt_editar":
                if self.screen.montou:
                    self.screen.montou = False
                    self.query_one("#lbl_categoria").remove()
                    self.query_one("#inpt_categoria").remove()
                input_id = self.query_one("#input_id", Input).value
                dados = []
                for input in self.query(Input)[1:]:
                    dados.append(input.value.upper())
                if self.screen.valor_select != "Nova categoria":
                    dados.append(self.screen.valor_select)
                elif self.screen.montou:
                    dados.append(self.query_one(
                        "#inpt_categoria", Input).value)
                else:
                    dados.append("")
                mensagem = Controller.editar_produto(input_id, dados)
                self.notify(str(mensagem), markup=False)
                self.screen.on_mount()
