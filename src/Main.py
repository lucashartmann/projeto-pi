from view.App import App
from controller import Controller
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
            Controller.cadastrar_cliente()
        case ["editar_cliente"]:
            Controller.editar_cliente()
        case ["remover_cliente", cpf]:
            Controller.remover(cpf, "usuario")

        case ["cadastrar_corretor"]:
            Controller.cadastrar_corretor()
        case ["editar_corretor"]:
            Controller.editar_corretor()
        case ["remover_corretor", cpf]:
            Controller.remover(cpf, "usuario")

        case ["cadastrar_captador"]:
            Controller.cadastrar_captador()
        case ["editar_captador"]:
            Controller.editar_captador()
        case ["remover_captador", cpf]:
            Controller.remover(cpf, "usuario")

        case ["cadastrar_gerente"]:
            Controller.cadastrar_gerente()
        case ["editar_gerente"]:
            Controller.editar_gerente()
        case ["remover_gerente", cpf]:
            Controller.remover(cpf, "usuario")

        case ["cadastrar_administrador"]:
            Controller.cadastrar_administrador()
        case ["editar_administrador"]:
            Controller.editar_administrador()
        case ["remover_administrador", cpf]:
            Controller.remover(cpf, "usuario")

        case ["cadastrar_proprietario"]:
            Controller.cadastrar_proprietario()
        case ["editar_proprietario"]:
            Controller.editar_proprietario()
        case ["remover_proprietario", cpf]:
            Controller.remover(cpf, "proprietario")

        case ["cadastrar_atendimento"]:
            Controller.cadastrar_atendimento()
        case ["editar_atendimento"]:
            Controller.editar_atendimento()
        case ["remover_atendimento", cpf]:
            Controller.remover(cpf, "atendimento")

        case ["cadastrar_anuncio"]:
            Controller.cadastrar_anuncio()
        case ["editar_anuncio"]:
            Controller.editar_anuncio()
        case ["remover_anuncio", cpf]:
            Controller.remover(cpf, "anuncio")

        case ["cadastrar_condominio"]:
            Controller.cadastrar_condominio()
        case ["editar_condominio"]:
            Controller.editar_condominio()
        case ["remover_condominio", cpf]:
            Controller.remover(cpf, "condominio")

        case ["cadastrar_imovel"]:
            Controller.cadastrar_imovel()
        case ["editar_imovel"]:
            Controller.editar_imovel()
        case ["remover_imovel", id]:
            Controller.remover(id, "imovel")

        case ["ajuda"]:
            print(ajuda())


if __name__ == "__main__":
    if comando:
        menu_cmd(comando)
    else:
        # app = App(ansi_color=True)
        app = App()
        app.run()