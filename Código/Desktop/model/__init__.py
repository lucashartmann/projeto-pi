from model import Cliente, Imobiliaria, Imovel, Cupom, Reembolso, Relatorio, Pedido, Usuario, Corretor, Captador


class Init:

    um_pedido = Pedido.Pedido()
    um_cupom = Cupom.Cupom("qwdsadas")
    um_reembolso = Reembolso.Reembolso()
    um_relatorio = Relatorio.Relatorio()
    um_imovel = Imovel.Imovel()
    
    usuario_atual = ""
    
    cliente = Cliente.Comprador("MARCOS", "11111111111", "11111111111",
                                 "11111111111", "RUA 1", "MARCOS@GMAIL.COM")
    
    captador = Captador.Captador("lucas", "00000000000", "00000000", "00000000000", "bento", "lucas@email")

    corretor = Corretor.Corretor("lucas", "00000000000", "00000000", "00000000000", "bento", "lucas@email")
    
    dict_objetos = {
        "imovel": um_imovel, "pedido": um_pedido,  "cliente": cliente, "cupom": um_cupom,   "reembolso": um_reembolso, "relatorio": um_relatorio, "captador": captador, "corretor": corretor,
    }


    imobiliaria = Imobiliaria.Imobiliaria("GameStart", "00000000000")

    def inicializar():

        if not Init.imobiliaria.get_lista_usuarios():
            admin = Usuario.Usuario(
                "admin", "admin", "admin")
            corretor = Corretor.Corretor()
            captador = Captador.Captador()
            cliente = Cliente.Cliente()

            Init.imobiliaria.cadastrar_usuario(admin)
            Init.imobiliaria.cadastrar_usuario(corretor)
            Init.imobiliaria.cadastrar_usuario(captador)
            Init.imobiliaria.cadastrar_usuario(cliente)

        if not Init.imobiliaria.get_lista_clientes():

            cliente2 = Cliente.Cliente("PEDRO", "22222222222", "22222222222",
                                       "22222222222", "RUA 2", "PEDRO@GMAIL.COM")
            cliente3 = Cliente.Cliente("JULIA", "33333333333", "33333333333",
                                       "33333333333", "RUA 3", "JULIA@GMAIL.COM")
            cliente4 = Cliente.Cliente("JOÃO", "44444444444", "44444444444",
                                       "44444444444", "RUA 4", "JOAO@GMAIL.COM")
            cliente5 = Cliente.Cliente("ANDRESSA", "55555555555", "55555555555",
                                       "55555555555", "RUA 5", "ANDRESSA@GMAIL.COM")
            cliente6 = Cliente.Cliente("MARIA", "66666666666", "66666666666",
                                       "66666666666", "RUA 6", "MARIA@GMAIL.COM")
            cliente7 = Cliente.Cliente("ANA", "77777777777", "77777777777",
                                       "77777777777", "RUA 7", "ANA@GMAIL.COM")
            cliente8 = Cliente.Cliente("JOANA", "88888888888", "88888888888",
                                       "88888888888", "RUA 8", "JOANA@GMAIL.COM")
            cliente9 = Cliente.Cliente("GABRIELA", "99999999999", "99999999999",
                                       "99999999999", "RUA 9", "GABRIELA@GMAIL.COM")
            cliente10 = Cliente.Cliente("FERNANDA", "10101010101", "10101010101",
                                        "10101010101", "RUA 10", "FERNANDA@GMAIL.COM")

            Init.imobiliaria.cadastrar(cliente3)
            Init.imobiliaria.cadastrar(cliente2)
            Init.imobiliaria.cadastrar(cliente4)
            Init.imobiliaria.cadastrar(cliente5)
            Init.imobiliaria.cadastrar(cliente6)
            Init.imobiliaria.cadastrar(cliente7)
            Init.imobiliaria.cadastrar(cliente8)
            Init.imobiliaria.cadastrar(cliente9)
            Init.imobiliaria.cadastrar(cliente10)

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

            Init.imobiliaria.get_estoque().adicionar_imovel(imovel2)
            Init.imobiliaria.get_estoque().adicionar_imovel(imovel3)
            Init.imobiliaria.get_estoque().adicionar_imovel(imovel4)
            Init.imobiliaria.get_estoque().adicionar_imovel(imovel5)
            Init.imobiliaria.get_estoque().adicionar_imovel(imovel6)
            Init.imobiliaria.get_estoque().adicionar_imovel(imovel7)
            Init.imobiliaria.get_estoque().adicionar_imovel(imovel9)
            Init.imobiliaria.get_estoque().adicionar_imovel(imovel10)
            Init.imobiliaria.get_estoque().adicionar_imovel(imovel11)
