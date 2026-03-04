from view.app import App
from controller import controller
import sys

comando = sys.argv[1:]

# pyinstaller  --hidden-import textual.widgets._tab_pane Main.py


def ajuda():
    mensagem = '''
    # Comandos:
    # python Main.py cadastrar_cliente "pedro" "00000000000", "00000000", "00000000000", "Bento 205", "pedro@email.com"
    # python Main.py editar_cliente "00000000000" "pedro" "00000000000", "00000000", "00000000000", "Bento 205", "pedro@email.com"
    # python Main.py remover_cliente "lucas@email.com"
    # python Main.py cadastrar_imovel
    # python Main.py editar_imovel 1
    # python Main.py remover_imovel 1
    '''

    return mensagem


def menu_cmd(comando):
    match comando:
        case ["cadastrar_cliente"]:
            controller.cadastrar_cliente()
        case ["editar_cliente"]:
            controller.editar_cliente()
        case ["remover_cliente", cpf]:
            controller.remover(cpf, "usuario")

        case ["cadastrar_corretor"]:
            controller.cadastrar_corretor()
        case ["editar_corretor"]:
            controller.editar_corretor()
        case ["remover_corretor", cpf]:
            controller.remover(cpf, "usuario")

        case ["cadastrar_captador"]:
            controller.cadastrar_captador()
        case ["editar_captador"]:
            controller.editar_captador()
        case ["remover_captador", cpf]:
            controller.remover(cpf, "usuario")

        case ["cadastrar_gerente"]:
            controller.cadastrar_gerente()
        case ["editar_gerente"]:
            controller.editar_gerente()
        case ["remover_gerente", cpf]:
            controller.remover(cpf, "usuario")

        case ["cadastrar_administrador"]:
            controller.cadastrar_administrador()
        case ["editar_administrador"]:
            controller.editar_administrador()
        case ["remover_administrador", cpf]:
            controller.remover(cpf, "usuario")

        case ["cadastrar_proprietario"]:
            controller.cadastrar_proprietario()
        case ["editar_proprietario"]:
            controller.editar_proprietario()
        case ["remover_proprietario", cpf]:
            controller.remover(cpf, "proprietario")

        case ["cadastrar_atendimento"]:
            controller.cadastrar_atendimento()
        case ["editar_atendimento"]:
            controller.editar_atendimento()
        case ["remover_atendimento", cpf]:
            controller.remover(cpf, "atendimento")

        case ["cadastrar_anuncio"]:
            controller.cadastrar_anuncio()
        case ["editar_anuncio"]:
            controller.editar_anuncio()
        case ["remover_anuncio", cpf]:
            controller.remover(cpf, "anuncio")

        case ["cadastrar_condominio"]:
            controller.cadastrar_condominio()
        case ["editar_condominio"]:
            controller.editar_condominio()
        case ["remover_condominio", cpf]:
            controller.remover(cpf, "condominio")

        case ["cadastrar_imovel"]:
            controller.cadastrar_imovel()
        case ["editar_imovel"]:
            controller.editar_imovel()
        case ["remover_imovel", id]:
            controller.remover(id, "imovel")

        case ["ajuda"]:
            print(ajuda())


if __name__ == "__main__":
    if comando:
        menu_cmd(comando)
    else:
        # app = App(ansi_color=True)
        app = App()
        app.run()
