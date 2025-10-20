from api import API
from database import Banco

def adicionar_item(tabela, dados: dict):
    if tabela == "customers" and "name" in dados.keys():

        nome_split = dados["name"].split()
        

        if len(nome_split) > 1:
            dados["first_name"] = " ".join(nome for nome in nome_split[:-1])
            dados["last_name"] = nome_split[-1]
            del dados["name"]
        else:
            dados["first_name"] = dados["name"]
            del dados["name"]
    
    if tabela == "orders":
        consulta, erro = API.get_item("customers", dados["customer_id"])

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