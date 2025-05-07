class Pessoa:
    def __init__(self, nome, cpf, rg, telefone, endereco, email):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.telefone = telefone
        self.endereco = endereco
        self.email = email

    def editar_campo(self, nome_campo, setter):
        while True:
            novo_valor = input(f"Digite o novo {nome_campo}: ")
            validacao = len(novo_valor) > 0
            if validacao:
                setter(novo_valor)
                print(f"{nome_campo} atualizado com sucesso!\n")
                break
            print(f"{nome_campo} inválido!")
    
    def get_nome(self):
        return self.nome
    
    def get_rg(self):
        return self.rg
    
    def get_telefone(self):
        return self.telefone
    
    def get_endereco(self):
        return self.endereco
    
    def get_email(self):
        return self.email

    def get_cpf(self):
        return self.cpf

    def set_nome(self, nome):
        self.nome = nome

    def set_cpf(self, cpf):
        self.cpf = cpf

    def set_rg(self, rg):
        self.rg = rg

    def set_telefone(self, telefone):
        self.telefone = telefone

    def set_endereco(self, endereco):
        self.endereco = endereco

    def set_email(self, email):
        self.email = email
