import string
import random

class Produto:

    def __init__(self, nome, marca, modelo, cor, preco, quantidade, categoria):
        self.id = 0
        self.codigo = self.gerar_codigo_com_prefixo(prefixo='SKU-')
        self.nome = nome
        self.cor = cor
        self.preco = preco
        self.marca = marca
        self.modelo = modelo
        self.quantidade = quantidade
        self.categoria = categoria
        self.descricao = ""
        self.imagem = ""
        
    
    def gerar_codigo_com_prefixo(self, prefixo='PROD-', tamanho_sufixo=6):
        sufixo_caracteres = string.ascii_uppercase + string.digits
        sufixo = ''.join(random.choice(sufixo_caracteres) for _ in range(tamanho_sufixo))
        codigo = f'{prefixo}{sufixo}'
        return codigo
    
    def get_codigo(self):
        return self.codigo
    
    def set_codigo(self, novo_codigo):
        self.codigo = novo_codigo

    def get_descricao(self):
        return self.descricao
    
    def set_descricao(self, descricao):
        self.descricao = descricao
        
    def get_imagem(self):
        return self.imagem

    def set_imagem(self, imagem):
        self.imagem = imagem

    def editar_campo(self, nome_campo, setter):
        while True:
            novo_valor = input(f"Digite o novo {nome_campo}: ").upper()
            validacao = len(novo_valor) > 0
            if validacao:
                setter(novo_valor)
                print(f"{nome_campo} atualizado com sucesso!\n")
                break
            print(f"{nome_campo} inválido!")

    def get_quantidade(self):
        return self.quantidade

    def get_nome(self):
        return self.nome

    def get_categoria(self):
        return self.categoria

    def get_marca(self):
        return self.marca

    def get_modelo(self):
        return self.modelo

    def get_cor(self):
        return self.cor

    def get_preco(self):
        return self.preco

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def set_nome(self, nome):
        self.nome = nome

    def set_categoria(self, categoria):
        self.categoria = categoria

    def set_cor(self, cor):
        self.cor = cor

    def set_preco(self, preco):
        self.preco = preco

    def set_marca(self, marca):
        self.marca = marca

    def set_modelo(self, modelo):
        self.modelo = modelo

    def set_quantidade(self, quantidade):
        self.quantidade = quantidade

    def __str__(self):
        return (f"Produto [id = {self.get_id()}, nome = {self.get_nome()}, marca = {self.get_marca()}, modelo = {self.get_modelo()}, cor = {self.get_cor()}, "
                f"preco = {self.get_preco()}, quantidade = {self.get_quantidade()}, categoria = {self.get_categoria()}]")

