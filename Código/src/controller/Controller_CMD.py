from model import Cliente, Produto
from view import View
from model import Init


class Controller:

    def cadastrar_cliente(nome, cpf, rg, telefone, endereco, email):
        if nome == "":
            View.mostrar_mensagem("Nome está vazio")
            return
        if len(cpf) != 11:
            View.mostrar_mensagem("CPF inválido")
            return
        if not len(rg) <= 8 and not len(rg) >= 7:
            View.mostrar_mensagem("RG inválido")
            return
        if not len(telefone) <= 9 and not len(telefone) >= 8:
            View.mostrar_mensagem("Telefone inválido")
            return
        if endereco == "":
            View.mostrar_mensagem("Endereco está vazio")
            return
        if email == "":
            View.mostrar_mensagem("Email está vazio")
            return

        cliente = Cliente(nome, cpf, rg, telefone, endereco, email)
        cadastrado = Init.loja.cadastrar(cliente)

        if cadastrado:
            View.mostrar_mensagem(f"Cliente cadastrado! {cliente}")
        else:
            View.mostrar_mensagem("ERRO ao cadastrar cliente")

    def cadastrar_produto(nome, marca, modelo, cor, preco, quantidade, categoria):
        try:
            preco = float(preco)
        except ValueError:
            View.mostrar_mensagem("Preço incorreto")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            View.mostrar_mensagem("Quantidade incorreta")
            return

        if nome == "":
            View.mostrar_mensagem("Nome está vazio")
            return
        if marca == "":
            View.mostrar_mensagem("Nome está vazio")
            return
        if modelo == "":
            View.mostrar_mensagem("Nome está vazio")
            return
        if cor == "":
            View.mostrar_mensagem("Nome está vazio")
            return
        if preco == "":
            View.mostrar_mensagem("Endereco está vazio")
            return
        if quantidade == "":
            View.mostrar_mensagem("Email está vazio")
            return
        if categoria == "":
            View.mostrar_mensagem("Nome está vazio")
            return

        produto = Produto(nome, marca, modelo, cor,
                          preco, quantidade, categoria)
        cadastrado = Init.loja.get_estoque().adicionar_produto(produto)

        if cadastrado:
            View.mostrar_mensagem(f"Produto cadastrado! {produto}")
        else:
            View.mostrar_mensagem("ERRO ao cadastrar produto")

    def editar_produto(id, nome, marca, modelo, cor, preco, quantidade, categoria):
        produto = Init.loja.get_estoque().get_produto_por_id(id)
        if not produto:
            View.mostrar_mensagem("ERRO")
            return
        if nome != "":
            produto.set_nome(nome)
        if marca != "":
            produto.set_marca(marca)
        if modelo != "":
            produto.set_modelo(modelo)
        if cor != "":
            produto.set_cor(cor)
        if preco != "":
            try:
                preco = float(preco)
            except ValueError:
                View.mostrar_mensagem(f"O valor {preco} está incorreto")
                return
            produto.set_preco(preco)

        if quantidade != "":
            try:
                int(quantidade)
            except ValueError:
                View.mostrar_mensagem(f"O valor {quantidade} está incorreto")
                return
            produto.set_quantidade(quantidade)

        if categoria != "":
            produto.set_categoria(categoria)

        View.mostrar_mensagem(f"Produto editado com sucesso\n {produto}")

    def editar_cliente(self, cpf, dados):
        cliente = Init.loja.get_cliente_por_cpf(cpf)
        if not cliente:
            View.mostrar_mensagem("ERRO")
            return
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
        View.mostrar_mensagem(f"Cliente editado com sucesso\n {cliente}")
