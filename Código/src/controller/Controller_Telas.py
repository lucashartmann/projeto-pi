from model import Init, Cliente, Produto


class Controller():

    def editar_produto(self, produto, lista):
        if lista[0] != "":
            produto.set_nome(lista[0])
        if lista[1] != "":
            produto.set_marca(lista[1])
        if lista[2] != "":
            produto.set_modelo(lista[2])
        if lista[3] != "":
            produto.set_cor(lista[3])
        if lista[4] != "":
            try:
                float(lista[4])
            except ValueError:
                return (f"O valor {lista[4]} está incorreto")
            produto.set_preco(lista[4])
        if lista[5] != "":
            try:
                int(lista[5])
            except ValueError:
                return (f"O valor {lista[5]} está incorreto")
            produto.set_quantidade(lista[5])
        if lista[6] != "":
            produto.set_categoria(lista[6])
        return "Produto editado com sucesso"

    def editar_cliente(self, cliente, dados):
        if dados[0] != "":
            cliente.set_nome(dados[0])
        if dados[1] != "":
            cliente.set_cpf(dados[1])
        if dados[2] != "":
            cliente.set_rg(dados[2])
        if dados[3] != "":
            cliente.set_telefone(dados[3])
        if dados[4] != "":
            cliente.set_endereco(dados[4])
        if dados[5] != "":
            cliente.set_email(dados[5])
        return "Cliente editado com sucesso"

    def cadastrar_cliente(self, lista):
        cliente = Cliente.Cliente(
            lista[0], lista[1], lista[2], lista[3], lista[4], lista[5])
        cadastro = Init.loja.cadastrar(cliente)
        if cadastro:
            return "Cliente cadastrado com sucesso!"
        else:
            return "Erro ao cadastrar cliente"

    def cadastrar_produto(self, lista):
        if lista[4] != "":
            try:
                float(lista[4])
            except ValueError:
                return (f"O valor {lista[4]} está incorreto")
        if lista[5] != "":
            try:
                int(lista[5])
            except ValueError:
                return (f"O valor {lista[5]} está incorreto")
        produto = Produto.Produto(
            lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6])
        cadastro = Init.loja.get_estoque().adicionar_produto(produto)
        if cadastro:
            return "Produto cadastrado com sucesso!"
        else:
            return "Erro ao cadastrar produto"

    def remover_produto(self):
        pass

    def remover_cliente(self):
        pass

    def ver_produtos_estoque(self):
        return Init.loja.get_estoque().get_lista_produtos()
