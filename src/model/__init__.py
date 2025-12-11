from model import Cliente, Imobiliaria, Imovel, Venda_Aluguel, Endereco, Corretor, Captador, Anuncio, Gerente, Usuario, Proprietario


class Init:

    imobiliaria = Imobiliaria.Imobiliaria("GameStart", "00000000000")
    usuario_atual = ""

    filtros_imovel = ["Aceita Pet", "Churrasqueira", "Armarios Embutidos", "Cozinha Americana", "Área de Serviço", "Suíte Master",
                      "Banheiro com Janela", "Piscina", "Lareira", "Ar Condicionado", "Semi Mobiliado", "Mobiliado", "Dependência de Empregada", "Despensa", "Depósito"]

    filtros_condominio = ["Churrasqueira Coletiva", "Piscina", "Piscina Infantil", "Piscina Aquecida", "Quiosque", "Sauna", "Quadra de Esportes", "Jardim", "Salão de Festas", "Academia", "Sala de Jogos", "Playground", "Brinquedoteca", "Vaga Coberta",
                          "Estacionamento", "Vaga para Visitantes", "Mercado", "Mesa de Sinuca", "Mesa de Ping Pong", "Mesa de Pebolim", "Quadra de Tenis", "Quadra de Futebol", "Quadra de Basquete", "Quadra de Volei", "Quadra de Areia", "Bicicletario", "Heliponto", "Elevador de Serviço"]

    imobiliaria.cadastrar_lista_filtros(filtros_imovel, "filtros_imovel")

    imobiliaria.cadastrar_lista_filtros(
        filtros_condominio, "filtros_condominio")

    administrador = Usuario.Usuario(username="administrador", senha="123", email="admin@example.com",
                                    nome="Lucas", cpf_cnpj="00000000000", tipo=Usuario.Tipo.ADMINISTRADOR)
    administrador_dois = Usuario.Usuario(username="admin2", senha="123", email="admin2@example.com",
                                         nome="Felipe", cpf_cnpj="11111111111", tipo=Usuario.Tipo.ADMINISTRADOR)
    gerente = Gerente.Gerente(username="gerente", senha="123", email="gerente@example.com",
                              nome="Pedro", cpf_cnpj="22222222222")
    gerente_dois = Gerente.Gerente(username="gerente2", senha="123", email="gerente2@example.com",
                                   nome="Rosangela", cpf_cnpj="33333333333")
    comprador = Cliente.Cliente(username="cliente", senha="123", email="cliente@example.com",
                                nome="Marcela", cpf_cnpj="44444444444")
    comprador_dois = Cliente.Cliente(username="cliente2", senha="123", email="cliente2@example.com",
                                     nome="Rute Dois", cpf_cnpj="77777777777")
    captador = Captador.Captador(username="captador", senha="123", email="captador@example.com",
                                 nome="Ana", cpf_cnpj="55555555555")
    captador_dois = Captador.Captador(username="captador2", senha="123", email="captador2@example.com",
                                      nome="Ana Dois", cpf_cnpj="88888888888")
    corretor = Corretor.Corretor(username="corretor", senha="123", email="corretor@example.com",
                                 nome="João", cpf_cnpj="66666666666", creci="123456")
    corretor_dois = Corretor.Corretor(username="corretor2", senha="123", email="corretor2@example.com",
                                      nome="Elisabeth", cpf_cnpj="99999999999", creci="654321")

    if not imobiliaria.get_lista_usuarios():

        imobiliaria.cadastrar_usuario(administrador)
        imobiliaria.cadastrar_usuario(gerente)
        imobiliaria.cadastrar_usuario(comprador)
        imobiliaria.cadastrar_usuario(captador)
        imobiliaria.cadastrar_usuario(corretor)
        imobiliaria.cadastrar_usuario(administrador_dois)
        imobiliaria.cadastrar_usuario(gerente_dois)
        imobiliaria.cadastrar_usuario(comprador_dois)
        imobiliaria.cadastrar_usuario(captador_dois)
        imobiliaria.cadastrar_usuario(corretor_dois)

    proprietario = Proprietario.Proprietario(email="proprietario@example.com",
                                             nome="Maria", cpf_cnpj="00000000000")

    proprietario_dois = Proprietario.Proprietario(email="proprietario2@example.com",
                                                  nome="Joaquim", cpf_cnpj="11111111111")

    if not imobiliaria.get_lista_proprietarios():

        imobiliaria.cadastrar_proprietario(proprietario_dois)
        imobiliaria.cadastrar_proprietario(proprietario)

    endereco = Endereco.Endereco(
        rua="Rua A", bairro="Centro", cep=12345678, cidade="Cidade X", uf="Estado Y")
    endereco.set_numero("123")

    endereco_dois = Endereco.Endereco(
        rua="Rua B", bairro="Bairro Z", cep=87654321, cidade="Cidade W", uf="Estado V")
    endereco_dois.set_numero("456")

    if not imobiliaria.get_lista_enderecos():
        cadastro = imobiliaria.cadastrar_endereco(endereco)
        cadastro_dois = imobiliaria.cadastrar_endereco(endereco_dois)
    consulta = None
    consulta_dois = None

    consulta = imobiliaria.verificar_endereco(endereco)
    imovel_um = Imovel.Imovel(
        endereco=consulta, status=Imovel.Status.VENDA, categoria=Imovel.Categoria.APARTAMENTO)
    imovel_dois = Imovel.Imovel(
        endereco=consulta, status=Imovel.Status.ALUGUEL, categoria=Imovel.Categoria.APARTAMENTO)
    imovel_tres = Imovel.Imovel(
        endereco=consulta, status=Imovel.Status.VENDIDO, categoria=Imovel.Categoria.LOFT)
    if not imobiliaria.get_estoque().get_lista_imoveis():
        imobiliaria.get_estoque().cadastrar_imovel(imovel_um)
        imobiliaria.get_estoque().cadastrar_imovel(imovel_dois)
        imobiliaria.get_estoque().cadastrar_imovel(imovel_tres)

    consulta_dois = imobiliaria.verificar_endereco(endereco_dois)
    imovel_quatro = Imovel.Imovel(
        endereco=consulta_dois, status=Imovel.Status.PENDENTE, categoria=Imovel.Categoria.TERRENO)
    imovel_cinco = Imovel.Imovel(
        endereco=consulta_dois, status=Imovel.Status.VENDA_ALUGUEL, categoria=Imovel.Categoria.CASA)
    if not imobiliaria.get_estoque().get_lista_imoveis():
        imobiliaria.get_estoque().cadastrar_imovel(imovel_quatro)
        imobiliaria.get_estoque().cadastrar_imovel(imovel_cinco)
