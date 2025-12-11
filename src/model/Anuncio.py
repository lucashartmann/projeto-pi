class Anuncio:
    def __init__(self):
        self.id = None
        self.descricao = None
        self.titulo = None
        self.id = None
        self.imagens = []
        self.videos = []
        self.anexos = []
        
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id

    def get_descricao(self):
        return self.descricao

    def set_descricao(self, descricao):
        self.descricao = descricao

    def set_titulo(self, titulo):
        self.titulo = titulo

    def get_titulo(self):
        return self.titulo

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_imagens(self):
        return self.imagens

    def set_imagens(self, value):
        self.imagens = value

    def get_videos(self):
        return self.videos

    def set_videos(self, value):
        self.videos = value

    def get_anexos(self):
        return self.anexos

    def set_anexos(self, value):
        self.anexos = value
