from api import API
from database import Banco

banco = Banco.Banco()

def cadastrar_pessoa(lista):
    if lista[0] == "":
        return "Nome está vazio"

        nome_split = dados["name"].split()
        

    if lista[4] == "":
        return "Endereco está vazio"

    if lista[5] == "":
        return "Email está vazio"

    if lista[-1] == "Cliente":
        pessoa = Cliente.Cliente(lista[0], lista[1], lista[2],
                                 lista[3], lista[4], lista[5])
    else:
        pessoa = Funcionario.Funcionario(lista[0], lista[1], lista[2],
                                         lista[3], lista[4], lista[5])

    cadastrado = Init.loja.cadastrar(pessoa)

    if cadastrado:
        return f"Pessoa cadastrado!\n {pessoa}"
    else:
        return "ERRO ao cadastrar pessoa"


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


def editar_pessoa(cpf, dados):
    validar(cpf, "CPF")

    if dados[-1] == "Cliente":
        pessoa = Init.loja.get_cliente_por_cpf(cpf)
    else:
        pessoa = Init.loja.get_funcionario_por_cpf(cpf)

    if not pessoa:
        return f"Pessoa com CPF {cpf} não encontrado"

    if dados[0] != "":
        pessoa.set_nome(dados[0])
    if dados[1] != "":
        validar(dados[1])
        pessoa.set_cpf(dados[1])
    if dados[2] != "":
        validar(dados[2])
        pessoa.set_rg(dados[2])
    if dados[3] != "":
        validar(dados[3])
        pessoa.set_telefone(dados[3])
    if dados[4] != "":
        pessoa.set_endereco(dados[4])
    if dados[5] != "":
        pessoa.set_email(dados[5])

    return f"Pessoa editado com sucesso\n {pessoa}"


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


def remover_pessoa(cpf, tipo_pessoa):

    validar(cpf, "CPF")

    if tipo_pessoa == "Cliente":
        pessoa = Init.loja.get_cliente_por_cpf(cpf)
    else:
        pessoa = Init.loja.get_funcionario_por_cpf(cpf)

    if not pessoa:
        return f"Pessoa com CPF {cpf} não encontrado"

    remocao = Init.loja.remover(pessoa)

    if remocao:
        return f"Pessoa removida com sucesso"
    else:
        return f"ERRO ao remover pessoa"


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

def salvar_login(usuario):

    consulta = banco.cadastrar_usuario(usuario)

        if erro or not consulta:
            return "Controller.adicionar_item: ERRO! Cliente não cadastrado"

    adicao, erro = API.adicionar(tabela, dados)

    if erro:
        return f"Controller.adicionar_item: ERRO! API.adicionar: {erro}"

    if adicao:
        return f"Cadastro realizado com sucesso!"
    
    return f"Controller.adicionar_item: ERRO! Não foi possivel realizar cadastro"


def remover_item(tabela, id_item):
    if id_item == "":
        return "ID está vazio"
    
    consulta, erro = API.get_item(tabela, id_item)

    if erro:
        return f"Controller.remover_item: ERRO! API.get_item: {erro}"
    
    if not consulta:
        return f"Controller.remover_item: ERRO! Não existe item com id '{id_item}'"


    remocao, erro = API.remover(tabela, id_item)

    if erro:
        return f"Controller.remover_item: ERRO! API.remover: {erro}"

    if remocao:
        return "Remoção realizada com sucesso"
    
    return f"Controller.remover_item: ERRO! Não foi possivel remover '{id_item}'"


def atualizar_item(tabela, id_item, dados):
    if id_item == "":
        return "Controller.atualizar_item: ERRO! ID está vazio"
    
    consulta, erro = API.get_item(tabela, id_item)

    if erro:
        return f"Controller.atualizar_item: ERRO! API.get_item: {erro}"

    if not consulta:
        return f"Controller.atualizar_item: ERRO! Não existe item com id '{id_item}'"

    resultado_atualizacao = ""

    if tabela == "customers" and "name" in dados.keys() and dados["name"]:

        nome_split = dados["name"].split()

        if len(nome_split) > 1:
            dados["first_name"] = nome_split[:-1]
            dados["last_name"] = nome_split[-1]
            del dados["name"]

    for chave, valor in dados.items():
        if valor: 
            
            atualizacao, erro = API.atualizar(tabela, id_item, chave, valor)

            if erro:
                resultado_atualizacao += f"Controller.atualizar_item: ERRO! API.atualizar: {erro}"
    
            if atualizacao:
                resultado_atualizacao += f"{chave.capitalize()} atualizado com sucesso com sucesso\n"
            else:
                resultado_atualizacao += f"Controller.atualizar_item: ERRO! Não foi possivel atualizar {chave} de '{id_item}'"

    return resultado_atualizacao

def listar_itens(tabela):
    filtros_tabela = {
        "products": ["id", "name", "price", "description"],
        "customers": ["id", "email", "first_name", "last_name"],
        "orders": ["id", "customer_id"],
        "coupons": ["id", "code", "amount", "date_expires"]
    }

    lista_dicionarios, erro = API.get_lista_itens(tabela)

    if erro:
        return f"Controller.listar_itens: ERRO! API.get_lista_itens: {erro}"
    
    if not lista_dicionarios:
        return f"Controller.listar_itens: ERRO! Itens não encontrados"

    resultado = ""

    if lista_dicionarios:
        for produto in lista_dicionarios:
            resultado += f"\nPRODUTO\n"
            for chave, valor in produto.items():
                if valor and chave in filtros_tabela[tabela]:
                    resultado += f"{chave} = {valor}\n"

    if resultado != "":
        return resultado
    else:
        return f"Controller.listar_itens: ERRO! Não foi possivel listar itens da tabela '{tabela}'"


def consultar_item(tabela, id):
    filtros_tabela = {
        "products": ["id", "name", "price", "description"],
        "customers": ["id", "email", "first_name", "last_name"],
        "orders": ["id", "customer_id"],
        "coupons": ["id", "code", "amount", "date_expires"]
    }

    dicionario_item, erro = API.get_item(tabela, id)

    if erro:
        return f"Controller.consultar_item: ERRO! API.get_item: {erro}"
    
    if not dicionario_item:
        return f"Controller.consultar_item: ERRO! Item não encontrado"

    resultado = ""

    if dicionario_item:
       
        for chave, valor in dicionario_item.items():
            if valor and chave in filtros_tabela[tabela]:
                resultado += f"{chave} = {valor}\n"

    if resultado != "":
        return resultado
    else:
        return f"Controller.consultar_item: ERRO! Não foi possivel consultar item de id '{id}'"
    
def salvar_login(dados):
    try:
        API.wcapi.url = dados[0]
        API.wcapi.consumer_key = dados[1]
        API.wcapi.consumer_secret = dados[2]
        Banco.Banco.salvar_login(dados)
        return "Login salvo"
    except Exception as e:
        return f"Controller.salvar_login: ERRO! {e}"
    
def carregar_login(dados):
    try:
        API.wcapi.url = dados[0]
        API.wcapi.consumer_key = dados[1]
        API.wcapi.consumer_secret = dados[2]
        return "Dados de login carregados com sucesso"
    except Exception as e:
        return f"Controller.carregar_login: ERRO! {e}"
