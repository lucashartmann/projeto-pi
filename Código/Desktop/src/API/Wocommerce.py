from woocommerce import API

wcapi = API(
    url="https://sualoja.com",
    consumer_key="ck_xxxxxxxxxxxxxxxxxxxxxx",
    consumer_secret="cs_xxxxxxxxxxxxxxxxxxxxxx",
    version="wc/v3"
)


def adicionar(tabela, dados: dict):
    try:
        resposta = wcapi.post(tabela, dados).json()
        if "code" in resposta:
            print("ERRO da API ao adicionar!", resposta)
            return False, resposta
        else:
            if resposta:
                return True, ""
            else:
                print("ERRO da API ao adicionar!", resposta)
                return False, ""
    except Exception as e:
        print("ERRO ao adicionar!", e)
        return False, e


def remover(tabela, id):
    try:
        resposta = wcapi.delete(f"{tabela}/{id}").json()
        if resposta:
            return True, ""
    except Exception as e:
        print("ERRO ao remover!", e)
        return False, e


def atualizar(tabela, id, tipo_dado, novo_valor):
    try:
        novo_dado = {
            tipo_dado: novo_valor
        }

        resposta = wcapi.put(f"{tabela}/{id}", novo_dado).json()
        if resposta:
            return True, ""
        else:
            print("ERRO da API ao atualizar!", resposta)
            return False, ""
    except Exception as e:
        print("ERRO ao atualizar!", e)
        return False, e


def get_lista_itens(tabela):
    try:
        lista_de_dicionarios = wcapi.get(tabela).json()
        return lista_de_dicionarios, ""
    except Exception as e:
        return [], e


def get_item(tabela, id):
    try:
        lista_de_dicionarios = wcapi.get(f"{tabela}/{id}").json()
        if "code" in lista_de_dicionarios:
            print("ERRO da API ao consultar!", lista_de_dicionarios)
            return [], ""
        else:
            if lista_de_dicionarios:
                return lista_de_dicionarios, ""
            else:
                print("ERRO da API ao consultar!", lista_de_dicionarios)
                return [], ""
    except Exception as e:
        print("ERRO ao consultar!", e)
        return [], e
