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
                    "id": imovel.id,
                    "valor_venda": imovel.valor_venda,
                    "valor_aluguel": imovel.valor_aluguel,
                    "categoria": imovel.categoria.value if imovel.categoria else None,
                    "status": imovel.status.value if imovel.status else None,
                    "endereco": {
                        "rua": imovel.endereco.rua,
                        "numero": imovel.endereco.numero,
                        "bairro": imovel.endereco.bairro,
                        "cidade": imovel.endereco.cidade,
                        "uf": imovel.endereco.uf,
                        "cep": imovel.endereco.cep,
                        "complemento": imovel.endereco.complemento,
                    } if imovel.endereco else None,
                    "anuncio": {
                        "id" : imovel.anuncio.id,
                        "descricao" : imovel.anuncio.descricao,
                        "titulo" : imovel.anuncio.titulo,
                        "imagens": [
                            base64.b64encode(imagem.getvalue()).decode("utf-8")
                            for imagem in imovel.anuncio.imagens
                        ] if imovel.anuncio and imovel.anuncio.imagens else []
                    } if imovel.anuncio else None,
                })

        return _com_cors(JsonResponse(lista, safe=False))

    return _com_cors(JsonResponse({"erro": "Metodo invalido"}, status=405))
