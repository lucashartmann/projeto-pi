from model import Cliente, Produto, Init


def cadastrar_cliente(lista):
    if lista[0] == "":
        return "Nome está vazio"

    # validar(lista[1])
    # validar(lista[2])
    # validar(lista[3])

    if lista[4] == "":
        return "Endereco está vazio"

    if lista[5] == "":
        return "Email está vazio"

    cliente = Cliente.Cliente(lista[0], lista[1], lista[2],
                              lista[3], lista[4], lista[5])

    cadastrado = Init.loja.cadastrar(cliente)

    if cadastrado:
        return f"Cliente cadastrado!\n {cliente}"
    else:
        return "ERRO ao cadastrar cliente"


def cadastrar_produto(lista):
    if lista[0] == "":
        return "Nome está vazio"

    if lista[1] == "":
        return "Marca está vazio"

    if lista[2] == "":
        return "Modelo está vazio"

    if lista[3] == "":
        return "Cor está vazio"

    if lista[4] == "":
        return "Preço está vazio"

    if lista[5] == "":
        return "Quantidade está vazio"

    if lista[6] == "":
        return "Categoria  está vazio"

    try:
        lista[4] = float(lista[4])
    except ValueError:
        return "ERRO Preço incorreto"

    try:
        lista[5] = int(lista[5])
    except ValueError:
        return "ERRO Quantidade incorreta"

    produto = Produto.Produto(lista[0], lista[1], lista[2],
                              lista[3], lista[4], lista[5], lista[6])
    cadastrado = Init.loja.get_estoque().adicionar_produto(produto)

    if cadastrado:
        return f"Produto cadastrado!\n {produto}"
    else:
        return "ERRO ao cadastrar produto"


def editar_produto(id, lista):
    if len(id) < 1:
        return "ERRO"

    try:
        id = int(id)
    except ValueError:
        return "ERRO"

    produto = Init.loja.get_estoque().get_produto_por_id(id)

    if not produto:
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
            return (f"O valor {lista[4]} está incorreto")
        produto.set_preco(lista[4])

    if lista[5] != "":
        try:
            lista[5] = int(lista[5])
        except ValueError:
            return (f"O valor {lista[5]} está incorreto")
        produto.set_quantidade(lista[5])

    if lista[6] != "":
        produto.set_categoria(lista[6])

    return f"Produto editado com sucesso\n {produto}"


def editar_cliente(cpf, dados):
    validar(cpf, "CPF")

    cliente = Init.loja.get_cliente_por_cpf(cpf)

    if not cliente:
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

    return f"Cliente editado com sucesso\n {cliente}"


def validar(valor, tipo):
    match tipo:

        case "CPF":
            if len(valor) == 11:
                cpf_ja_cadastrado = Init.loja.is_cpf_cadastrado(valor)
                if cpf_ja_cadastrado:
                    return "Erro. CPF já cadastrado!"
            else:
                return f"ERRO. {valor} precisa ter 11 digitos"

        case "RG":
            if len(valor) == 9:
                rg_ja_cadastrado = Init.loja.is_rg_cadastrado(valor)
                if rg_ja_cadastrado:
                    return "Erro. RG já cadastrado!"
            else:
                return f"ERRO. {valor} precisa ter 9 digitos"

        case "TELEFONE":
            if len(valor) == 11:
                telefone_ja_cadastrado = Init.loja.is_telefone_cadastrado(
                    valor)
                if telefone_ja_cadastrado:
                    return "Erro. Telefone já cadastrado!"
            else:
                return f"ERRO. {valor} precisa ter 11 digitos"


def remover_cliente(cpf):
    validar(cpf, "CPF")

    cliente = Init.loja.get_cliente_por_cpf(cpf)

    if not cliente:
        return f"Cliente com CPF {cpf} não encontrado"

    remocao = Init.loja.remover(cliente)

    if remocao:
        return f"Cliente removido com sucesso"
    else:
        return f"ERRO ao remover cliente"


def remover_produto(id):
    if len(id) < 1:
        return "ERRO"

    try:
        id = int(id)
    except ValueError:
        return "ERRO"

    produto = Init.loja.get_estoque().get_produto_por_id(id)

    if not produto:
        return "ERRO"

    remocao = Init.loja.get_estoque().remover_produto(produto)

    if remocao:
        return f"Produto removido com sucesso"
    else:
        return f"ERRO ao remover produto"
