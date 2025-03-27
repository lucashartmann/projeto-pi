from tkinter import *

class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        self.sextoContainer = Frame(master)
        self.sextoContainer["pady"] = 20
        self.sextoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Dados do usuário")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.nomeLabel = Label(self.segundoContainer,text="Nome", font=self.fontePadrao)
        self.nomeLabel.pack(side=LEFT)

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=LEFT)

        self.cpfLabel = Label(self.terceiroContainer, text="cpf", font=self.fontePadrao)
        self.cpfLabel.pack(side=LEFT)

        self.cpf = Entry(self.terceiroContainer)
        self.cpf["width"] = 30
        self.cpf["font"] = self.fontePadrao
        self.cpf["show"] = "*"
        self.cpf.pack(side=LEFT)

        self.rgLabel = Label(self.quartoContainer, text="RG", font=self.fontePadrao)
        self.rgLabel.pack(side=LEFT)

        self.rg = Entry(self.quartoContainer)
        self.rg["width"] = 30
        self.rg["font"] = self.fontePadrao
        self.rg["show"] = "*"
        self.rg.pack(side=LEFT)

        self.cadastrar = Button(self.quintoContainer)
        self.cadastrar["text"] = "Cadastrar"
        self.cadastrar["font"] = ("Calibri", "8")
        self.cadastrar["width"] = 12
        self.cadastrar.pack()

        self.mensagem = Label(self.sextoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

root = Tk()
app = Application(root)  
root.mainloop()