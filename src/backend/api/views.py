import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from model import Init
import base64


def _com_cors(resposta: JsonResponse) -> JsonResponse:
    resposta["Access-Control-Allow-Origin"] = "*"
    resposta["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resposta["Access-Control-Allow-Headers"] = "Content-Type"
    return resposta


@csrf_exempt
def deslogar(request):
    if request.method == "OPTIONS":
        return _com_cors(JsonResponse({"status": "ok"}))

    if request.method == "POST":
        Init.usuario_atual = None
        return _com_cors(JsonResponse({"status": "ok"}))

    return _com_cors(JsonResponse({"erro": "Metodo invalido"}, status=405))


@csrf_exempt
def carregar_usuario(request):
    if request.method == "OPTIONS":
        return _com_cors(JsonResponse({"status": "ok"}))

    if request.method == "GET":
        if Init.usuario_atual:
            return _com_cors(JsonResponse({
                "tipo": Init.usuario_atual.tipo.value if Init.usuario_atual.tipo else None
            }))
        return _com_cors(JsonResponse({"erro": "Usuario nao encontrado"}, status=404))

    return _com_cors(JsonResponse({"erro": "Metodo invalido"}, status=405))


@csrf_exempt
def verificar_login(request):
    if request.method == "OPTIONS":
        return _com_cors(JsonResponse({"status": "ok"}))

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return _com_cors(JsonResponse({"erro": "JSON invalido"}, status=400))

        usuario = data.get("usuario")
        senha = data.get("senha")

        consulta = Init.imobiliaria.verificar_usuario(usuario, senha)

        if consulta:
            Init.usuario_atual = consulta
            return _com_cors(JsonResponse({"status": "ok"}))
        return _com_cors(JsonResponse({"status": "erro"}, status=401))

    return _com_cors(JsonResponse({"erro": "Metodo invalido"}, status=405))


@csrf_exempt
def listar_imoveis(request):
    if request.method == "OPTIONS":
        return _com_cors(JsonResponse({"status": "ok"}))

    if request.method == "GET":

        imoveis = Init.imobiliaria.get_estoque().get_lista_imoveis_disponiveis()
        lista = []

        if imoveis:
            for imovel in imoveis:
                lista.append({
                    "id": imovel.get_id(),
                    "valor_venda": imovel.get_valor_venda(),
                    "valor_aluguel": imovel.get_valor_aluguel(),
                    "categoria": imovel.get_categoria().value if imovel.get_categoria() else None,
                    "status": imovel.get_status().value if imovel.get_status() else None,
                    "endereco": {
                        "rua": imovel.get_endereco().rua,
                        "numero": imovel.get_endereco().numero,
                        "bairro": imovel.get_endereco().bairro,
                        "cidade": imovel.get_endereco().cidade,
                        "uf": imovel.get_endereco().uf,
                        "cep": imovel.get_endereco().cep,
                        "complemento": imovel.get_endereco().complemento,
                    } if imovel.get_endereco() else None,
                    "anuncio": {
                        "id": imovel.get_anuncio().get_id(),
                        "descricao": imovel.get_anuncio().get_descricao(),
                        "titulo": imovel.get_anuncio().get_titulo(),
                        "imagens": [
                            base64.b64encode(imagem.getvalue()).decode("utf-8")
                            for imagem in imovel.get_anuncio().get_imagens()
                        ] if imovel.get_anuncio() and imovel.get_anuncio().get_imagens() else []
                    } if imovel.get_anuncio() else None,
                })

        return _com_cors(JsonResponse(lista, safe=False))

    return _com_cors(JsonResponse({"erro": "Metodo invalido"}, status=405))
