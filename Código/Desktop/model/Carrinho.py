from database.Banco import Banco


class Carrinho:
    def __init__(self):
        self.banco_dados = Banco()

    def adicionar_item(self, cpf, id_produto, quantidade):
        self.banco_dados.adicionar_carrinho(cpf, id_produto, quantidade)

    def remover_item(self,  cpf, id_produto):
        return self.banco_dados.remover_item_carrinho(cpf, id_produto)

    def listar_itens(self, cpf):
        return self.banco_dados.get_lista_produtos_carrinho(cpf)
    
    def get_item_por_id(self, cpf, id_produto):
        return self.banco_dados.get_item_carrinho_por_id(cpf, id_produto)

    def atualizar_quantidade_item(self, cpf, id_produto, quantidade):
        self.banco_dados.atualizar_quantidade_item_carrinho(cpf, id_produto, quantidade)
        
    def get_quantidade(self, id_produto):
        return self.banco_dados.get_quantidade_item_carrinho(id_produto)