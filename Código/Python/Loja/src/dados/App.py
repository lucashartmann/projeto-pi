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

def menu():
    opcao = 0 
    while opcao < 1 or opcao > 11:
        print()
        print('##### MENU ######')
        print('1 -- Cadastrar Cliente/Fornecedor/Funcionario')
        print('2 -- Cadastrar Produto')
        print('3 -- Editar Cliente/Fornecedor/Funcionario')
        print('4 -- Editar Produto')
        print('5 -- Estoque')
        print('6 -- Dados')
        print('7 -- Sair do menu')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                cadastroPessoa()
            case 2:
                cadastroProduto()
            case 3:
                edicaoPessoa()
            case 4:
                edicaoProduto()
            case 5:
                menuEstoque()
            case 6:
                menuDados()
            case 7:
                return
            case _:
                print('Opção errada, tente novamente')
        menu()

def menuEstoque():
    opcao = 0
    while opcao < 1 or opcao > 11:
        print()
        print('##### MENU ######')
        print('1 -- Ver produto por nome')
        print('2 -- Ver produtos por fornecedor')
        print('3 -- Ver produtos por categoria')
        print('4 -- Sair do menu')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                estoque.verProdutoPorNome()
            case 2:
                estoque.verProdutoPorFornecedor()
            case 3:
                estoque.verProdutoPorCategoria()
            case 4:
                return
            case _:
                print('Opção errada, tente novamente')
        
def menuDados():
    opcao = 0 
    while opcao < 1 or opcao > 7:
        print()
        print('##### MENU DADOS ######')
        print('1 -- Ver quantidade de clientes')
        print('2 -- Ver quantidade de produtos')
        print('3 -- Ver quantidade de fornecedores')
        print('4 -- Ver quantidade de funcionarios')
        print('5 -- Ver quantidade de produtos por fornecedor')
        print('6 -- Ver quantidade de produtos por categoria')
        print('7 -- Sair do menu')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                print("Qauantidade de clientes: ", loja.get_quantidade_clientes())
            case 2:
                print("Quantidade de produtos: ", estoque.get_quantidade())
            case 3:
                print("Quantidade de fornecedores: ", loja.get_quantidade_fornecedores())
            case 4:
                print("Quantidade de funcionarios: ", loja.get_quantidade_funcionarios())
            case 5:
                loja.get_quantidade_produtos_por_fornecedor()
            case 6:
                estoque.get_quantidade_produtos_por_categoria()
            case 7:
                return
            case _:
                print('Opção errada, tente novamente')
        
def cadastroPessoa():
    opcao = 0
    while opcao < 1 or opcao > 3:
        print()
        print('##### MENU PESSOA ######')
        print('1 -- Cliente')
        print('2 -- Fornecedor')
        print('3 -- Funcionario')
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
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
        opcao = 0
        while opcao < 1 or opcao > 3:
            print()
            print('##### MENU PESSOA ######')
            print('1 -- Cliente')
            print('2 -- Fornecedor')
            print('3 -- Funcionario')
            opcao = int(input('Digite o número correspondente a opção: '))
            print()
            match opcao:
                case 1:
                    cliente1.editar()
                case 2:
                    fornecedor1.editar()
                case 3:
                    funcionario1.editar()
                case _:
                    print('Opção errada, tente novamente')
            
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
    pass

menu()