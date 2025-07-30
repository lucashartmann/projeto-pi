from model import Venda, Cliente, Fornecedor, Funcionario, Loja, Produto

usuario = 0
cliente_atual = None
loja = Loja("GameStart", "00000000000")


def init():

    cliente1 = Cliente("MARCOS", "11111111111", "11111111111",
                       "11111111111", "RUA 1", "MARCOS@GMAIL.COM")
    cliente2 = Cliente("PEDRO", "22222222222", "22222222222",
                       "22222222222", "RUA 2", "PEDRO@GMAIL.COM")
    cliente3 = Cliente("JULIA", "33333333333", "33333333333",
                       "33333333333", "RUA 3", "JULIA@GMAIL.COM")
    cliente4 = Cliente("JOÃO", "44444444444", "44444444444",
                       "44444444444", "RUA 4", "JOAO@GMAIL.COM")
    cliente5 = Cliente("ANDRESSA", "55555555555", "55555555555",
                       "55555555555", "RUA 5", "ANDRESSA@GMAIL.COM")
    cliente6 = Cliente("MARIA", "66666666666", "66666666666",
                       "66666666666", "RUA 6", "MARIA@GMAIL.COM")
    cliente7 = Cliente("ANA", "77777777777", "77777777777",
                       "77777777777", "RUA 7", "ANA@GMAIL.COM")
    cliente8 = Cliente("JOANA", "88888888888", "88888888888",
                       "88888888888", "RUA 8", "JOANA@GMAIL.COM")
    cliente9 = Cliente("GABRIELA", "99999999999", "99999999999",
                       "99999999999", "RUA 9", "GABRIELA@GMAIL.COM")
    cliente10 = Cliente("FERNANDA", "10101010101", "10101010101",
                        "10101010101", "RUA 10", "FERNANDA@GMAIL.COM")

    loja.cadastrar(cliente1)
    loja.cadastrar(cliente2)
    loja.cadastrar(cliente3)
    loja.cadastrar(cliente4)
    loja.cadastrar(cliente5)
    loja.cadastrar(cliente6)
    loja.cadastrar(cliente7)
    loja.cadastrar(cliente8)
    loja.cadastrar(cliente9)
    loja.cadastrar(cliente10)

    produto1 = Produto("PLAYSTATION 5", "SONY", "SLIM", "PRETO", 3000.00, 10)
    produto2 = Produto("XBOX SERIES X", "MICROSOFT",
                       "SLIM", "PRETO", 4000.00, 10)
    produto3 = Produto("NINTENDO SWITCH", "NINTENDO",
                       "SLIM", "PRETO", 3000.00, 10)
    produto4 = Produto("GEFORCE RTX 3080 TI", "NVIDIA",
                       "TI", "BRANCO", 2000.00, 3)
    produto5 = Produto("RX 6900 XT", "AMD", "60 SERIES", "BRANCO", 1000.00, 3)
    produto6 = Produto("GEFORCE RTX 3090", "NVIDIA",
                       "30 SERIES", "BRANCO", 1000.00, 3)
    produto7 = Produto("DUALSHOCK 4", "SONY", "SLIM", "PRETO", 200.00, 10)
    produto9 = Produto("VOLANTE GAMER", "LOGITECH", "G29", "PRETO", 500.00, 5)
    produto10 = Produto("MOUSE GAMER", "LOGITECH", "G502", "PRETO", 100.00, 10)
    produto11 = Produto("PLAYSTATION 5", "SONY", "PRO", "BRANCO", 6000.00, 30)

    loja.get_estoque().adicionar_produto(produto1)
    loja.get_estoque().adicionar_produto(produto2)
    loja.get_estoque().adicionar_produto(produto3)
    loja.get_estoque().adicionar_produto(produto4)
    loja.get_estoque().adicionar_produto(produto5)
    loja.get_estoque().adicionar_produto(produto6)
    loja.get_estoque().adicionar_produto(produto7)
    loja.get_estoque().adicionar_produto(produto9)
    loja.get_estoque().adicionar_produto(produto10)
    loja.get_estoque().adicionar_produto(produto11)


def login():
    init()
    while True:
        menu = '''
## Login ## 
1. Cliente 
2. Admin 
3. Encerrar programa
        '''
        print(menu)
        usuario = int(input("Digite o número correspondente ao usuário: "))
        match usuario:
            case 1:
                cliente(usuario, cliente_atual)
            case 2:
                admin(usuario)
            case 3:
                break
            case _:
                print("Erro. Opção inválida. Tente novamente.")


def cliente(usuario, cliente_atual):
    while True:
        menu = '''
## Menu Cliente ##
1. Cadastrar
2. Editar cadastro
3. Ver cadastro
4. Carrinho de compras
5. Realizar compra
6. Ver últimas compras
7. Sair do menu
        '''
        print(menu)
        opcao = int(input('Digite o número correspondente a opção: '))
        print()
        match opcao:
            case 1:
                cliente_atual = cadastroPessoa(usuario)
            case 2:
                edicaoPessoa(usuario, cliente_atual)
            case 3:
                print(cliente_atual)
            case 4:
                carrinho(cliente_atual)
            case 5:
                realizar_compra(cliente_atual)
            case 7:
                break
            case _:
                print('Erro. Opção errada, tente novamente')


def admin(usuario):
    while True:
        menu = '''
## Menu Admin ##
1. Cadastrar Produto
2. Editar Produto
3. Cadastrar Pessoa
4. Editar Pessoa
5. Ver produto por nome
6. Ver produtos por marca
7. Ver produtos por categoria
8. Ver quantidade de tudo
9. Ver quantidade de produtos por marca
10. Ver quantidade de produtos por categoria
11. Ver quantidade de produtos por modelo
12. Sair do menu
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
                cadastroPessoa(usuario)
            case 4:
                edicaoPessoa(usuario, cliente_atual)
            case 5 | 6 | 7:
                procurarProduto(opcao)
            case 8:
                print("Quantidade de Produtos: ", loja.get_estoque().get_quantidade_produtos(), "\nQuantidade de clientes: ", loja.get_quantidade_clientes(), "\nQuantidade de funcionários: ",
                      loja.get_quantidade_funcionarios(), "\nQuantidade de fornecedores: ", loja.get_quantidade_fornecedores())
            case 9 | 10 | 11:
                verQuantidadeProduto(opcao)
            case 12:
                break
            case _:
                print('Erro. Opção errada, tente novamente')


def verQuantidadeProduto(opcao):
    campos = {
        9: ("marca", loja.get_estoque().get_quantidade_produto_por_marca),
        10: ("categoria", loja.get_estoque().get_quantidade_produto_por_categoria),
        11: ("modelo", loja.get_estoque().get_quantidade_produto_por_modelo)
    }

    nome_campo, func = campos[opcao]
    valor = input(f"Digite a {nome_campo} do produto: ").upper()
    quantidade = func(valor)

    if quantidade is None:
        print("Erro. Produto não encontrado!")
        return

    print(f"Quantidade de produtos da {nome_campo} {valor}: {quantidade}")


def procurarProduto(opcao):
    campos = {
        5: ("nome", loja.get_estoque().get_produtos_por_nome),
        6: ("marca", loja.get_estoque().get_produtos_por_marca),
        7: ("categoria", loja.get_estoque().get_produtos_por_categoria)
    }

    nome_campo, func = campos[opcao]
    valor = input(f"Digite a {nome_campo} do produto: ").upper()
    produtos = func(valor)

    if not produtos:
        print("Erro. Produto não encontrado!")
        return

    print("Produtos encontrados:")
    for produto in produtos:
        print(produto)


def validar(string):
    while True:
        campo = input(f"Digite {string}: ").upper()
        if len(campo) > 0:
            if "CPF" in string:
                if len(campo) == 11:
                    cpf_ja_cadastrado = loja.is_cpf_cadastrado(campo)
                    if not cpf_ja_cadastrado:
                        return campo
                    print("Erro. CPF já cadastrado!")
            elif "RG" in string:
                if len(campo) == 9:
                    rg_ja_cadastrado = loja.is_rg_cadastrado(campo)
                    if not rg_ja_cadastrado:
                        return campo
                    print("Erro. RG já cadastrado!")
            elif "telefone" in string:
                if len(campo) == 11:
                    telefone_ja_cadastrado = loja.is_telefone_cadastrado(campo)
                    if not telefone_ja_cadastrado:
                        return campo
                    print("Erro. Telefone já cadastrado!")
            else:
                return campo
        print(f"Erro. {campo} inválido!")


def cadastroPessoa(usuario):
    nome = validar("o seu nome")
    cpf = validar("o seu CPF")
    telefone = validar("o seu telefone")
    email = validar("o seu email")
    rg = validar("a sua RG")
    endereco = validar("o seu endereço")
    if usuario == 1:
        cliente_atual = Cliente(nome, cpf, rg, telefone, endereco, email)
        if loja.cadastrar(cliente_atual):
            loja.cadastrar(cliente_atual)
            cliente_atual.set_is_cadastrado(True)
            print("Cliente cadastrado com sucesso!")
            print(cliente_atual)
            return cliente_atual
        else:
            print("Erro. Cliente não cadastrado!")
    else:
        print("1 - Funcionário")
        print("2 - Fornecedor")
        tipo = int(input("Digite o tipo de pessoa: "))
        if tipo == 1:
            funcionario = Funcionario(nome, cpf, rg, telefone, endereco, email)
            if loja.cadastrar(funcionario):
                loja.cadastrar(funcionario)
                print("Funcionário cadastrado com sucesso!")
            else:
                print("Erro. Funcionário não cadastrado!")
        else:
            fornecedor = Fornecedor(nome, cpf, rg, telefone, endereco, email)
            if loja.cadastrar(fornecedor):
                loja.cadastrar(fornecedor)
                print("Fornecedor cadastrado com sucesso!")
            else:
                print("Erro. Fornecedor não cadastrado!")


def edicaoPessoa(usuario, cliente_atual):
    if usuario == 1:
        if not cliente_atual.get_is_cadastrado():
            print("Erro. Você não está cadastrado!")
            return
        pessoa_atual = cliente_atual
    else:
        cpf = input("Digite o CPF do cliente que deseja editar: ")
        pessoa_atual = loja.get_cliente_por_cpf(cpf)
        if pessoa_atual is None:
            print("Erro. Cliente não encontrado!")
            return
    while True:
        menu = '''
## Menu de Edição ##
1. Editar nome
2. Editar CPF
3. Editar telefone
4. Editar email
5. Editar RG
6. Editar endereço
7. Sair
        '''
        print(menu)
        opcao = int(input("Digite o número correspondente à opção: "))
        match opcao:
            case 1:
                pessoa_atual.editar_campo("nome", pessoa_atual.set_nome)
            case 2:
                pessoa_atual.editar_campo("CPF", pessoa_atual.set_cpf)
            case 3:
                pessoa_atual.editar_campo(
                    "telefone", pessoa_atual.set_telefone)
            case 4:
                pessoa_atual.editar_campo("email", pessoa_atual.set_email)
            case 5:
                pessoa_atual.editar_campo("RG", pessoa_atual.set_rg)
            case 6:
                pessoa_atual.editar_campo(
                    "endereço", pessoa_atual.set_endereco)
            case 7:
                print("Saindo da edição...")
                break
            case _:
                print("Erro. Opção inválida. Tente novamente.")
        print(pessoa_atual)


def cadastroProduto():
    nome = validar("o nome do produto")
    marca = validar("a marca do produto")
    modelo = validar("o modelo do produto")
    cor = validar("a cor do produto")
    preco = float(validar("o preço do produto"))
    quantidade = int(validar("a quantidade do produto"))
    novo_produto = Produto(nome, marca, modelo, cor, preco, quantidade)
    cadastrado = loja.get_estoque().adicionar_produto(novo_produto)
    if cadastrado:
        print("\nProduto cadastrado com sucesso!")
        print(novo_produto)
    else:
        print("\nErro. Não foi possivel cadastrar o produto")


def edicaoProduto():
    id = int(input("Digite o ID do produto que deseja editar: "))
    produto = loja.get_estoque().get_produto_por_id(id)
    if produto is None:
        print("Erro. Produto não encontrado!")
        return
    while True:
        menu = '''
## Menu de Edição ## 
1. Editar nome
2. Editar marca
3. Editar modelo
4. Editar cor
5. Editar preço
6. Editar quantidade
7. Sair
        '''
        print(menu)
        opcao = int(input("Digite o número correspondente a opção: "))
        match opcao:
            case 1:
                produto.editar_campo("nome", produto.set_nome)
            case 2:
                produto.editar_campo("marca", produto.set_marca)
            case 3:
                produto.editar_campo(
                    "modelo", produto.set_modelo)
            case 4:
                produto.editar_campo("cor", produto.set_cor)
            case 5:
                produto.editar_campo("preco", produto.set_preco)
            case 6:
                produto.editar_campo(
                    "quantidade", produto.set_quantidade)
            case 7:
                break
            case _:
                print("Erro. Opção inválida. Tente novamente.")
        print(produto)


def realizar_compra(cliente_atual):
    if not cliente_atual.get_is_cadastrado():
        print("Erro. Você não está cadastrado!")
        return
    carrinho = cliente_atual.get_carrinho()
    if carrinho.esta_vazio():
        print("Erro. Carrinho vazio!")
        return
    print("Produtos no carrinho:")
    for produto in carrinho.listar_produtos():
        print(produto)
    menu = '''
## Menu de Pagamento ##
1. Cartão de crédito
2. Cartão de débito
3. Pix
    '''
    print(menu)
    opcao = int(input("Digite o número correspondente à opção: "))
    match opcao:
        case 1:
            parcelas = int(input("Parcelas: "))
        case 2 | 3:
            parcelas = 1
        case _:
            print("Erro. Opção inválida.")
            return
    modo_pagamento = opcao
    venda = Venda(cliente_atual, carrinho,
                  modo_pagamento)
    venda.set_parcelas(parcelas)
    venda.aplicar_venda(loja)
    print(venda.gerar_recibo(loja))
    carrinho.limpar()
    quit()


def carrinho(cliente_atual):
    if not cliente_atual.get_is_cadastrado():
        print("Você não está cadastrado!")
        return
    carrinho = cliente_atual.get_carrinho()
    while True:
        menu = '''
### Menu Carrinho ###
1. Ver todos os produtos da loja para adicionar no carrinho
2. Pesquisar produto para adicionar no carrinho
3. Remover produto do carrinho
4. Ver produtos no carrinho
5. Sair do menu
        '''
        print(menu)
        opcao = int(input("Digite o número correspondente à opção: "))
        match opcao:
            case 1:
                produtos_estoque = loja.get_estoque().get_lista_produtos()
                for produto in produtos_estoque:
                    print(produto)
            case 2:
                nome = input("Nome do produto: ")
                nome = nome.upper()
                produtos = loja.get_estoque().get_produtos_por_nome(nome)
                if not produtos:
                    print(f"Erro. Nenhum produto {nome} no estoque")
                else:
                    for p in produtos:
                        print(p)
            case 3:
                id = int(input("ID do produto a remover: "))
                removido = carrinho.remover_produto_por_id(id)
                if removido:
                    print("Removido com sucesso.")
                else:
                    print("Erro. Produto não encontrado.")
            case 4:
                itens = carrinho.listar_produtos()
                if not itens:
                    print("Erro. Carrinho vazio.")
                else:
                    print("Produtos no carrinho:")
                    for produto, quantidade in itens.items():
                        print(produto, "Quantidade:", quantidade)
            case 5:
                return carrinho
            case _:
                print("Opção inválida.")
        if opcao == 1 or opcao == 2:
            while True:
                id = int(input("ID do produto (ou 0 para sair): "))
                if id == 0:
                    break
                produto = loja.get_estoque().get_produto_por_id(id)
                if produto:
                    qtd = int(input("Quantidade: "))
                    adicionar = carrinho.adicionar_produto(produto, qtd)
                    if adicionar:
                        print("Produto adicionado!")
                        print(produto)
                    else:
                        print("Erro. Quantidade inválida!")
                else:
                    print("Erro. Produto não encontrado.")


if __name__ == '__main__':
    login()