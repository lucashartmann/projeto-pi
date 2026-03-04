import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from model import Init


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
