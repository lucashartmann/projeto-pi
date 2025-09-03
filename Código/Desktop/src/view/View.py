def mostrar_mensagem(mensagem):
    print(mensagem)


def receber_dado(mensagem):
    dado = input(f"{mensagem.capitalize()}: ")
    return dado


def menu_login():
    menu = '''
## Login ## 
1. Cliente 
2. Admin 
3. Encerrar programa
        '''
    mostrar_mensagem(menu)


def menu_cliente():
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
    mostrar_mensagem(menu)


def menu_admin():
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
    mostrar_mensagem(menu)


def menu_carrinho():
    menu = '''
### Menu Carrinho ###
1. Ver todos os produtos da loja para adicionar no carrinho
2. Pesquisar produto para adicionar no carrinho
3. Remover produto do carrinho
4. Ver produtos no carrinho
5. Sair do menu
        '''
    mostrar_mensagem(menu)


def menu_pagamento():
    menu = '''
## Menu de Pagamento ##
1. Cartão de crédito
2. Cartão de débito
3. Pix
    '''
    mostrar_mensagem(menu)


def menu_edicao_produto():
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
    mostrar_mensagem(menu)


def menu_edicao_pessoa():
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
    mostrar_mensagem(menu)
