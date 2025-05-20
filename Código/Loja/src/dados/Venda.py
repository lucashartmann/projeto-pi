class Venda:
    def __init__(self, cliente, carrinho, modo_pagamento):
        self.cliente = cliente
        self.itens = carrinho.listar_produtos()
        self.modo_pagamento = modo_pagamento
        self.parcelas = 0
        self.total = cliente.get_carrinho().get_total()

    def set_parcelas(self, parcelas):
        self.parcelas = parcelas

    def aplicar_venda(self, loja):
        estoque = loja.get_estoque()
        for item in self.itens:
            quantidade = item.get_quantidade()
            for produto in estoque.get_lista_produtos():
                if produto.get_id() == item.get_id():
                    nova_qtd = produto.get_quantidade() - quantidade
                    if nova_qtd <= 0:
                        estoque.remover_produto(produto)
                    else:
                        produto.set_quantidade(nova_qtd)
                    break
            loja.faturamento += item.get_preco() * quantidade

    def gerar_recibo(self, loja):
        produtos_str = ""
        for produto, quantidade in self.itens.items():
            produtos_str += produto.get_nome() + " - Quantidade: " + str(quantidade) + "\n"
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
