class Venda:
    def __init__(self, cliente, carrinho, modo_pagamento):
        self.cliente = cliente
        self.carrinho = carrinho
        self.modo_pagamento = modo_pagamento

    def get_produtos(self):
        produtos = []
        for produto in self.carrinho:
            produtos.append(produto)
        return produtos
    
    def get_cliente(self):
        return self.cliente
    
    def get_modo_pagamento(self):
        return self.modo_pagamento

    def __str__(self):
        return (f"Venda [cliente={self.cliente.get_nome()}, produtos={', '.join([produto for produto in self.carrinho])}, "
                f"modo_pagamento={self.modo_pagamento}]")
