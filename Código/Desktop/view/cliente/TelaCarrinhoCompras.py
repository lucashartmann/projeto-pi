from textual.screen import Screen
from textual.widgets import Static, Checkbox, Select
from textual.containers import HorizontalGroup, VerticalGroup

from textual_image.widget import Image


class TelaCarrinhoCompras(Screen):
    def compose(self):
        with HorizontalGroup():
            with VerticalGroup(id="produtos"):
                pass
            with VerticalGroup(id="pagamento"):
                yield Static("Total: R$ 0,00")
                yield Static("Forma de Pagamento:")
                yield Checkbox("Cartão de Débito")
                yield Checkbox("Cartão de Crédito", id="chx_cartao_credito")
                yield Checkbox("Boleto")
                yield Checkbox("Pix")
                if self.query("#chx_cartao_credito").value == True:
                    yield Static("Parcelamento:")
                    yield Select([("1x", "1x"), ("2x", "2x"), ("3x", "3x"), ("4x", "4x"), ("5x", "5x"), ("6x", "6x"), ("7x", "7x"), ("8x", "8x"), ("9x", "9x"), ("10x", "10x"), ("11x", "11x"), ("12x", "12x")])
