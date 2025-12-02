from model import Cliente, Corretor, Init
import datetime


def cadastrar_atendimento(atendimento):
    cadastro = Init.imobiliaria.cadastrar_atendimento(atendimento)

    if cadastro:
        return "Atendimento pedido com sucesso"
    else:
        return "ERRO ao cadastrar atendimento"


def cadastrar_pessoa(lista):
    if lista[0] == "":
        return "Nome está vazio"

    if lista[1] == "":
        return "CPF está vazio"
    if lista[2] == "":
        return "RG está vazio"
    if lista[3] == "":
        "TELEFONE está vazio"

    if lista[4] == "":
        return "Endereco está vazio"

    if lista[5] == "":
        return "Email está vazio"

    if lista[-1] == "Cliente":
        pessoa = Cliente.Cliente(lista[0], lista[1], lista[2],
                                 lista[3], lista[4], lista[5])
    else:
        pessoa = Corretor.Funcionario(lista[0], lista[1], lista[2],
                                      lista[3], lista[4], lista[5])

    cadastrado = Init.imobiliaria.cadastrar(pessoa)

    if cadastrado:
        return f"Pessoa cadastrado!\n {pessoa}"
    else:
        return "ERRO"


def cadastrar_imovel(imovel):

    consultar_endereco = Init.imobiliaria.verificar_endereco(
        imovel.get_endereco())

    id_endereco = None

    if consultar_endereco:
        id_endereco = consultar_endereco.get_id()
    else:
        cadastro_endereco = Init.imobiliaria.cadastrar_endereco(
            imovel.get_endereco())
        if cadastro_endereco != False:
            id_endereco = cadastro_endereco

    if id_endereco == None:
        return "ERRO! Problema com o endereço"
    else:
        imovel.get_endereco().set_id(id_endereco)
        if imovel.get_id() >= 0:
            imovel = Init.imobiliaria.get_estoque().get_imovel_por_codigo(imovel.get_id())
            if imovel:
                edicao = Init.imobiliaria.get_estoque().atualizar_imovel(imovel)

                if edicao:
                    return f"Imóvel editado com sucesso!"
                else:
                    return "ERRO ao editar imóvel"

            else:
                imovel.set_data_cadastro(datetime.datetime.now)
                cadastrado = Init.imobiliaria.get_estoque().cadastrar_imovel(imovel)

                if cadastrado == True:
                    return f"imovel cadastrado!\n"
                else:
                    return "ERRO: ao cadastrar_imovel"


def editar_pessoa(cpf, dados):

    if dados[-1] == "Cliente":
        pessoa = Init.imobiliaria.get_cliente_por_cpf(cpf)
    else:
        pessoa = Init.imobiliaria.get_funcionario_por_cpf(cpf)

    if not pessoa:
        return f"Pessoa com CPF {cpf} não encontrado"

    if dados[0] != "":
        pessoa.set_nome(dados[0])
    if dados[1] != "":
        pessoa.set_cpf(dados[1])
    if dados[2] != "":
        pessoa.set_rg(dados[2])
    if dados[3] != "":
        pessoa.set_telefone(dados[3])
    if dados[4] != "":
        pessoa.set_endereco(dados[4])
    if dados[5] != "":
        pessoa.set_email(dados[5])

    return f"Pessoa editado com sucesso\n {pessoa}"


def remover_comprador(cpf):

    comprador = Init.imobiliaria.get_comprador_por_cpf(cpf)

    if not comprador:
        return f"Comprador com CPF {cpf} não encontrado"

    remocao = Init.imobiliaria.remover_comprador(comprador)

    if remocao == True:
        return f"Comprador removido com sucesso"
    else:
        return "ERRO"


def remover_corretor(cpf):

    corretor = Init.imobiliaria.get_corretor_por_cpf(cpf)

    if not corretor:
        return f"corretor com CPF {cpf} não encontrado"

    remocao = Init.imobiliaria.remover_corretor(corretor)

    if remocao == True:
        return f"corretor removido com sucesso"
    else:
        return "ERRO"


def remover_captador(cpf):

    captador = Init.imobiliaria.get_captador_por_cpf(cpf)

    if not captador:
        return f"captador com CPF {cpf} não encontrado"

    remocao = Init.imobiliaria.remover_comprador(captador)

    if remocao == True:
        return f"captador removido com sucesso"
    else:
        return "ERRO"


def remover_proprietario(cpf):

    proprietario = Init.imobiliaria.get_proprietario_por_cpf(cpf)

    if not proprietario:
        return f"proprietario com CPF {cpf} não encontrado"

    remocao = Init.imobiliaria.remover_proprietario(proprietario)

    if remocao == True:
        return f"proprietario removido com sucesso"
    else:
        return "ERRO"


def atualizar_dado_cliente(dados):
    username = dados[0].split()
    nome = dados[1]
    novo_cpf = dados[2].split()
    rg = dados[3].split()
    telefone = dados[4].split()
    endereco = dados[5]
    email = dados[6].split()
    senha = dados[7].split()

    cpf = Init.cliente_atual.get_cpf_cnpj()

    mensagem = []

    if not cpf:
        return f"Cliente com CPF {cpf} não encontrado"

    if nome and nome != Init.cliente_atual.get_nome():

        atualizacao = Init.imobiliaria.atualizar_dado_cliente(
            cpf, "nome", nome)

        if atualizacao != True:
            mensagem += f"ERRO ao atualizar nome {atualizacao[1]}"
        else:
            mensagem += f"Nome atualizado com sucesso"
            Init.cliente_atual.set_nome(nome)

    elif novo_cpf and novo_cpf != cpf:

        atualizacao = Init.imobiliaria.atualizar_dado_cliente(
            cpf, "cpf", novo_cpf)
        cpf = novo_cpf

        if atualizacao != True:
            mensagem += f"ERRO ao atualizar CPF {atualizacao[1]}"
        else:
            mensagem += f"CPF atualizado com sucesso"
            Init.cliente_atual.set_cpf(novo_cpf)

    elif rg and rg != Init.cliente_atual.get_rg():

        atualizacao = Init.imobiliaria.atualizar_dado_cliente(
            cpf, "rg", rg)

        if atualizacao != True:
            mensagem += f"ERRO ao atualizar RG {atualizacao[1]}"
        else:
            mensagem += f"RG atualizado com sucesso"
            Init.cliente_atual.set_rg(rg)

    elif telefone and telefone != Init.cliente_atual.get_telefone():

        atualizacao = Init.imobiliaria.atualizar_dado_cliente(
            cpf, "telefone", telefone)

        if atualizacao != True:
            mensagem += f"ERRO ao atualizar telefone {atualizacao[1]}"
        else:
            mensagem += f"Telefone atualizado com sucesso"
            Init.cliente_atual.set_telefone(telefone)

    elif endereco and endereco != Init.cliente_atual.get_endereco():

        atualizacao = Init.imobiliaria.atualizar_dado_cliente(
            cpf, "endereco", endereco)

        if atualizacao != True:
            mensagem += f"ERRO ao atualizar endereco {atualizacao[1]}"
        else:
            mensagem += f"Endereço atualizado com sucesso"
            Init.cliente_atual.set_endereco(endereco)

    elif email and email != Init.cliente_atual.get_email():

        atualizacao = Init.imobiliaria.atualizar_dado_cliente(
            cpf, "email", email)

        if atualizacao != True:
            mensagem += f"ERRO ao atualizar email {atualizacao[1]}"
        else:
            mensagem += f"Email atualizado com sucesso"
            Init.cliente_atual.set_email(email)

    return mensagem


def remover_imovel(id_imovel):
    imovel = Init.imobiliaria.get_estoque().get_imovel_por_codigo(id_imovel)

    if not imovel:
        return "ERRO"

    remocao = Init.imobiliaria.get_estoque().remover_imovel(imovel)

    if remocao == True:
        return f"imovel removido com sucesso"
    else:
        return "ERRO"


def verificar_login(username, senha, tipo_usuario):
    username = username
    senha = senha
    tipo_usuario = tipo_usuario

    consulta = Init.imobiliaria.verificar_usuario(
        username, senha, tipo_usuario)

    if consulta:
        Init.usuario_atual = consulta
        return "Login realizado com sucesso"
    else:
        return "ERRO"


def salvar_login(username, senha, email):
    um_usuario = Cliente.Comprador(
        nome="", cpf="", rg="", telefone="", email="")

    um_usuario.set_username(username)
    um_usuario.set_senha(senha)
    um_usuario.set_email(email)

    consulta = Init.imobiliaria.cadastrar_comprador(um_usuario)

    if consulta:
        Init.usuario_atual = um_usuario
        return "Cadastro realizado com sucesso"
    else:
        return "ERRO. Tente Novamente"
