class Condominio:
    def __init__(self, nome, endereco):
        self.id = None
        self.nome = nome
        self.endereco = endereco
        self.filtros = dict()
        
    def set_filtros(self, filtros):
        self.filtros = filtros
        
    def get_filtros(self):
        return self.filtros
        
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id

    def get_endereco(self):
        return self.endereco
    
    def set_endereco(self, endereco):
        self.endereco = endereco

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome
