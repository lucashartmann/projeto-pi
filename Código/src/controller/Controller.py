from view import View
from model import Init, Cliente, Produto, Fornecedor, Funcionario, Venda


def ver_quantidade_produto(opcao):
    campos = {
        9: ("marca", Init.loja.get_estoque().get_quantidade_produto_por_marca),
        10: ("categoria", Init.loja.get_estoque().get_quantidade_produto_por_categoria),
        11: ("modelo", Init.loja.get_estoque().get_quantidade_produto_por_modelo)
    }

    nome_campo, func = campos[opcao]
    valor = View.receber_dado(f"Digite a {nome_campo} do produto: ").upper()
    quantidade = func(valor)

    if quantidade is None:
        View.mostrar_mensagem("Erro. Produto não encontrado!")
        return

    View.mostrar_mensagem(
        f"Quantidade de produtos da {nome_campo} {valor}: {quantidade}")


def procurar_produto(opcao):
    campos = {
        5: ("nome", Init.loja.get_estoque().get_produtos_por_nome),
        6: ("marca", Init.loja.get_estoque().get_produtos_por_marca),
        7: ("categoria", Init.loja.get_estoque().get_produtos_por_categoria)
    }

    nome_campo, func = campos[opcao]
    valor = View.receber_dado(f"Digite a {nome_campo} do produto: ").upper()
    produtos = func(valor)

    if not produtos:
        View.mostrar_mensagem("Erro. Produto não encontrado!")
        return

    View.mostrar_mensagem("Produtos encontrados:")
    for produto in produtos:
        View.mostrar_mensagem(produto)


def validar(string):
    while True:
        campo = View.receber_dado(f"Digite {string}: ").upper()
        if len(campo) > 0:
            if "CPF" in string:
                if len(campo) == 11:
                    cpf_ja_cadastrado = Init.loja.is_cpf_cadastrado(campo)
                    if not cpf_ja_cadastrado:
                        return campo
                    View.mostrar_mensagem("Erro. CPF já cadastrado!")
            elif "RG" in string:
                if len(campo) == 9:
                    rg_ja_cadastrado = Init.loja.is_rg_cadastrado(campo)
                    if not rg_ja_cadastrado:
                        return campo
                    View.mostrar_mensagem("Erro. RG já cadastrado!")
            elif "telefone" in string:
                if len(campo) == 11:
                    telefone_ja_cadastrado = Init.loja.is_telefone_cadastrado(
                        campo)
                    if not telefone_ja_cadastrado:
                        return campo
                    View.mostrar_mensagem("Erro. Telefone já cadastrado!")
            else:
                return campo
        View.mostrar_mensagem(f"Erro. {campo} inválido!")


def cadastro_pessoa(usuario):
    nome = validar("o seu nome")
    cpf = validar("o seu CPF")
    telefone = validar("o seu telefone")
    email = validar("o seu email")
    rg = validar("a sua RG")
    endereco = validar("o seu endereço")
    if usuario == 1:
        cliente_atual = Cliente(nome, cpf, rg, telefone, endereco, email)
        if Init.loja.cadastrar(cliente_atual):
            Init.loja.cadastrar(cliente_atual)
            cliente_atual.set_is_cadastrado(True)
            View.mostrar_mensagem("Cliente cadastrado com sucesso!")
            View.mostrar_mensagem(cliente_atual)
            return cliente_atual
        else:
            View.mostrar_mensagem("Erro. Cliente não cadastrado!")
    else:
        View.mostrar_mensagem("1 - Funcionário")
        View.mostrar_mensagem("2 - Fornecedor")
        tipo = int(View.receber_dado("Digite o tipo de pessoa: "))
        if tipo == 1:
            funcionario = Funcionario(nome, cpf, rg, telefone, endereco, email)
            if Init.loja.cadastrar(funcionario):
                Init.loja.cadastrar(funcionario)
                View.mostrar_mensagem("Funcionário cadastrado com sucesso!")
            else:
                View.mostrar_mensagem("Erro. Funcionário não cadastrado!")
        else:
            fornecedor = Fornecedor(nome, cpf, rg, telefone, endereco, email)
            if Init.loja.cadastrar(fornecedor):
                Init.loja.cadastrar(fornecedor)
                View.mostrar_mensagem("Fornecedor cadastrado com sucesso!")
            else:
                View.mostrar_mensagem("Erro. Fornecedor não cadastrado!")


def edicao_pessoa(usuario, cliente_atual):
    if usuario == 1:
        if not cliente_atual.get_is_cadastrado():
            View.mostrar_mensagem("Erro. Você não está cadastrado!")
            return
        pessoa_atual = cliente_atual
    else:
        cpf = View.receber_dado("Digite o CPF do cliente que deseja editar: ")
        pessoa_atual = Init.loja.get_cliente_por_cpf(cpf)
        if pessoa_atual is None:
            View.mostrar_mensagem("Erro. Cliente não encontrado!")
            return
    while True:
        View.menu_edicao_pessoa()
        opcao = int(View.receber_dado(
            "Digite o número correspondente à opção: "))
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
                View.mostrar_mensagem("Saindo da edição...")
                break
            case _:
                View.mostrar_mensagem("Erro. Opção inválida. Tente novamente.")
        View.mostrar_mensagem(pessoa_atual)


def cadastro_produto():
    nome = validar("o nome do produto")
    marca = validar("a marca do produto")
    modelo = validar("o modelo do produto")
    cor = validar("a cor do produto")
    preco = float(validar("o preço do produto"))
    quantidade = int(validar("a quantidade do produto"))
    novo_produto = Produto(nome, marca, modelo, cor, preco, quantidade)
    cadastrado = Init.loja.get_estoque().adicionar_produto(novo_produto)
    if cadastrado:
        View.mostrar_mensagem("\nProduto cadastrado com sucesso!")
        View.mostrar_mensagem(novo_produto)
    else:
        View.mostrar_mensagem("\nErro. Não foi possivel cadastrar o produto")


def edicao_produto():
    id = int(View.receber_dado("Digite o ID do produto que deseja editar: "))
    produto = Init.loja.get_estoque().get_produto_por_id(id)
    if produto is None:
        View.mostrar_mensagem("Erro. Produto não encontrado!")
        return
    while True:
        View.menu_edicao_produto()
        opcao = int(View.receber_dado(
            "Digite o número correspondente a opção: "))
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
                View.mostrar_mensagem("Erro. Opção inválida. Tente novamente.")
        View.mostrar_mensagem(produto)


def realizar_compra(cliente_atual):
    if not cliente_atual.get_is_cadastrado():
        View.mostrar_mensagem("Erro. Você não está cadastrado!")
        return
    carrinho = cliente_atual.get_carrinho()
    if carrinho.esta_vazio():
        View.mostrar_mensagem("Erro. Carrinho vazio!")
        return
    View.mostrar_mensagem("Produtos no carrinho:")
    for produto in carrinho.listar_produtos():
        View.mostrar_mensagem(produto)
    View.menu_pagamento()
    opcao = int(View.receber_dado("Digite o número correspondente à opção: "))
    match opcao:
        case 1:
            parcelas = int(View.receber_dado("Parcelas: "))
        case 2 | 3:
            parcelas = 1
        case _:
            View.mostrar_mensagem("Erro. Opção inválida.")
            return
    modo_pagamento = opcao
    venda = Venda(cliente_atual, carrinho,
                  modo_pagamento)
    venda.set_parcelas(parcelas)
    venda.aplicar_venda(Init.loja)
    View.mostrar_mensagem(venda.gerar_recibo(Init.loja))
    carrinho.limpar()
    quit()


def carrinho(cliente_atual):
    if not cliente_atual.get_is_cadastrado():
        View.mostrar_mensagem("Você não está cadastrado!")
        return
    carrinho = cliente_atual.get_carrinho()
    while True:
        View.menu_carrinho()
        opcao = int(View.receber_dado(
            "Digite o número correspondente à opção: "))
        match opcao:
            case 1:
                produtos_estoque = Init.loja.get_estoque().get_lista_produtos()
                for produto in produtos_estoque:
                    View.mostrar_mensagem(produto)
            case 2:
                nome = View.receber_dado("Nome do produto: ")
                nome = nome.upper()
                produtos = Init.loja.get_estoque().get_produtos_por_nome(nome)
                if not produtos:
                    View.mostrar_mensagem(
                        f"Erro. Nenhum produto {nome} no estoque")
                else:
                    for p in produtos:
                        View.mostrar_mensagem(p)
            case 3:
                id = int(View.receber_dado("ID do produto a remover: "))
                removido = carrinho.remover_produto_por_id(id)
                if removido:
                    View.mostrar_mensagem("Removido com sucesso.")
                else:
                    View.mostrar_mensagem("Erro. Produto não encontrado.")
            case 4:
                itens = carrinho.listar_produtos()
                if not itens:
                    View.mostrar_mensagem("Erro. Carrinho vazio.")
                else:
                    View.mostrar_mensagem("Produtos no carrinho:")
                    for produto, quantidade in itens.items():
                        View.mostrar_mensagem(
                            produto, "Quantidade:", quantidade)
            case 5:
                return carrinho
            case _:
                View.mostrar_mensagem("Opção inválida.")
        if opcao == 1 or opcao == 2:
            while True:
                id = int(View.receber_dado("ID do produto (ou 0 para sair): "))
                if id == 0:
                    break
                produto = Init.loja.get_estoque().get_produto_por_id(id)
                if produto:
                    qtd = int(View.receber_dado("Quantidade: "))
                    adicionar = carrinho.adicionar_produto(produto, qtd)
                    if adicionar:
                        View.mostrar_mensagem("Produto adicionado!")
                        View.mostrar_mensagem(produto)
                    else:
                        View.mostrar_mensagem("Erro. Quantidade inválida!")
                else:
                    View.mostrar_mensagem("Erro. Produto não encontrado.")
def dados():
    View.mostrar_mensagem("Quantidade de Produtos: ", Init.loja.get_estoque().get_quantidade_produtos(), "\nQuantidade de clientes: ", Init.loja.get_quantidade_clientes(), "\nQuantidade de funcionários: ",
                                      Init.loja.get_quantidade_funcionarios(), "\nQuantidade de fornecedores: ", Init.loja.get_quantidade_fornecedores())