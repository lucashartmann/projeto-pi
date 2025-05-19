from dados.Venda import Venda
from dados.Cliente import Cliente
from dados.Fornecedor import Fornecedor
from dados.Funcionario import Funcionario
from dados.Produto import Produto
from dados.Loja import Loja

usuario = 0
cliente_atual = None
loja = Loja("GameStart", "00000000000")


def init():

    cliente1 = Cliente("Marcos", "00000000000", "00000000000",
                       "00000000000", "Rua 1", "marcos@gmail.com")
    cliente2 = Cliente("Pedro", "00000000000", "00000000000",
                       "00000000000", "Rua 2", "pedro@gmail.com")
    cliente3 = Cliente("Julia", "00000000000", "00000000000",
                       "00000000000", "Rua 3", "julia@gmail.com")
    cliente4 = Cliente("João", "00000000000", "00000000000",
                       "00000000000", "Rua 4", "joao@gmail.com")
    cliente5 = Cliente("Andressa", "00000000000", "00000000000",
                       "00000000000", "Rua 5", "andressa@gmail.com")
    cliente6 = Cliente("Maria", "00000000000", "00000000000",
                       "00000000000", "Rua 6", "maria@gmail.com")
    cliente7 = Cliente("Ana", "00000000000", "00000000000",
                       "00000000000", "Rua 7", "ana@gmail.com")
    cliente8 = Cliente("Joana", "00000000000", "00000000000",
                       "00000000000", "Rua 8", "joana@gmail.com")
    cliente9 = Cliente("Gabriela", "00000000000", "00000000000",
                       "00000000000", "Rua 9", "gabriela@gmail.com")
    cliente10 = Cliente("Fernanda", "00000000000", "00000000000",
                        "00000000000", "Rua 10", "fernanda@gmail.com")

    produto1 = Produto("Playstation 5", "Sony", "Slim", "Preto", 5000.00, 10)
    produto2 = Produto("Xbox Series X", "Microsoft",
                       "Slim", "Preto", 4000.00, 10)
    produto3 = Produto("Nintendo Switch", "Nintendo",
                       "Slim", "Preto", 3000.00, 10)
    produto4 = Produto("GeForce RTX 3080 ti", "Nvidia",
                       "ti", "Branco", 2000.00, 3)
    produto5 = Produto("RX 6900 XT", "AMD", "60 Series", "Branco", 1000.00, 3)
    produto6 = Produto("GeForce RTX 3090", "Nvidia",
                       "30 Series", "Branco", 1000.00, 3)
    produto7 = Produto("Dualshock 4", "Sony", "Slim", "Preto", 200.00, 10)
    produto9 = Produto("Volante Gamer", "Logitech", "G29", "Preto", 500.00, 5)
    produto10 = Produto("Mouse Gamer", "Logitech", "G502", "Preto", 100.00, 10)


def login():
    # init()
    while True:
        print(menu_login())
        usuario = int(input("Digite o número correspondente ao usuário: "))
        match usuario:
            case 1:
                cliente(usuario, cliente_atual)
            case 2:
                admin(usuario)
            case 3:
                break
            case _:
                print("Opção inválida. Tente novamente.")


def cliente(usuario, cliente_atual):
    carrinho_compras = []
    while True:
        print(menu_cliente())
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
                carrinho_compras = carrinho(cliente_atual)
            case 5:
                realizar_compra(carrinho_compras)
            case 7:
                break
            case _:
                print('Opção errada, tente novamente')


def admin(usuario):
    while True:
        print(menu_admin())
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
                print('Opção errada, tente novamente')


def verQuantidadeProduto(opcao):
    campos = {
        9: ("marca", loja.get_estoque().get_quantidade_produto_por_marca),
        10: ("categoria", loja.get_estoque().get_quantidade_produto_por_categoria),
        11: ("modelo", loja.get_estoque().get_quantidade_produto_por_modelo)
    }

    nome_campo, func = campos[opcao]
    valor = input(f"Digite a {nome_campo} do produto: ")
    quantidade = func(valor)

    if quantidade is None:
        print("Produto não encontrado!")
        return

    print(f"Quantidade de produtos da {nome_campo} {valor}: {quantidade}")


def procurarProduto(opcao):
    campos = {
        5: ("nome", loja.get_estoque().get_produtos_por_nome),
        6: ("marca", loja.get_estoque().get_produtos_por_marca),
        7: ("categoria", loja.get_estoque().get_produtos_por_categoria)
    }

    nome_campo, func = campos[opcao]
    valor = input(f"Digite a {nome_campo} do produto: ")
    produtos = func(valor)

    if not produtos:
        print("Produto não encontrado!")
        return

    print("Produtos encontrados:")
    for produto in produtos:
        print(produto)


def validar(string):
    while True:
        campo = input(f"Digite {string}: ")
        if len(campo) > 0:
            if "CPF" in string:
                if len(campo) == 11:
                    cpf_ja_cadastrado = loja.is_cpf_cadastrado(campo)
                    if not cpf_ja_cadastrado:
                        return campo
                    print("CPF já cadastrado!")
                print("CPF inválido!")
            elif "RG" in string:
                if len(campo) == 9:
                    rg_ja_cadastrado = loja.is_rg_cadastrado(campo)
                    if not rg_ja_cadastrado:
                        return campo
                    print("RG já cadastrado!")
                print("RG inválido!")
            elif "telefone" in string:
                if len(campo) == 11:
                    telefone_ja_cadastrado = loja.is_telefone_cadastrado(campo)
                    if not telefone_ja_cadastrado:
                        return campo
                    print("Telefone já cadastrado!")
                print("Telefone inválido!")
            else:
                return campo
        print(f"{campo} inválido!")


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
            print("Cliente não cadastrado!")
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
                print("Funcionário não cadastrado!")
        else:
            fornecedor = Fornecedor(nome, cpf, rg, telefone, endereco, email)
            if loja.cadastrar(fornecedor):
                loja.cadastrar(fornecedor)
                print("Fornecedor cadastrado com sucesso!")
            else:
                print("Fornecedor não cadastrado!")


def edicaoPessoa(usuario, cliente_atual):
    if usuario == 1:
        if not cliente_atual.get_is_cadastrado():
            print("Você não está cadastrado!")
            return
        pessoa_atual = cliente_atual
    else:
        cpf = input("Digite o CPF do cliente que deseja editar: ")
        pessoa_atual = loja.get_cliente_por_cpf(cpf)
        if pessoa_atual is None:
            print("Cliente não encontrado!")
            return
    while True:
        print(menu_edicao_pessoa())
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
                print("Opção inválida. Tente novamente.")
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
        print("Produto não encontrado!")
        return
    while True:
        print(menu_edicao_produto())
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
                print("Opção inválida. Tente novamente.")
        print(produto)


def realizar_compra(cliente_atual):
    if not cliente_atual.get_is_cadastrado():
        print("Você não está cadastrado!")
        return
    carrinho = cliente_atual.get_carrinho()
    if carrinho.esta_vazio():
        print("Carrinho vazio!")
        return
    print("Produtos no carrinho:")
    for produto in carrinho.listar_produtos():
        print(produto)
    print(menu_pagamento())
    opcao = int(input("Digite o número correspondente à opção: "))
    match opcao:
        case 1:
            parcelas = int(input("Parcelas: "))
        case 2, 3:
            parcelas = 1
        case _:
            print("Opção inválida.")
            return
    modo_pagamento = opcao
    venda = Venda(cliente_atual, carrinho,
                  modo_pagamento)
    venda.set_parcelas(parcelas)
    venda.aplicar_venda(loja)
    print(venda.gerar_recibo(loja))
    carrinho.limpar()


def carrinho(cliente_atual):
    if not cliente_atual.get_is_cadastrado():
        print("Você não está cadastrado!")
        return
    carrinho = cliente_atual.get_carrinho()
    while True:
        print(menu_carrinho())
        opcao = int(input("Digite o número correspondente à opção: "))
        match opcao:
            case 1:
                print(loja.get_estoque().get_lista_produtos())
            case 2:
                nome = input("Nome do produto: ")
                produtos = loja.get_estoque().get_produtos_por_nome(nome)
                for p in produtos:  # Ou print(produtos)
                    print(p)
            case 3:
                id = int(input("ID do produto a remover: "))
                if carrinho.remover_produto_por_id(id):
                    print("Removido com sucesso.")
                else:
                    print("Produto não encontrado.")
            case 4:
                itens = carrinho.listar_produtos()
                if not itens:
                    print("Carrinho vazio.")
                else:
                    for item in itens:
                        print(item)
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
                    if carrinho.adicionar_produto(produto, qtd):
                        print("Produto adicionado!")
                        print(produto)
                    else:
                        print("Quantidade inválida!")
            print(carrinho)


def gerar_menu(titulo, opcoes):
    menu = f"\n##### {titulo.upper()} #####\n"
    i = 1
    for opcao in opcoes:
        menu += f"{i} - {opcao}\n"
        i += 1
    return menu


def menu_login():
    return gerar_menu("Login", ["Cliente", "Admin", "Encerrar programa"])


def menu_edicao_produto():
    return gerar_menu("Menu de Edição", ["Editar nome", "Editar marca", "Editar modelo", "Editar cor", "Editar preço", "Editar quantidade", "Sair"])


def menu_edicao_pessoa():
    return gerar_menu("Menu de Edição", ["Editar nome", "Editar CPF", "Editar telefone", "Editar email", "Editar RG", "Editar endereço", "Sair"])


def menu_pagamento():
    return gerar_menu("Menu de Pagamento", ["Cartão de crédito", "Cartão de débito", "Pix"])


def menu_carrinho():
    return gerar_menu("Menu Carrinho", [
        "Ver todos os produtos da loja para adicionar no carrinho",
        "Pesquisar produto para adicionar no carrinho",
        "Remover produto do carrinho",
        "Ver produtos no carrinho",
        "Sair do menu"
    ])


def menu_cliente():
    return gerar_menu("Menu Cliente", [
        "Cadastrar",
        "Editar cadastro",
        "Ver cadastro",
        "Carrinho de compras",
        "Realizar compra",
        "Ver últimas compras",
        "Sair do menu"
    ])


def menu_admin():
    return gerar_menu("Menu Admin", [
        "Cadastrar Produto",
        "Editar Produto",
        "Cadastrar Pessoa",
        "Editar Pessoa",
        "Ver produto por nome",
        "Ver produtos por marca",
        "Ver produtos por categoria",
        "Ver quantidade de tudo",
        "Ver quantidade de produtos por marca",
        "Ver quantidade de produtos por categoria",
        "Ver quantidade de produtos por modelo",
        "Sair do menu"
    ])


if __name__ == '__main__':
    login()
