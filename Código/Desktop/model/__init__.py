from model import Cliente, Imobiliaria, Imovel, Venda_Aluguel, Usuario, Corretor, Captador


class Init:

    um_imovel = Imovel.Imovel()
    uma_venda_aluguel = Venda_Aluguel.Venda_Aluguel()
    usuario_atual = ""

    comprador = Cliente.Comprador("MARCOS", "11111111111", "11111111111",
                                  "11111111111", "RUA 1", "MARCOS@GMAIL.COM")

    proprietario = Cliente.Proprietario("MARCOS", "11111111111", "11111111111",
                                        "11111111111", "RUA 1", "MARCOS@GMAIL.COM")

    captador = Captador.Captador(
        "lucas", "00000000000", "00000000", "00000000000", "bento", "lucas@email")

    corretor = Corretor.Corretor(
        "lucas", "00000000000", "00000000", "00000000000", "bento", "lucas@email")

    dict_objetos = {
        "imovel": um_imovel,  "comprador": comprador, "proprietario": proprietario, "captador": captador, "corretor": corretor, "venda_aluguel": uma_venda_aluguel
    }

    imobiliaria = Imobiliaria.Imobiliaria("GameStart", "00000000000")

    def inicializar():

        if not Init.imobiliaria.get_lista_compradores():

            cliente2 = Cliente.Comprador("PEDRO", "22222222222", "22222222222",
                                         "22222222222", "RUA 2", "PEDRO@GMAIL.COM")

            cliente4 = Cliente.Comprador("JOÃO", "44444444444", "44444444444",
                                         "44444444444", "RUA 4", "JOAO@GMAIL.COM")

            cliente6 = Cliente.Comprador("MARIA", "66666666666", "66666666666",
                                         "66666666666", "RUA 6", "MARIA@GMAIL.COM")

            cliente8 = Cliente.Comprador("JOANA", "88888888888", "88888888888",
                                         "88888888888", "RUA 8", "JOANA@GMAIL.COM")

            cliente10 = Cliente.Comprador("FERNANDA", "10101010101", "10101010101",
                                          "10101010101", "RUA 10", "FERNANDA@GMAIL.COM")

        if not Init.imobiliaria.get_lista_proprietarios():

            cliente3 = Cliente.Proprietario("JULIA", "33333333333", "33333333333",
                                            "33333333333", "RUA 3", "JULIA@GMAIL.COM")

            cliente5 = Cliente.Proprietario("ANDRESSA", "55555555555", "55555555555",
                                            "55555555555", "RUA 5", "ANDRESSA@GMAIL.COM")

            cliente7 = Cliente.Proprietario("ANA", "77777777777", "77777777777",
                                            "77777777777", "RUA 7", "ANA@GMAIL.COM")

            cliente9 = Cliente.Proprietario("GABRIELA", "99999999999", "99999999999",
                                            "99999999999", "RUA 9", "GABRIELA@GMAIL.COM")

            Init.imobiliaria.cadastrar_proprietario(cliente3)
            Init.imobiliaria.cadastrar_proprietario(cliente2)
            Init.imobiliaria.cadastrar_proprietario(cliente4)
            Init.imobiliaria.cadastrar_proprietario(cliente5)
            Init.imobiliaria.cadastrar_proprietario(cliente6)
            Init.imobiliaria.cadastrar_proprietario(cliente7)
            Init.imobiliaria.cadastrar_proprietario(cliente8)
            Init.imobiliaria.cadastrar_proprietario(cliente9)
            Init.imobiliaria.cadastrar_proprietario(cliente10)

        if not Init.imobiliaria.get_estoque().get_lista_imovels():

            imovel2 = Imovel.Imovel()
            imovel3 = Imovel.Imovel()
            imovel4 = Imovel.Imovel()
            imovel5 = Imovel.Imovel()
            imovel6 = Imovel.Imovel()
            imovel7 = Imovel.Imovel()

            # with open(r"assets/imovel.png", "rb") as img:
            #     img_bytes = img.read()

            # imovel2.set_imagem(img_bytes)
            # imovel3.set_imagem(img_bytes)
            # imovel7.set_imagem(img_bytes)

            imovel9 = Imovel.Imovel()
            imovel10 = Imovel.Imovel()
            imovel11 = Imovel.Imovel()

            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel2)
            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel3)
            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel4)
            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel5)
            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel6)
            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel7)
            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel9)
            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel10)
            Init.imobiliaria.get_estoque().cadastrar_imovel(imovel11)
