from view.App import App
from controller import Controller
import sys

comando = sys.argv[1:]


def menu_cmd(comando):
    match comando:
        case ["cadastrar_cliente", nome, cpf, rg, telefone, endereco, email]:
            dados = [nome, cpf, rg, telefone, endereco, email]
            Controller.cadastrar_cliente(dados)
        case ["editar_cliente", cpf, novo_nome, novo_cpf, novo_rg, novo_telefone, novo_endereco, novo_email]:
            dados = [novo_nome, novo_cpf, novo_rg,
                     novo_telefone, novo_endereco, novo_email]
            Controller.editar_cliente(cpf, dados)
        case ["cadastrar_fornecedor"]:
            pass
        case ["editar_fornecedor"]:
            pass
        case ["cadastrar_funcionario"]:
            pass
        case ["editar_funcionario"]:
            pass
        case ["cadastrar_produto", nome, marca, modelo, cor, preco, quantidade, categoria]:
            dados = [nome, marca, modelo, cor, preco, quantidade, categoria]
            Controller.cadastrar_produto(dados)
        case ["editar_produto", id, novo_nome, nova_marca, novo_modelo, nova_cor, novo_preco, nova_quantidade, nova_categoria]:
            dados = [novo_nome, nova_marca, novo_modelo, nova_cor,
                     novo_preco, nova_quantidade, nova_categoria]
            Controller.editar_produto(id, dados)


if __name__ == "__main__":
    if comando:
        menu_cmd(comando)
    else:
        app = App()
        app.run()
