class Administrador:
    def __init__(self, email, username, senha):
        self.email = email
        self.username = username
        self.senha = senha
        self.id = None
        
    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_email(self):
        return self.email

    def set_email(self, value):
        self.email = value

    def get_username(self):
        return self.username

    def set_username(self, value):
        self.username = value

    def get_senha(self):
        return self.senha

    def set_senha(self, value):
        self.senha = value
