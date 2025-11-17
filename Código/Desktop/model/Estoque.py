from database.Banco import Banco


class Estoque:

    def __init__(self):
        self.banco_dados = Banco()

    def cadastrar_imovel(self, imovel):
        return self.banco_dados.cadastrar_imovel(imovel)

    def remover_imovel(self, imovel):
        return self.banco_dados.remover_imovel(imovel.get_id())

    def get_lista_imoveis(self):
        return self.banco_dados.get_lista_imoveis()

    def get_lista_imoveis_disponiveis(self):
        return self.banco_dados.get_lista_imoveis_disponiveis()

    def get_imoveis_por_categoria(self, categoria):
        return self.banco_dados.get_imoveis_por_categoria(categoria)

    def get_imovel_por_codigo(self, codigo):
        return self.banco_dados.get_imovel_por_codigo(codigo)
    
    def adicionar_anexo(self, anexo, tipo, codigo):
        return self.banco_dados.adicionar_anexo(anexo, tipo, codigo)
   
