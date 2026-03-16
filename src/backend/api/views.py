from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from model import condominio, endereco, imovel, anuncio
from model import Init
from database.banco import Banco
import base64
from controller import controller
import logging


def _com_cors(resposta: JsonResponse) -> JsonResponse:
    resposta["Access-Control-Allow-Origin"] = "*"
    resposta["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resposta["Access-Control-Allow-Headers"] = "Content-Type"
    return resposta


@csrf_exempt
def getImovelPorId(request, id):
    if request.method == "OPTIONS":
        return _com_cors(JsonResponse({"status": "ok"}))
    if request.method == "GET":
        print(id)
        logging.info(f"Requisição para obter imóvel com ID: {id}")
        imovel_obj = Init.imobiliaria.get_imovel_por_id(int(id))
        print(imovel_obj)
        if imovel_obj:
            resposta = {
                "id": imovel_obj.get_id(),
                "valor_venda": imovel_obj.get_valor_venda(),
                "valor_condominio": imovel_obj.get_valor_condominio(),
                "valor_iptu": imovel_obj.get_iptu(),
                "valor_aluguel": imovel_obj.get_valor_aluguel(),
                "categoria": imovel_obj.get_categoria().value if imovel_obj.get_categoria() else None,
                "status": imovel_obj.get_status().value if imovel_obj.get_status() else None,
                "endereco": {
                    "rua": imovel_obj.get_endereco().rua,
                    "numero": imovel_obj.get_endereco().numero,
                    "bairro": imovel_obj.get_endereco().bairro,
                    "cidade": imovel_obj.get_endereco().cidade,
                    "uf": imovel_obj.get_endereco().uf,
                    "cep": imovel_obj.get_endereco().cep,
                    "complemento": imovel_obj.get_endereco().complemento,
                } if imovel_obj.get_endereco() else None,
                "anuncio": {
                    "id": imovel_obj.get_anuncio().get_id(),
                    "descricao": imovel_obj.get_anuncio().get_descricao(),
                    "titulo": imovel_obj.get_anuncio().get_titulo(),
                    "imagens": [
                        base64.b64encode(imagem.getvalue()).decode("utf-8")
                        for imagem in imovel_obj.get_anuncio().get_imagens()
                    ] if imovel_obj.get_anuncio() and imovel_obj.get_anuncio().get_imagens() else []
                } if imovel_obj.get_anuncio() else None,
            }
            return _com_cors(JsonResponse(resposta))
        else:
            return _com_cors(JsonResponse({"erro": "Imovel nao encontrado"}, status=404))
    return _com_cors(JsonResponse({"erro": "Metodo invalido"}, status=405))


@csrf_exempt
def cadastrar_imovel(request):
    if request.method == "OPTIONS":
        return _com_cors(JsonResponse({"status": "ok"}))

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return _com_cors(JsonResponse({"erro": "JSON invalido"}, status=400))

        id = int(data.get("ref")) if data.get("ref") else None
        nome_condominio = data.get("nome_condominio") if data.get(
            "nome_condominio") else None
        valor_venda = float(data.get("valor_venda", 0))
        valor_aluguel = float(data.get("valor_aluguel", 0))
        quant_quartos = int(data.get("quant_quartos", 0))
        quant_salas = int(data.get("quant_salas", 0))
        quant_vagas = int(data.get("quant_vagas", 0))
        quant_banheiros = int(data.get("quant_banheiros", 0))
        quant_varandas = int(data.get("quant_varandas", 0))
        categoria = imovel.Categoria(
            data.get("categoria")) if data.get("categoria") else None
        status = imovel.Status(
            data.get("status")) if data.get("status") else None
        iptu = float(data.get("iptu", 0))
        valor_condominio = float(data.get("valor_condominio", 0))
        andar = int(data.get("andar", 0))
        estado = imovel.Estado(
            data.get("estado")) if data.get("estado") else None
        bloco = data.get("bloco")
        ano_construcao = int(data.get("ano_construcao"))
        area_total = float(data.get("area_total", 0))
        area_privativa = float(data.get("area_privativa", 0))
        situacao = imovel.Situacao(
            data.get("situacao")) if data.get("situacao") else None
        ocupacao = imovel.Ocupacao(
            data.get("ocupacao")) if data.get("ocupacao") else None
        # proprietarios = data.get("proprietarios", [])
        # corretor = data.get("corretor")
        # captador = data.get("captador")
        cep = int(data.get("cep")) if data.get("cep") else None
        rua = data.get("rua") if data.get("rua") else None
        bairro = data.get("bairro") if data.get("bairro") else None
        cidade = data.get("cidade") if data.get("cidade") else None
        titulo = data.get("titulo") if data.get("titulo") else None
        descricao = data.get("descricao") if data.get("descricao") else None
        complemento = data.get("complemento") if data.get(
            "complemento") else None
        uf = data.get("uf") if data.get("uf") else None
        numero = int(data.get("numero")) if data.get("numero") else None
        anuncio_obj = anuncio.Anuncio()
        anuncio_obj.set_titulo(titulo)
        anuncio_obj.set_descricao(descricao)
        endereco_obj = endereco.Endereco(rua, bairro, cep, cidade, estado)
        endereco_obj.set_numero(numero)
        endereco_obj.set_complemento(complemento)
        endereco_obj.set_uf(uf)
        condominio_obj = condominio.Condominio(
            nome_condominio, endereco_obj)
        # imagens = anuncio.get("imagens", [])
        # imagens_bytes = []
        # for imagem in imagens:
        #     try:
        #         imagem_bytes = base64.b64decode(imagem)
        #         imagens_bytes.append(imagem_bytes)
        #     except (base64.binascii.Error, ValueError):
        #         continue
        # anuncio_obj.set_imagens(imagens_bytes)
        # condominio = data.get("condominio")
        # filtros = data.get("filtros", [])

        imovel_obj = None
        if id:
            imovel_obj = Init.imobiliaria.get_imovel_por_id(id)
        else:
            imovel_obj = imovel.Imovel(endereco_obj, status, categoria)

        imovel_obj.set_id(id)
        imovel_obj.set_valor_venda(valor_venda)
        imovel_obj.set_valor_aluguel(valor_aluguel)
        imovel_obj.set_quant_quartos(quant_quartos)
        imovel_obj.set_quant_salas(quant_salas)
        imovel_obj.set_quant_vagas(quant_vagas)
        imovel_obj.set_quant_banheiros(quant_banheiros)
        imovel_obj.set_quant_varandas(quant_varandas)
        imovel_obj.set_categoria(categoria)
        imovel_obj.set_endereco(endereco_obj)
        imovel_obj.set_status(status)
        imovel_obj.set_iptu(iptu)
        imovel_obj.set_valor_condominio(valor_condominio)
        imovel_obj.set_andar(andar)
        imovel_obj.set_estado(estado)
        imovel_obj.set_bloco(bloco)
        imovel_obj.set_ano_construcao(ano_construcao)
        imovel_obj.set_area_total(area_total)
        imovel_obj.set_area_privativa(area_privativa)
        imovel_obj.set_situacao(situacao)
        imovel_obj.set_ocupacao(ocupacao)
        # imovel_obj.set_corretor(corretor)
        # imovel_obj.set_captador(captador)
        imovel_obj.set_anuncio(anuncio_obj)
        imovel_obj.set_condominio(condominio_obj)

        if id:
            imovel_obj.set_data_modificacao(datetime.datetime.now())
            controller.editar_imovel(
                imovel_obj)
        else:
            controller.cadastrar_imovel(
                imovel_obj)

        return _com_cors(JsonResponse({"status": "ok"}))


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
def listar_atendimentos(request):
    if request.method == "OPTIONS":
        return _com_cors(JsonResponse({"status": "ok"}))
    
    atendimentos = Init.imobiliaria.get_lista_atendimentos()
    lista = []
    if atendimentos:
        for atendimento in atendimentos:
            lista.append({
                "id": atendimento.get_id(),
                "corretor": atendimento.get_corretor().get_nome() if atendimento.get_corretor() else None,
                "cliente": atendimento.get_cliente().get_nome() if atendimento.get_cliente() else None,
                "imovel": {
                    "id": atendimento.get_imovel().get_id(),
                    "titulo": atendimento.get_imovel().get_anuncio().get_titulo() if atendimento.get_imovel() and atendimento.get_imovel().get_anuncio() else None
                } if atendimento.get_imovel() else None,
                "status": atendimento.get_status().value if atendimento.get_status() else None
            })
    return _com_cors(JsonResponse(lista, safe=False))
    

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
