from view.App import App
from controller import Controller
import sys

comando = sys.argv[1:]

# pyinstaller  --hidden-import textual.widgets._tab_pane Main.py

# Comandos:
# python Main.py cadastrar_cliente "pedro" "00000000000", "00000000", "00000000000", "Bento 205", "pedro@email.com"
# python Main.py editar_cliente "00000000000" "pedro" "00000000000", "00000000", "00000000000", "Bento 205", "pedro@email.com"
# python Main.py remover_cliente "lucas@email.com"
# python Main.py cadastrar_produto "PLAYSTATION 5", "SONY", "SLIM", "PRETO", 3000.00, 10, "CONSOLE"
# python Main.py editar_produto 1 "PLAYSTATION 5", "SONY", "SLIM", "PRETO", 3000.00, 10, "CONSOLE"
# python Main.py remover_produto 1


def menu_cmd(comando):
    match comando:
        case ["cadastrar_cliente", nome, cpf, rg, telefone, endereco, email]:
            dados = [nome, cpf, rg, telefone, endereco, email]
            Controller.cadastrar_cliente(dados)
        case ["editar_cliente", cpf, novo_nome, novo_cpf, novo_rg, novo_telefone, novo_endereco, novo_email]:
            dados = [novo_nome, novo_cpf, novo_rg,
                     novo_telefone, novo_endereco, novo_email]
            Controller.editar_cliente(cpf, dados)
        case ["remover_cliente", cpf]:
            Controller.remover_cliente(cpf)
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
        case ["remover_produto", id]:
            Controller.remover_produto(id)


if __name__ == "__main__":
    if comando:
        menu_cmd(comando)
    else:
        app = App()
        app.run()
