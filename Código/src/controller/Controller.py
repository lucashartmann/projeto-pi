from model import Cliente, Produto, Init
from view import View


def ver_produtos_estoque():
    return Init.loja.get_estoque().get_lista_produtos()


def cadastrar_cliente(lista):
    if lista[0] == "":
        View.mostrar_mensagem("Nome está vazio")
        return "Nome está vazio"
    validar(lista[1])
    validar(lista[2])
    validar(lista[3])
    if lista[4] == "":
        View.mostrar_mensagem("Endereco está vazio")
        return "Endereco está vazio"
    if lista[5] == "":
        View.mostrar_mensagem("Email está vazio")
        return "Email está vazio"

    cliente = Cliente.Cliente(lista[0], lista[1], lista[2],
                              lista[3], lista[4], lista[5])
    cadastrado = Init.loja.cadastrar(cliente)

    if cadastrado:
        View.mostrar_mensagem(f"Cliente cadastrado!\n {cliente}")
        return f"Cliente cadastrado!\n {cliente}"
    else:
        View.mostrar_mensagem("ERRO ao cadastrar cliente")
        return "ERRO ao cadastrar cliente"


def cadastrar_produto(lista):
    if lista[0] == "":
        View.mostrar_mensagem("Nome está vazio")
        return "Nome está vazio"
    if lista[1] == "":
        View.mostrar_mensagem("Marca está vazio")
        return "Marca está vazio"
    if lista[2] == "":
        View.mostrar_mensagem("Modelo está vazio")
        return "Modelo está vazio"
    if lista[3] == "":
        View.mostrar_mensagem("Cor está vazio")
        return "Cor está vazio"
    if lista[4] == "":
        View.mostrar_mensagem("Preço está vazio")
        return "Preço está vazio"
    if lista[5] == "":
        View.mostrar_mensagem("Quantidade está vazio")
        return "Quantidade está vazio"
    if lista[6] == "":
        View.mostrar_mensagem("Categoria  está vazio")
        return "Categoria  está vazio"

    try:
        lista[4] = float(lista[4])
    except ValueError:
        View.mostrar_mensagem("ERRO Preço incorreto")
        return "ERRO Preço incorreto"

    try:
        lista[5] = int(lista[5])
    except ValueError:
        View.mostrar_mensagem("ERRO Quantidade incorreta")
        return "ERRO Quantidade incorreta"

    produto = Produto.Produto(lista[0], lista[1], lista[2],
                              lista[3], lista[4], lista[5], lista[6])
    cadastrado = Init.loja.get_estoque().adicionar_produto(produto)

    if cadastrado:
        View.mostrar_mensagem(f"Produto cadastrado!\n {produto}")
        return f"Produto cadastrado!\n {produto}"
    else:
        View.mostrar_mensagem("ERRO ao cadastrar produto")
        return "ERRO ao cadastrar produto"


def editar_produto(id, lista):
    if len(id) < 1:
        View.mostrar_mensagem("ERRO")
        return "ERRO"
    try:
        id = int(id)
    except ValueError:
        View.mostrar_mensagem("ERRO")
        return "ERRO"
    produto = Init.loja.get_estoque().get_produto_por_id(id)
    if not produto:
        View.mostrar_mensagem("ERRO")
        return "ERRO"
    if lista[0] != "":
        produto.set_nome(lista[0])
    if lista[1] != "":
        produto.set_marca(lista[1])
    if lista[2] != "":
        produto.set_modelo(lista[2])
    if lista[3] != "":
        produto.set_cor(lista[3])
    if lista[4] != "":
        try:
            lista[4] = float(lista[4])
        except ValueError:
            View.mostrar_mensagem(f"O valor {lista[4]} está incorreto")
            return (f"O valor {lista[4]} está incorreto")
        produto.set_preco(lista[4])
    if lista[5] != "":
        try:
            lista[5] = int(lista[5])
        except ValueError:
            View.mostrar_mensagem(f"O valor {lista[5]} está incorreto")
            return (f"O valor {lista[5]} está incorreto")
        produto.set_quantidade(lista[5])
    if lista[6] != "":
        produto.set_categoria(lista[6])
    View.mostrar_mensagem(f"Produto editado com sucesso\n {produto}")
    return f"Produto editado com sucesso\n {produto}"


def editar_cliente(cpf, dados):
    validar(cpf, "CPF")
    cliente = Init.loja.get_cliente_por_cpf(cpf)
    if not cliente:
        View.mostrar_mensagem(f"Cliente com CPF {cpf} não encontrado")
        return f"Cliente com CPF {cpf} não encontrado"
    if dados[0] != "":
        cliente.set_nome(dados[0])
    if dados[1] != "":
        validar(dados[1])
        cliente.set_cpf(dados[1])
    if dados[2] != "":
        validar(dados[2])
        cliente.set_rg(dados[2])
    if dados[3] != "":
        validar(dados[3])
        cliente.set_telefone(dados[3])
    if dados[4] != "":
        cliente.set_endereco(dados[4])
    if dados[5] != "":
        cliente.set_email(dados[5])
    View.mostrar_mensagem(f"Cliente editado com sucesso\n {cliente}")
    return f"Cliente editado com sucesso\n {cliente}"


def validar(valor, tipo):
    match tipo:
        case "CPF":
            if len(valor) == 11:
                cpf_ja_cadastrado = Init.loja.is_cpf_cadastrado(valor)
                if cpf_ja_cadastrado:
                    View.mostrar_mensagem("Erro. CPF já cadastrado!")
                    return "Erro. CPF já cadastrado!"
            else:
                View.mostrar_mensagem(
                    f"ERRO. {valor} precisa ter 11 digitos")
                return f"ERRO. {valor} precisa ter 11 digitos"
        case "RG":
            if len(valor) == 9:
                rg_ja_cadastrado = Init.loja.is_rg_cadastrado(valor)
                if rg_ja_cadastrado:
                    View.mostrar_mensagem("Erro. RG já cadastrado!")
                    return "Erro. RG já cadastrado!"
            else:
                View.mostrar_mensagem(
                    f"ERRO. {valor} precisa ter 9 digitos")
                return f"ERRO. {valor} precisa ter 9 digitos"
        case "TELEFONE":
            if len(valor) == 11:
                telefone_ja_cadastrado = Init.loja.is_telefone_cadastrado(
                    valor)
                if telefone_ja_cadastrado:
                    View.mostrar_mensagem("Erro. Telefone já cadastrado!")
                    return "Erro. Telefone já cadastrado!"
            else:
                View.mostrar_mensagem(
                    f"ERRO. {valor} precisa ter 11 digitos")
                return f"ERRO. {valor} precisa ter 11 digitos"


def remover_cliente(cpf):
    validar(cpf, "CPF")
    cliente = Init.loja.get_cliente_por_cpf(cpf)
    if not cliente:
        View.mostrar_mensagem(f"Cliente com CPF {cpf} não encontrado")
        return f"Cliente com CPF {cpf} não encontrado"
    remocao = Init.loja.remover(cliente)
    if remocao:
        View.mostrar_mensagem(f"Cliente removido com sucesso")
        return f"Cliente removido com sucesso"
    else:
        View.mostrar_mensagem(f"ERRO ao remover cliente")
        return f"ERRO ao remover cliente"

    def remover_produto(self, id):
        if len(id) < 1:
            View.mostrar_mensagem("ERRO")
            return "ERRO"
        try:
            id = int(id)
        except ValueError:
            View.mostrar_mensagem("ERRO")
            return "ERRO"
        produto = Init.loja.get_estoque().get_produto_por_id(id)
        if not produto:
            View.mostrar_mensagem("ERRO")
            return "ERRO"
        remocao = Init.loja.get_estoque().remover_produto(produto)
        if remocao:
            View.mostrar_mensagem(f"Produto removido com sucesso")
            return f"Produto removido com sucesso"
        else:
            View.mostrar_mensagem(f"ERRO ao remover produto")
            return f"ERRO ao remover produto"
