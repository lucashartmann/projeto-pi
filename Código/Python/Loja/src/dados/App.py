from Cliente import Cliente
from Fornecedor import Fornecedor
from Funcionario import Funcionario
from Produto import Produto
from Estoque import Estoque
from Loja import Loja

loja = Loja("Loja do João", "123456789")
estoque = Estoque()
cliente1 = Cliente("João", "00000000000", "00000000000", "00000000000", "Bento Gonçalves 102", "joao@gmail.com")
fornecedor1 = Fornecedor("Pedro", "11111111111", "11111111111", "11111111111", "Bento Gonçalves 10", "pedro@gmail.com")
funcionario1 = Funcionario("Fernando", "22222222222", "2222222222", "22222222222", "Bento Gonçalves 100", "fernando@gmail.com")
produto1 = Produto("Placa de video", "Branca", 1000.00, "Nvidia", "RTX 4060", 100)

# Implementar lógica de segurança para ver se é o admin

def login():
    print("Escolha um usuário: ")
    print("1 - Cliente")
    print("2 - Admin")
    usuario = int(input("Digite o número correspondente ao usuário: "))
    if usuario == 1:
        menuCliente()
    elif usuario == 2:
        menuAdmin()
    else:
        print("Usuário não encontrado")

def menuCliente():
    opcao = 0 
    carrinho_compras = []
    while opcao < 1 or opcao > 3:
        print()
        print('##### MENU CLIENTE ######')
        print('1 - Adicionar produtos no Carrinho')
        print('2 - Realizar compra')
        print('3 -- Sair do menu')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                carrinho_compras = carrinho_compras()
            case 2:
                realizar_compra(carrinho_compras)
            case 3:
                return
            case _:
                print('Opção errada, tente novamente')
        menuCliente()

def menuAdmin():
    opcao = 0 
    while opcao < 1 or opcao > 5:
        print()
        print('##### MENU ######')
        print('1 -- Cadastrar pessoa')
        print('2 -- Editar pessoa')
        print('3 -- Estoque')
        print('4 -- Dados')
        print('5 -- Sair do menu')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                cadastroPessoa()
            case 2:
                edicaoPessoa()
            case 3:
                menuEstoque()
            case 4:
                menuDados()
            case 5:
                return
            case _:
                print('Opção errada, tente novamente')
        menuAdmin()

def menuEstoque():
    opcao = 0
    while opcao < 1 or opcao > 6:
        print()
        print('##### MENU ######')
        print('1 -- Cadastrar Produto')
        print('2 -- Editar Produto')
        print('3 -- Ver produto por nome')
        print('4 -- Ver produtos por marca')
        print('5 -- Ver produtos por categoria')
        print('6 -- Sair do menu')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                cadastroProduto()
            case 2:
                edicaoProduto()
            case 3:
                estoque.ver_produto_por_nome()
            case 4:
                estoque.ver_produto_por_marca()
            case 5:
                estoque.ver_produto_por_categoria()
            case 6:
                return
            case _:
                print('Opção errada, tente novamente')
        
def menuDados():
    opcao = 0 
    while opcao < 1 or opcao > 4:
        print()
        print('##### MENU DADOS ######')
        print('1 -- Ver quantidade')
        print('2 -- Ver quantidade de produtos por marca')
        print('3 -- Ver quantidade de produtos por categoria')
        print('4 -- Sair do menu')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                print("Quantidade de clientes: ", loja.get_quantidade_clientes(), "\nQuantidade de funcionários: ", loja.get_quantidade_funcionarios(), "\nQuantidade de fornecedores: ", loja.get_quantidade_fornecedores())
            case 2:
                loja.get_quantidade_produtos_por_marca()
            case 3:
                estoque.get_quantidade_produtos_por_categoria()
            case 4:
                return
            case _:
                print('Opção errada, tente novamente')

def menuPessoa():
    opcao = 0
    while opcao < 1 or opcao > 3:
        print('##### MENU PESSOA ######')
        print('1 -- Cliente')
        print('2 -- Fornecedor')
        print('3 -- Funcionario')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        return opcao
        
def cadastroPessoa():
        opcao = menuPessoa()
        nome = input("Digite o nome: ")
        cpf = input("Digite o CPF: ")
        telefone = input("Digite o telefone: ")
        email = input("Digite o email: ")
        rg = input("Digite a RG: ")
        idade = int(input("Digite a idade: "))
        endereco = input("Digite o endereço: ")
        email = input("Digite o email: ")
        data_nascimento = input("Digite a data de nascimento: ")
        if(nome == "" or cpf == "" or telefone == "" or email == "" or rg == "" or idade == "" or endereco == "" or email == "" or data_nascimento == ""):
            print("Preencha todos os campos")
            cadastroPessoa()
        elif(len(cpf) != 11 or len(rg) != 7 or len(idade) != 2 or len(data_nascimento) != 8 or len(telefone) != 11):
            print("Preencha todos os campos")
            cadastroPessoa()
        match opcao:
            case 1:
                loja.cadastrar_cliente(nome, cpf, telefone, email, rg, idade, endereco, email, data_nascimento)
            case 2:
                loja.cadastrar_fornecedor(nome, cpf, telefone, email, rg, idade, endereco, email, data_nascimento)
            case 3:
                loja.cadastrar_funcionario(nome, cpf, telefone, email, rg, idade, endereco, email, data_nascimento)
            case _:
                print('Opção errada, tente novamente')
        
def edicaoPessoa():
        opcao = menuPessoa()
            
def cadastroProduto():
    nome = input("Digite o nome: ")
    marca = input("Digite a marca: ")
    modelo = input("Digite o modelo: ")
    cor = input("Digite a cor: ")
    preco = float(input("Digite o preço: "))  
    quantidade = int(input("Digite a quantidade: "))
    if(nome == "" or marca == "" or modelo == "" or preco == "" or quantidade == ""):
        print("Preencha todos os campos")
        cadastroProduto()
    produto1 = Produto(nome, marca, modelo, cor, preco, quantidade)
    if(estoque.adicionar_produto(produto1)):
        estoque.adicionar_produto(produto1)
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
    if(loja.verificar_cliente(cpf)):
        while condicao == "s":
            menu = '''
            1- Ver todos os produtos
            2- Pesquisar produto
            '''
            print(menu)
            opcao = input("Digite o número correspondente a opção: ")
            if(opcao == "1"):
                print(estoque.get_lista_produtos())
                id = input("Digite o ID do produto que você deseja comprar: ")
            elif(opcao == "2"):
                produto = input("Digite o nome do produto: ")
                quantidade = int(input("Digite a quantidade: "))
            else:
                print("Opção inválida")
                carrinho_compras()  
            if(estoque.verificar_produto(produto)):
                if(estoque.verificar_quantidade(produto, quantidade)):
                    carrinho = {
                        "produto": produto,
                        "quantidade": quantidade
                    }
                    carrinho_compras = []
                    carrinho_compras.append(carrinho)
                    condicao = input("Deseja comprar mais algum produto? (s/n): ")
                    if(condicao == "s"):
                            carrinho_compras()
                    else:
                        for i in carrinho_compras:
                            print(i)
                        condicao = "n"
                        return carrinho_compras
                else:
                    print("Quantidade insuficiente!")
            else:
                print("Produto não encontrado!")         
    else:
        print("Cliente não encontrado!")
        cadastroPessoa()

def realizar_compra(carrinho_compras):
    for produto in carrinho_compras:
        loja.realizar_venda(produto)
  

login()