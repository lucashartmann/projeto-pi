import Cliente
import Fornecedor
import Funcionario
import Produto
import Estoque
import Loja

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

def menuCliente():
    opcao = 0 
    carrinho_compras = []
    # Fazer cadastrar e editar em um método só?
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
        3 -- Ver produto por nome
        4 -- Ver produtos por marca
        5 -- Ver produtos por categoria
        6 -- Ver quantidade de tudo
        7 -- Ver quantidade de produtos por marca
        8 -- Ver quantidade de produtos por categoria
        9 -- Sair do menu
        '''
        print(menu)
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                cadastroProduto()
            case 2:
                edicaoProduto()
            case 3, 4, 5:
                procurarProduto(opcao)
            case 6:
                print("Quantidade de clientes: ", Loja.get_quantidade_clientes(), "\nQuantidade de funcionários: ", Loja.get_quantidade_funcionarios(), "\nQuantidade de fornecedores: ", Loja.get_quantidade_fornecedores())
            case 7, 8:
                verQuantidadeProduto(opcao)
            case 9:
                return
            case _:
                print('Opção errada, tente novamente')
        menuAdmin()

def verQuantidadeProduto(opcao):
    # Ver quantidade por modelo
    if opcao == 7:
        marca = input("Digite a marca do produto: ")
        quantidade = Estoque.get_quantidade_produtos_por_marca(marca)
        if quantidade is None:
            print("Produto não encontrado!")
            return
        print(f"Quantidade de produtos da marca {marca}: {quantidade}")
    elif opcao == 8:
        categoria = input("Digite a categoria do produto: ")
        quantidade = Estoque.get_quantidade_produtos_por_categoria(categoria)
        if quantidade is None:
            print("Produto não encontrado!")
            return
        print(f"Quantidade de produtos da categoria {categoria}: {quantidade}")

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
    Loja.cadastrar(nome, cpf, rg, telefone, endereco, email)
    
def edicaoPessoa():
        # Implementar
        pass
            
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
    if(Estoque.adicionar_produto(produto1)):
        Estoque.adicionar_produto(produto1)
        print("Produto cadastrado com sucesso!")
        print(produto1)
    else:
        print("Erro. Produto não cadastrado!")
            
def edicaoProduto():
    # Implementar
    pass

# Implementar Remover produto do carrinho
def carrinho_compras():

    cpf = input("Digite o CPF do cliente: ") # ?
    condicao = "s"
    if(Loja.verificar_cliente(cpf)):
        while condicao == "s":

            menu = '''
            1 - Ver todos os produtos
            2 - Pesquisar produto
            '''
            print(menu)
            opcao = input("Digite o número correspondente a opção: ")

            if(opcao == "1"):
                print(Estoque.get_lista_produtos())
                id = input("Digite o ID do produto que você deseja comprar: ")
            elif(opcao == "2"):
                nome = input("Digite o nome do produto: ")
                produtos = Estoque.consultar_produtos_por_nome(nome)
                if produtos is None:
                    print("Produto não encontrado!")
                    return
                print("Produtos encontrados:")
                for produto in produtos:
                    print(produto)
                id = input("Digite o ID do produto que você deseja comprar: ")
                while True:
                    quantidade = int(input("Digite a quantidade: "))
                    if quantidade <= produto.get_quantidade():
                        break
            else:
                print("Opção inválida")
                carrinho_compras()  

            produto = Estoque.consultar_produto_por_id(id)

            carrinho = {
                "produto": produto,
                "quantidade": quantidade
            }
            carrinho_compras = []
            carrinho_compras.append(carrinho)
            print("Produto adicionado ao carrinho!")

            condicao = input("Deseja adicionar mais algum produto? (s/n): ")
            if(condicao == "s"):
                    carrinho_compras()
            else:
                for i in carrinho_compras:
                    print(i)
                condicao = "n"
                return carrinho_compras    
              
    else:
        print("Cliente não encontrado!")
        cadastroPessoa()

def realizar_compra(carrinho_compras):
    for produto in carrinho_compras:
        Loja.realizar_venda(produto)

login()