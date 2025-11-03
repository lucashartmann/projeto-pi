from textual.screen import Screen
from textual.widgets import Static, Checkbox, Select, Tab, Tabs, Button
from textual.containers import HorizontalGroup, VerticalGroup

from textual_image.widget import Image

from model import Init
from controller import Controller

from io import BytesIO


class TelaCarrinhoCompras(Screen):
    CSS_PATH = "css/TelaCarrinhoCompras.tcss"

    lista_produtos = Init.cliente_atual.carrinho.listar_itens(
        Init.cliente_atual.get_cpf())
    lista_selecionados = []

    def compose(self):
        yield Tabs(Tab("Comprar", id="tab_comprar"), Tab("Carrinho", id="tab_carrinho_compras"), Tab("Dados", id="tab_dados_usuario"))
        with HorizontalGroup():
            with VerticalGroup(id="produtos"):
                if self.lista_produtos:
                    yield Button("Selecionar/Deselecionar todos", id="btn_selecionar_todos")
            # TODO: implementar funcionalidade de pagamento
            with VerticalGroup(id="pagamento"):
                yield Static("Total: [green]R$ 0,00 [/]")
                yield Static("Forma de Pagamento:")
                yield Checkbox("Cartão de Débito", classes="chbx_pagamento")
                yield Checkbox("Cartão de Crédito", id="chx_cartao_credito", classes="chbx_pagamento")
                yield Checkbox("Boleto", classes="chbx_pagamento")
                yield Checkbox("Pix", classes="chbx_pagamento")
                yield Button("Finalizar Pagamento")

    def atualizar_total(self):
        total = 0.0

        if not self.lista_selecionados:
            self.query_one("#pagamento").query_one(
                Static).update("Total: [green]R$ 0,00 [/]")
            return

        for produto in self.lista_produtos:
            quantidade = Init.cliente_atual.carrinho.get_quantidade(
                produto.get_id())
            total += produto.get_preco() * quantidade
        total_formatado = f"R$ {total:.2f}"
        self.query_one("#pagamento").query_one(Static).update(
            f"Total: [green]{total_formatado} [/]")

    def on_mount(self):
        self.montar_itens()

    def atualizar(self):
        self.lista_produtos = Init.cliente_atual.carrinho.listar_itens(
            Init.cliente_atual.get_cpf())
        self.query_one("#produtos").remove_children()
        self.montar_itens()

    def montar_itens(self):
        if self.lista_produtos:
            for produto in self.lista_produtos:
                horizontal = HorizontalGroup(
                    name=produto.get_id(), classes="item_produto")
                self.query_one("#produtos").mount(horizontal)
                if produto.get_imagem():
                    imagem = Image(BytesIO(produto.get_imagem()))
                    imagem.styles.width = 12
                    imagem.styles.height = 5
                    horizontal.mount(imagem)
                horizontal.mount(
                    Static(f"Nome: {produto.get_nome()}", classes="nome_produto"))
                horizontal.mount(
                    Static(f"Preço: R$ {produto.get_preco()}", classes="preco_produto"))
                horizontal.mount(
                    Static(f"Quantidade: {Init.cliente_atual.carrinho.get_quantidade(produto.get_id())}", classes="quantidade_produto"))
                horizontal.mount(Button("+"))
                horizontal.mount(Button("-"))
                horizontal.mount(Checkbox(classes="chbx_produto"))

        else:
            self.query_one("#produtos").mount(Static("Carrinho Vazio"))

    def on_button_pressed(self, evento: Button.Pressed):
        # Todo: Arrumar
        if evento.button.id == "btn_selecionar_todos":
            todos_selecionados = all(
                checkbox.value for checkbox in self.query(".chbx_produto"))
            for checkbox in self.query(".chbx_produto"):
                checkbox.value = not todos_selecionados
            if todos_selecionados:
                self.lista_selecionados.clear()
            else:
                self.lista_selecionados = [
                    produto.get_id() for produto in self.lista_produtos]

            return

        if evento.button.label == "+" or evento.button.label == "-":
            quantidade_atual = int(evento.button.parent.query_one(
                ".quantidade_produto").content.split(": ")[1])

            if evento.button.label == "+":
                nova_quantidade = quantidade_atual + 1
            elif evento.button.label == "-":
                nova_quantidade = quantidade_atual - 1

            if nova_quantidade < 1:
                for hg in self.query("#produtos").query(HorizontalGroup):
                    if hg.name == evento.button.parent.name:
                        remocao = Controller.remover_do_carrinho(hg.name)
                        if "ERRO" not in remocao:
                            hg.remove()
                        self.notify(remocao)
                        break

            mensagem = Controller.atualizar_quantidade_carrinho(
                evento.button.parent.name, nova_quantidade)
            self.notify(mensagem)

            if "ERRO" not in mensagem:
                self.atualizar()

    def on_checkbox_changed(self, evento: Checkbox.Changed):
        if "chbx_pagamento" in evento.checkbox.classes:
            for checkbox in self.query(Checkbox):
                if checkbox.value == True and evento.checkbox.value == True and checkbox.label != evento.checkbox.label:
                    evento.checkbox.value = False
                    self.notify("Selecione apenas uma forma de pagamento.")
                    break

        elif evento.checkbox.id == "#chx_cartao_credito" and evento.checkbox.value == True:
            self.mount(Static("Parcelamento:"))
            self.mount(Select([("1x", "1x"), ("2x", "2x"), ("3x", "3x"), ("4x", "4x"), ("5x", "5x"), ("6x", "6x"), (
                "7x", "7x"), ("8x", "8x"), ("9x", "9x"), ("10x", "10x"), ("11x", "11x"), ("12x", "12x")]))

        else:
            if evento.checkbox.parent.name not in self.lista_selecionados:
                self.lista_selecionados.append(evento.checkbox.parent.name)
            else:
                self.lista_selecionados.remove(evento.checkbox.parent.name)
            self.atualizar_total()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated):
        if event.tabs.active == self.query_one("#tab_comprar", Tab).id:
            self.app.switch_screen("tela_estoque_cliente")
        elif event.tabs.active == self.query_one("#tab_dados_usuario", Tab).id:
            self.app.switch_screen("tela_dados_usuario")

    def on_screen_resume(self):
        self.query_one(Tabs).active = self.query_one(
            "#tab_carrinho_compras", Tab).id
