from datetime import datetime


class Venda:
    def __init__(self, cliente, carrinho, modo_pagamento):
        self.cliente = cliente
        self.itens = carrinho.listar_produtos()
        self.modo_pagamento = modo_pagamento
        self.parcelas = 0
        self.total = self.calcular_total()

    def calcular_total(self):
        for item in self.itens:
            self.total += item.get_preco() * item.get_quantidade()
        return self.total

    def aplicar_venda(self, loja):
        for item in self.itens:
            produto_carrinho = item
            quantidade = item.get_quantidade()
            for produto_estoque in loja.get_estoque().get_produtos():
                if produto_estoque.get_id() == produto_carrinho.get_id():
                    if produto_estoque.get_quantidade() == quantidade:
                        loja.get_estoque().remover_produto(produto_estoque)
                    else:
                        produto_estoque.set_quantidade(
                            produto_estoque.get_quantidade() - quantidade)
            loja.faturamento += produto_carrinho.get_preco() * quantidade

    def gerar_recibo(self, loja):
        produtos_str = "\n".join(item for item in self.itens)

        if self.modo_pagamento == 1:
            pagamento = "Cartão de Crédito"
            valor_parcela = self.total / self.parcelas
            parcelas_info = f"{self.parcelas}x de R$ {valor_parcela:.2f}"
        elif self.modo_pagamento == 2:
            pagamento = "Cartão de Débito"
            parcelas_info = "À vista"
        elif self.modo_pagamento == 3:
            pagamento = "Dinheiro"
            parcelas_info = "À vista"

        recibo = f"""
    ========= RECIBO =========
    Cliente: {self.cliente.get_nome()} (CPF: {self.cliente.get_cpf()})
    Loja: {loja.get_nome()} - CNPJ: {loja.get_cnpj()}

    Itens Comprados:
    {produtos_str}

    Total: R$ {self.total:.2f}
    Pagamento: {pagamento} | {parcelas_info}
    ===========================
    """
        return recibo
