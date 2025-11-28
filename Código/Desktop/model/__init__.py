from model import Cliente, Imobiliaria, Imovel, Venda_Aluguel, Endereco, Corretor, Captador, Administrador
from model.Imovel import Categoria, Status
from database import Banco

class Init:
    
    banco = Banco.Banco()

    endereco1 = Endereco.Endereco(
        "Avenida Bento Gonçalves", 205, "Partenon", "90650002")

    um_imovel = Imovel.Imovel(
        endereco1, Status.VENDA, Categoria.APARTAMENTO)
    uma_venda_aluguel = Venda_Aluguel.Venda_Aluguel()
    usuario_atual = ""

    administrador = Administrador.Administrador(
        "asdasdas", "asdasdas", "asdasdas")

    comprador = Cliente.Comprador("MARCOS", "11111111111", "11111111111",
                                  "11111111111", "MARCOS@GMAIL.COM")

    proprietario = Cliente.Proprietario("MARCOS", "11111111111", "11111111111",
                                        "11111111111", "MARCOS@GMAIL.COM")

    captador = Captador.Captador(
        "lucas", "00000000000", "00000000", "00000000000", "bento", "lucas@email")

    corretor = Corretor.Corretor(
        "lucas", "00000000000", "00000000", "00000000000", "bento", "lucas@email")

    dict_objetos = {
        "imovel": um_imovel,  "comprador": comprador, "proprietario": proprietario, "captador": captador, "corretor": corretor, "venda_aluguel": uma_venda_aluguel
    }

    imobiliaria = Imobiliaria.Imobiliaria("GameStart", "00000000000")

    def inicializar():


            cliente2 = Cliente.Comprador("PEDRO", "22222222222", "22222222222",
                                         "22222222222", "PEDRO@GMAIL.COM")

            cliente4 = Cliente.Comprador("JOÃO", "44444444444", "44444444444",
                                         "44444444444",  "JOAO@GMAIL.COM")

            cliente6 = Cliente.Comprador("MARIA", "66666666666", "66666666666",
                                         "66666666666", "MARIA@GMAIL.COM")

            cliente8 = Cliente.Comprador("JOANA", "88888888888", "88888888888",
                                         "88888888888", "JOANA@GMAIL.COM")

            cliente10 = Cliente.Comprador("FERNANDA", "10101010101", "10101010101",
                                          "10101010101", "FERNANDA@GMAIL.COM")
            
            Init.imobiliaria.cadastrar_comprador(cliente2)
            Init.imobiliaria.cadastrar_comprador(cliente4)
            Init.imobiliaria.cadastrar_comprador(cliente10)
            Init.imobiliaria.cadastrar_comprador(cliente8)
            Init.imobiliaria.cadastrar_comprador(cliente6)


            cliente3 = Cliente.Proprietario("JULIA", "33333333333", "33333333333",
                                            "33333333333", "JULIA@GMAIL.COM")

            cliente5 = Cliente.Proprietario("ANDRESSA", "55555555555", "55555555555",
                                            "55555555555", "ANDRESSA@GMAIL.COM")

            cliente7 = Cliente.Proprietario("ANA", "77777777777", "77777777777",
                                            "77777777777", "ANA@GMAIL.COM")

            cliente9 = Cliente.Proprietario("GABRIELA", "99999999999", "99999999999",
                                            "99999999999", "GABRIELA@GMAIL.COM")

            Init.imobiliaria.cadastrar_proprietario(cliente3)
            
         
            Init.imobiliaria.cadastrar_proprietario(cliente5)
            Init.imobiliaria.cadastrar_proprietario(cliente7)
            Init.imobiliaria.cadastrar_proprietario(cliente9)

       

            endereco1 = Endereco.Endereco(
                "Avenida Bento Gonçalves", 205, "Partenon", "90650002")
            
            resultado = Init.banco.cadastrar_endereco(endereco1)
            
            print(resultado)
            endereco1.set_id(resultado)

            imovel2 = Imovel.Imovel(
                endereco1, Status.VENDA, Categoria.APARTAMENTO)
            
            imovel3 = Imovel.Imovel(
                endereco1, Status.VENDA, Categoria.APARTAMENTO)
            
            imagens = [r"assets\apartamento1\5661162882.jpg", r"assets\apartamento2\5661211031.jpg"]
            
            imovel2.set_imagens(imagens)
            imovel3.set_imagens(imagens)
        
            
            resultado = Init.imobiliaria.get_estoque().cadastrar_imovel(imovel2)
            print(resultado)
            resultado = Init.imobiliaria.get_estoque().cadastrar_imovel(imovel3)
            print(resultado)
            
            with open(r"assets\apartamento1\5661162882.jpg", 'rb') as file:
                binary_data = file.read()
                
            
            
            resultado = Init.banco.cadastrar_anexo(1, binary_data, "Imagem")
            print(resultado)
            
            resultado = Init.banco.cadastrar_anexo(2, binary_data, "Imagem")
            print(resultado)
            
            
            
            with open(r"assets\apartamento2\5661211031.jpg", 'rb') as file:
                binary_data2 = file.read()
                
            resultado = Init.banco.cadastrar_anexo(2, binary_data2, "Imagem")
            print(resultado)
                
            resultado = Init.banco.cadastrar_anexo(1, binary_data2, "Imagem")
            print(resultado)
            
            
           
            

            # imovel3 = Imovel.Imovel()
            # imovel4 = Imovel.Imovel()
            # imovel5 = Imovel.Imovel()
            # imovel6 = Imovel.Imovel()
            # imovel7 = Imovel.Imovel()

            # # with open(r"assets/imovel.png", "rb") as img:
            # #     img_bytes = img.read()

            # # imovel2.set_imagem(img_bytes)
            # # imovel3.set_imagem(img_bytes)
            # # imovel7.set_imagem(img_bytes)

            # imovel9 = Imovel.Imovel()
            # imovel10 = Imovel.Imovel()
            # imovel11 = Imovel.Imovel()

            # Init.imobiliaria.get_estoque().cadastrar_imovel(imovel2)
            # Init.imobiliaria.get_estoque().cadastrar_imovel(imovel3)
            # Init.imobiliaria.get_estoque().cadastrar_imovel(imovel4)
            # Init.imobiliaria.get_estoque().cadastrar_imovel(imovel5)
            # Init.imobiliaria.get_estoque().cadastrar_imovel(imovel6)
            # Init.imobiliaria.get_estoque().cadastrar_imovel(imovel7)
            # Init.imobiliaria.get_estoque().cadastrar_imovel(imovel9)
            # Init.imobiliaria.get_estoque().cadastrar_imovel(imovel10)
            
           