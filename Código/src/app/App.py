from model import Init
from view import View
from controller.Controller_CMD import Controller
import sys


def menu_cmd(comando):
    match comando:
        case ["cadastrar_cliente", nome, cpf, rg, telefone, endereco, email]:
            Controller.cadastrar_cliente(
                nome, cpf, rg, telefone, endereco, email)
        case ["editar_cliente", cpf, dados]:
            pass
        case ["cadastrar_fornecedor"]:
            pass
        case ["editar_fornecedor"]:
            pass
        case ["cadastrar_funcionario"]:
            pass
        case ["editar_funcionario"]:
            pass
        case ["cadastrar produto", nome, marca, modelo, cor, preco, quantidade, categoria]:
            Controller.cadastrar_produto(
                nome, marca, modelo, cor, preco, quantidade, categoria)
        case ["editar produto", id, nome, marca, modelo, cor, preco, quantidade, categoria]:
            Controller.editar_produto(id, nome, marca, modelo, cor, preco, quantidade, categoria)



comando = sys.argv[1:]

if len(comando) > 0:
    menu_cmd(comando)


def login():
    while True:
        View.menu_login()
        usuario = int(View.receber_dado(
            "Digite o número correspondente ao usuário"))
        match usuario:
            case 1:
                cliente(usuario, Init.cliente_atual)
            case 2:
                admin(usuario)
            case 3:
                break
            case _:
                View.mostrar_mensagem("Erro. Opção inválida. Tente novamente.")


def cliente(usuario, cliente_atual):
    while True:
        View.menu_cliente()
        opcao = int(View.receber_dado(
            "Digite o número correspondente ao usuário"))
        View.mostrar_mensagem("")
        match opcao:
            case 1:
                cliente_atual = Controller.cadastro_pessoa(usuario)
            case 2:
                Controller.edicao_pessoa(usuario, cliente_atual)
            case 3:
                View.mostrar_mensagem(cliente_atual)
            case 4:
                Controller.carrinho(cliente_atual)
            case 5:
                Controller.realizar_compra(cliente_atual)
            case 7:
                break
            case _:
                View.mostrar_mensagem('Erro. Opção errada, tente novamente')


def admin(usuario):
    while True:
        View.menu_admin()
        opcao = int(View.receber_dado(
            'Digite o número correspondente a opção'))
        View.mostrar_mensagem("")
        match opcao:
            case 1:
                Controller.cadastro_produto()
            case 2:
                Controller.edicao_produto()
            case 3:
                Controller.cadastro_pessoa(usuario)
            case 4:
                Controller.edicao_pessoa(usuario, Init.cliente_atual)
            case 5 | 6 | 7:
                Controller.procurar_produto(opcao)
            case 8:
                Controller.dados()
            case 9 | 10 | 11:
                Controller.ver_quantidade_produto(opcao)
            case 12:
                break
            case _:
                View.mostrar_mensagem('Erro. Opção errada, tente novamente')
