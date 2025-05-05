import Estoque
import Funcionario
import Cliente
import Fornecedor


class Loja:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self.estoque = Estoque()
        self.pessoas = []
        self.quantidade_funcionarios = self.set_quantidade()
        self.quantidade_clientes = self.set_quantidade()
        self.quantidade_fornecedores = self.set_quantidade()
        self.faturamento = 0

    def realizar_compra(self, cliente, produtos):  # ou realizar_venda()?
        # Pedir dados do cliente?
        # Ver se cliente está cadastrado
        # Remover produto do estoque, diminuir quantidade do produto no estoque
        # Somar preço do produto ao faturamento da loja
        # Permitir usuario de realizar mais compras? Implementar lógica de um carrinho?
        # Receber uma lista de produtos?
        # Usar um for em uma lista de produtos passando para cada produto o realizar_compra
        for produto_carrinho in produtos:
            for produto_estoque in self.estoque.get_produtos():
                if produto_carrinho == produto_estoque:
                    if produto_carrinho.get_quantidade() == produto_estoque.get_quantidade():
                        Estoque.remover_produto(produto_estoque)
                    else:
                        produto_estoque.set_quantidade(
                            produto_estoque.get_quantidade() - produto_carrinho.get_quantidade())
                self.faturamento += produto_carrinho.get_preco() * produto_carrinho.get_quantidade()

    def gerar_recibo(self, cliente, produtos, modo_pagamento):
        total = sum(produto.get_preco() * produto.get_quantidade() for produto in produtos)
        recibo = f'''
Recibo de Compra:
Nome do Cliente: {cliente.get_nome()}
CPF do Cliente: {cliente.get_cpf()}
CNPJ da Loja: {self.cnpj}
Nome da Loja: {self.nome}
Produtos Comprados: {', '.join([produto for produto in produtos])}
Total: {total}
Modo de Pagamento: {modo_pagamento}
            '''
        # Modo de Pagamento: {if (modo_pagamento == "crédito") print("Parcelas")}
        # Data: {}
        # Hora: {}
        return recibo

    def cadastrar(self, pessoa):
        if pessoa not in self.pessoas:
            self.pessoas.append(pessoa)
            self.set_quantidade()
            return True
        return False

    def remover(self, pessoa):
        if pessoa in self.pessoas:
            self.pessoas.remove(pessoa)
            self.set_quantidade()
            return True
        return False

    def set_quantidade(self):
        self.quantidade_clientes = 0
        self.quantidade_fornecedores = 0
        self.quantidade_funcionarios = 0

        for pessoa in self.pessoas:
            if isinstance(pessoa, Cliente):
                self.quantidade_clientes += 1
            elif isinstance(pessoa, Fornecedor):
                self.quantidade_fornecedores += 1
            self.quantidade_funcionarios += 1

    def get_quantidade_funcionarios(self):
        return self.quantidade_funcionarios

    def get_quantidade_clientes(self):
        return self.quantidade_clientes

    def get_quantidade_fornecedores(self):
        return self.quantidade_fornecedores

    def get_faturamento(self):
        return self.faturamento

    def is_cliente_cadastrado(self, cpf):
        for cliente in self.clientes:
            if cliente.get_cpf() == cpf:
                return True
        return False

    def get_cliente_por_cpf(self, cpf):
        for cliente in self.clientes:
            if cliente.get_cpf() == cpf:
                return cliente
        return None

    def get_produto_por_id(self, id):
        for produto in self.estoque.get_produtos():
            if produto.get_id() == id:
                return produto
        return None
