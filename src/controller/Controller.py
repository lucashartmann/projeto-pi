from model import Cliente, Corretor, Init, Captador
import datetime


def cadastrar_atendimento(atendimento):
    cadastro = Init.imobiliaria.cadastrar_atendimento(atendimento)

    if cadastro:
        return "Atendimento pedido com sucesso"
    else:
        return "ERRO ao cadastrar atendimento"


def remover(dado, tabela):

    remocao = Init.imobiliaria.remover(dado, tabela)

    if remocao == True:
        return f"'{tabela.upper()} - {dado}' removida com sucesso"
    else:
        return f"ERRO ao remover '{tabela} - {dado}'"



def editar_usuario(cpf_pesquisa,
                   nome, email, telefone, data_nascimento, cpf, rg):
    gerente = Init.imobiliaria.get_gerente_por_cpf(cpf_pesquisa)
    if not gerente:
        return f"Gerente com CPF {cpf_pesquisa} não encontrado"

    if nome != "" or nome is not None:
        gerente.set_nome(nome)
    if email != "" or email is not None:
        gerente.set_email(email)
    if telefone != "" or telefone is not None:
        gerente.set_telefone(telefone)
    if data_nascimento != "" or data_nascimento is not None:
        gerente.set_data_nascimento(data_nascimento)
    if cpf != "" or cpf is not None:
        gerente.set_cpf_cnpj(cpf)
    if rg != "" or rg is not None:
        gerente.set_rg(rg)

    atualizado = Init.imobiliaria.atualizar_gerente(gerente)

    if atualizado != True:
        return f"ERRO ao atualizar gerente {atualizado[1]}"
    return f"Gerente editado com sucesso\n {gerente}"


def editar_proprietario(cpf_pesquisa,
                        nome, email, telefone, data_nascimento, cpf, rg):
    proprietario = Init.imobiliaria.get_proprietario_por_cpf(cpf_pesquisa)
    if not proprietario:
        return f"Proprietario com CPF {cpf_pesquisa} não encontrado"

    if nome != "" or nome is not None:
        proprietario.set_nome(nome)
    if email != "" or email is not None:
        proprietario.set_email(email)
    if telefone != "" or telefone is not None:
        proprietario.set_telefone(telefone)
    if data_nascimento != "" or data_nascimento is not None:
        proprietario.set_data_nascimento(data_nascimento)
    if cpf != "" or cpf is not None:
        proprietario.set_cpf_cnpj(cpf)
    if rg != "" or rg is not None:
        proprietario.set_rg(rg)
    proprietario.set_endereco(None)
    atualizado = Init.imobiliaria.atualizar_proprietario(proprietario)

    if atualizado != True:
        return f"ERRO ao atualizar proprietario {atualizado[1]}"
    return f"Proprietario editado com sucesso\n {proprietario}"


def cadastrar_proprietario(nome, email, telefone, data_nascimento, cpf, rg):
    proprietario = Cliente.Proprietario(
        nome, cpf, rg, telefone,  email)
    proprietario.set_data_nascimento(data_nascimento)

    cadastrado = Init.imobiliaria.cadastrar_proprietario(proprietario)

    if cadastrado:
        return f"Proprietario cadastrado!\n {proprietario}"
    else:
        return "ERRO"



def cadastrar_usuario(nome, email, telefone, data_nascimento, cpf, rg):
    comprador = Cliente.Comprador(
        nome, cpf, rg, telefone, email)
    comprador.set_data_nascimento(data_nascimento)

    cadastrado = Init.imobiliaria.cadastrar_comprador(comprador)

    if cadastrado:
        return f"Comprador cadastrado!\n {comprador}"
    else:
        return "ERRO"


def cadastrar_imovel(imovel):
     
    if imovel.get_id() != "" and imovel.get_id() is not None and imovel.get_id() >= 0:
            imovel_encontrado = Init.imobiliaria.get_estoque().get_imovel_por_codigo(imovel.get_id())
            if imovel_encontrado:
                edicao = Init.imobiliaria.get_estoque().atualizar_imovel(imovel)
                # Init.imobiliaria.atualizar_anuncio()
                # Init.imobiliaria.atualizar_endereco()
                # Init.imobiliaria.atualizar_condominio()
                
                if edicao:
                    
                    return f"Imóvel editado com sucesso!"
                else:
                    return "ERRO ao editar imóvel"
    else:
        

        consultar_endereco = Init.imobiliaria.verificar_endereco(imovel.get_endereco())

        endereco = None

        if consultar_endereco:
            endereco = consultar_endereco
        else:
            cadastro_endereco = Init.imobiliaria.cadastrar_endereco(
                imovel.get_endereco())
            if cadastro_endereco:
                endereco = Init.imobiliaria.verificar_endereco(imovel.get_endereco())

        if not endereco:
            return "ERRO! Problema com o endereço"
        else:
            imovel.get_endereco().set_id(endereco.get_id())
            consultar_condominio = Init.imobiliaria.get_condominio_por_id_endereco(endereco.get_id())
            
            if not consultar_condominio:
                cadastrar = Init.imobiliaria.cadastrar_condominio(imovel.get_condominio())
                if cadastrar:
                    consultar_condominio = Init.imobiliaria.get_condominio_por_id_endereco(endereco.get_id())
                    if consultar_condominio:
                        imovel.set_condominio(consultar_condominio)
                    else:
                        imovel.set_condominio(None)
            else:
                imovel.set_condominio(consultar_condominio)
        
            cadastro_anuncio = Init.imobiliaria.get_estoque().cadastrar_anuncio(
                imovel.get_anuncio())
            if cadastro_anuncio != False:
                imovel.get_anuncio().set_id(cadastro_anuncio)
            imovel.set_data_cadastro(datetime.datetime.now())
            cadastrado = Init.imobiliaria.get_estoque().cadastrar_imovel(imovel)
            if cadastrado == True:
                return f"imovel cadastrado!\n"
            else:
                return "ERRO: ao cadastrar_imovel"


def verificar_login(username, senha):
    username = username
    senha = senha

    consulta = Init.imobiliaria.verificar_usuario(
        username, senha)

    if consulta:
        Init.usuario_atual = consulta
        return "Login realizado com sucesso"
    else:
        return "ERRO"


def salvar_login(username, senha, email):
    um_usuario = Cliente.Cliente(
        nome="", cpf="", rg="", telefone="", email="")

    um_usuario.set_username(username)
    um_usuario.set_senha(senha)
    um_usuario.set_email(email)

    consulta = Init.imobiliaria.cadastrar_usuario(um_usuario)

    if consulta:
        Init.usuario_atual = um_usuario
        return "Cadastro realizado com sucesso"
    else:
        return "ERRO. Tente Novamente"
