import Cliente
import Fornecedor
import Funcionario
import Produto
import Estoque
import Loja

isCadastrado = False
usuario = 0
cliente = None


def login():
    menu = '''
##### LOGIN ######
1 - Cliente
2 - Admin
        '''
    print(menu)
    usuario = int(input("Digite o número correspondente ao usuário: "))
    if usuario == 1:
        menuCliente()
    elif usuario == 2:
        menuAdmin()
    else:
        print("Opção inválida. Tente novamente.")
        login()
    login()


def menuCliente():
    opcao = 0
    carrinho_compras = []
    while opcao < 1 or opcao > 8:
        menu = '''
##### MENU CLIENTE ######
1 - Cadastrar 
2 - Editar cadastro
3 - Adicionar produtos no Carrinho
4 - Realizar compra
5 - Ver produtos no carrinho
6 - Remover produto do carrinho
7 - Ver últimas compras
8 - Sair do menu
            '''
        print(menu)
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                cadastroPessoa()
            case 2:
                edicaoPessoa()
            case 3:
                carrinho_compras = carrinho_compras()
            case 4:
                realizar_compra(carrinho_compras)
            case 8:
                return 
            case _:
                print('Opção errada, tente novamente')
        menuCliente()


def menuAdmin():
    opcao = 0
    while opcao < 1 or opcao > 9:
        menu = '''
##### MENU ADMIN ######
1 -- Cadastrar Produto
2 -- Editar Produto
3 - Editar Cliente
4 -- Ver produto por nome
5 -- Ver produtos por marca
6 -- Ver produtos por categoria
7 -- Ver quantidade de tudo
8 -- Ver quantidade de produtos por marca
9 -- Ver quantidade de produtos por categoria
10 - Ver quantidade de produtos por modelo
11 -- Sair do menu
            '''
        print(menu)
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                cadastroProduto()
            case 2:
                edicaoProduto()
            case 3:
                edicaoPessoa()
            case 4, 5, 6:
                procurarProduto(opcao)
            case 7:
                print("Quantidade de clientes: ", Loja.get_quantidade_clientes(), "\nQuantidade de funcionários: ",
                      Loja.get_quantidade_funcionarios(), "\nQuantidade de fornecedores: ", Loja.get_quantidade_fornecedores())
            case 8, 9, 10:
                verQuantidadeProduto(opcao)
            case 11:
                return
            case _:
                print('Opção errada, tente novamente')
        menuAdmin()


def verQuantidadeProduto(opcao):
    if opcao == 7:
        marca = input("Digite a marca do produto: ")
        quantidade = Estoque.get_quantidade_produto_por_marca(marca)
        if quantidade is None:
            print("Produto não encontrado!")
            return
        print(f"Quantidade de produtos da marca {marca}: {quantidade}")
    elif opcao == 8:
        categoria = input("Digite a categoria do produto: ")
        quantidade = Estoque.get_quantidade_produto_por_categoria(categoria)
        if quantidade is None:
            print("Produto não encontrado!")
            return
        print(f"Quantidade de produtos da categoria {categoria}: {quantidade}")
    elif opcao == 9:
        modelo = input("Digite o modelo do produto: ")
        quantidade = Estoque.get_quantidade_produto_por_modelo(modelo)
        if quantidade is None:
            print("Produto não encontrado!")
            return
        print(f"Quantidade de produtos do modelo {modelo}: {quantidade}")


def procurarProduto(opcao):
    if opcao == 3:
        nome = input("Digite o nome do produto: ")
        produtos = Estoque.consultar_produtos_por_nome(nome)
        if produtos is None:
            print("Produto não encontrado!")
            return
        print("Produtos encontrados:")
        for produto in produtos:
            print(produto)
    elif opcao == 4:
        marca = input("Digite a marca do produto: ")
        produtos = Estoque.consultar_produtos_por_marca(marca)
        if produtos is None:
            print("Produto não encontrado!")
            return
        print("Produtos encontrados:")
        for produto in produtos:
            print(produto)
    elif opcao == 5:
        categoria = input("Digite a categoria do produto: ")
        produtos = Estoque.consultar_produtos_por_categoria(categoria)
        if produtos is None:
            print("Produto não encontrado!")
            return
        print("Produtos encontrados:")
        for produto in produtos:
            print(produto)


def cadastroPessoa():
    while True:
        nome = input("Digite o nome: ")
        if len(nome) > 0:
            break
    while True:
        cpf = input("Digite o CPF: ")
        if len(cpf) == 11:
            break
    while True:
        telefone = input("Digite o telefone: ")
        if len(telefone) == 11:
            break
    while True:
        email = input("Digite o email: ")
        if len(email) > 0:
            break
    while True:
        rg = input("Digite a RG: ")
        if len(rg) > 0:
            break
    while True:
        endereco = input("Digite o endereço: ")
        if len(endereco) > 0:
            break
    if usuario == 1:
        cliente = Cliente(nome, cpf, rg, telefone, endereco, email)
        Loja.cadastrar(cliente)
        isCadastrado = True
        return
    # Mudar para fornecedor ou funcionario
    pessoa = (nome, cpf, rg, telefone, endereco, email)


def edicaoPessoa():
    if usuario == 1:
        if isCadastrado == False:
            print("Você não está cadastrado!")
            return
    else:
        print("Digite o CPF do cliente que deseja editar: ")
        cpf = input()
        pessoa = Loja.get_cliente_por_cpf(cpf)
        if pessoa is None:
            print("Cliente não encontrado!")
            return
    menu = '''
##### MENU DE EDIÇÃO ######
1 - Editar nome
2 - Editar CPF
3 - Editar telefone
4 - Editar email
5 - Editar RG
6 - Editar endereço
7 - Sair
        '''
    print(menu)
    opcao = int(input("Digite o número correspondente a opção: "))
    match opcao:
        case 1:
            while True:
                nome = input("Digite o novo nome: ")
                if len(nome) > 0:
                    pessoa.set_nome(nome)
                    break
        case 2:
            while True:
                cpf = input("Digite o novo CPF: ")
                if len(cpf) == 11:
                    pessoa.set_cpf(cpf)
                    break
        case 3:
            while True:
                telefone = input("Digite o novo telefone: ")
                if len(telefone) == 11:
                    pessoa.set_telefone(telefone)
                    break
        case 4:
            while True:
                email = input("Digite o novo email: ")
                if len(email) > 0:
                    pessoa.set_email(email)
                    break
        case 5:
            while True:
                rg = input("Digite o novo RG: ")
                if len(rg) > 0:
                    pessoa.set_rg(rg)
                    break
        case 6:
            while True:
                endereco = input("Digite o novo endereço: ")
                if len(endereco) > 0:
                    pessoa.set_endereco(endereco)
                    break
        case 7:
            return
        case _:
            print("Opção inválida. Tente novamente.")
    edicaoPessoa()
    

def cadastroProduto():
    while True:
        nome = input("Digite o nome: ")
        if len(nome) > 0:
            break
    while True:
        marca = input("Digite a marca: ")
        if len(marca) > 0:
            break
    while True:
        modelo = input("Digite o modelo: ")
        if len(modelo) > 0:
            break
    while True:
        cor = input("Digite a cor: ")
        if len(cor) > 0:
            break
    while True:
        preco = float(input("Digite o preço: "))
        if preco > 0:
            break
    while True:
        quantidade = int(input("Digite a quantidade: "))
        if quantidade > 0:
            break
    produto1 = Produto(nome, marca, modelo, cor, preco, quantidade)
    if (Estoque.adicionar_produto(produto1)):
        Estoque.adicionar_produto(produto1)
        print("Produto cadastrado com sucesso!")
        print(produto1)
    else:
        print("Erro. Produto não cadastrado!")


def edicaoProduto():
    print("Digite o ID do produto que deseja editar: ")
    id = input()
    produto = Estoque.get_produto_por_id(id)
    if produto is None:
        print("Produto não encontrado!")
        return
    menu = '''
##### MENU DE EDIÇÃO ######
1 - Editar nome
2 - Editar marca
3 - Editar modelo
4 - Editar cor
5 - Editar preço
6 - Editar quantidade
7 - Sair
        '''
    print(menu)
    opcao = int(input("Digite o número correspondente a opção: "))
    match opcao:
        case 1:
            while True:
                nome = input("Digite o novo nome: ")
                if len(nome) > 0:
                    produto.set_nome(nome)
                    break
        case 2:
            while True:
                marca = input("Digite a nova marca: ")
                if len(marca) > 0:
                    produto.set_marca(marca)
                    break
        case 3:
            while True:
                modelo = input("Digite o novo modelo: ")
                if len(modelo) > 0:
                    produto.set_modelo(modelo)
                    break
        case 4:
            while True:
                cor = input("Digite a nova cor: ")
                if len(cor) > 0:
                    produto.set_cor(cor)
                    break
        case 5:
            while True:
                preco = float(input("Digite o novo preço: "))
                if preco > 0:
                    produto.set_preco(preco)
                    break
        case 6:
            while True:
                quantidade = int(input("Digite a nova quantidade: "))
                if quantidade > 0:
                    produto.set_quantidade(quantidade)
                    break
        case 7:
            return
        case _:
            print("Opção inválida. Tente novamente.")
    edicaoProduto()

def carrinho_compras():
    if isCadastrado == False:
        print("Você não está cadastrado!")
        return
    else:
        carrinho_compras = []
        menu = '''
##### MENU CARRINHO ######
1 - Ver todos os produtos da loja para adicionar no carrinho
2 - Pesquisar produto para adicionar no carrinho
3 - Remover produto do carrinho
4 - Ver produtos no carrinho
5 - Sair do menu
            '''
        print(menu)
        opcao = input("Digite o número correspondente a opção: ")
        match opcao:
            case 1:
                print(Estoque.get_lista_produtos())
                add_carrinho()
            case 2:
                nome = input("\nDigite o nome do produto: ")
                produtos = Estoque.consultar_produtos_por_nome(nome)
                if produtos is None:
                    print("Produto não encontrado!")
                    return
                print("Produtos encontrados:")
                for produto in produtos:
                    print(produto)
                add_carrinho()
            case 3:
                id = input("Digite o ID do produto que deseja remover: ")
                for produto in carrinho_compras:
                    if produto.get_id() == id:
                        carrinho_compras.remove(i)
                        print("Produto removido do carrinho!")
                print("Produto não encontrado no carrinho!")
            case 4:
                if len(carrinho_compras) == 0:
                    print("Carrinho vazio!")
                    return
                print("Produtos no carrinho:")
                for i in carrinho_compras:
                    print(i)
            case 5:
                return
            case _:
                print("Opção inválida")
        carrinho_compras()


def add_carrinho():
        id = input("Digite o ID do produto que você deseja comprar: ")
        produto = Estoque.consultar_produto_por_id(id)
        while True:
            quantidade = int(input("Digite a quantidade: "))
            if quantidade <= produto.get_quantidade():
                break
        carrinho = {
            "produto": produto,
            "quantidade": quantidade
        }
        carrinho_compras.append(carrinho)
        print("Produto adicionado ao carrinho!")
        # condicao = input("Deseja adicionar mais algum produto? (s/n): ")
        # if(condicao == "s"):
        #         carrinho_compras()
        # else:
        #     for i in carrinho_compras:
        #         print(i)
        #     condicao = "n"
        return carrinho_compras


def realizar_compra(carrinho_compras):
    if isCadastrado == False:
        print("Você não está cadastrado!")
        return
    if len(carrinho_compras) == 0:
        print("Carrinho vazio!")
        return
    print("Produtos no carrinho:")
    for i in carrinho_compras:
        print(i)
    menu = '''
##### MENU DE PAGAMENTO ######
1 - Cartão de crédito
2 - Cartão de débito
3 - Pix
        '''
    print(menu)
    opcao = int(input("Digite o número correspondente a opção: "))
    match opcao:
        case 1:
            parcelas = int(input("Parcelas:"))
            modo_pagamento = 1
            print("Pagamento realizado com cartão de crédito!")
        case 2:
            modo_pagamento = 2
            print("Pagamento realizado com cartão de débito!")
        case 3:
            modo_pagamento = 3
            print("Pagamento realizado com dinheiro!")
        case _:
            print("Opção inválida. Tente novamente.")
            realizar_compra(carrinho_compras)
    for produto in carrinho_compras:
        Loja.realizar_venda(produto)
    print(Loja.gerar_recibo(cliente, carrinho_compras, modo_pagamento))


login()
