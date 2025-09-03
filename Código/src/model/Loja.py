from model import Banco, Estoque


class Loja:
    def __init__(self, nome, cnpj):
        self.banco_dados = Banco.Banco()
        self.nome = nome
        self.cnpj = cnpj
        self.estoque = Estoque.Estoque()
        self.quantidade_funcionarios = self.set_quantidade()
        self.quantidade_clientes = self.set_quantidade()
        self.quantidade_fornecedores = self.set_quantidade()
        self.faturamento = 0

    def cadastrar(self, cliente):
        return self.banco_dados.cadastrar_cliente(cliente)

    def remover(self, cliente):
        return self.banco_dados.remover_cliente(cliente.get_cpf())

    def set_quantidade(self):
        self.quantidade_clientes = 0
        self.quantidade_fornecedores = 0
        self.quantidade_funcionarios = 0

        # for pessoa in self.pessoas:
        #     if isinstance(pessoa, Cliente):
        #         self.quantidade_clientes += 1
        #     elif isinstance(pessoa, Fornecedor):
        #         self.quantidade_fornecedores += 1
        #     self.quantidade_funcionarios += 1

    def get_lista_clientes(self):
        return self.banco_dados.get_lista_clientes()

    def get_estoque(self):
        return self.estoque

    def get_nome(self):
        return self.nome

    def get_cnpj(self):
        return self.cnpj

    def get_quantidade_funcionarios(self):
        return self.quantidade_funcionarios

    def get_quantidade_clientes(self):
        return self.quantidade_clientes

    def get_quantidade_fornecedores(self):
        return self.quantidade_fornecedores

    def get_faturamento(self):
        return self.faturamento

    def get_cliente_por_cpf(self, cpf):
        return self.banco_dados.get_cliente_por_cpf(cpf)

    def get_produto_por_id(self, id):
        return self.banco_dados.get_produto_por_id(id)
