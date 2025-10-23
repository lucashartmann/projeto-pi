from model import Cliente, Loja, Produto, Cupom, Taxa, Reembolso, Relatorio, Pedido
from api import API
from database import Banco


class Init:
    usuario = ""
    cliente_atual = None
    loja = Loja.Loja("GameStart", "00000000000")

    um_produto = Produto.Produto()
    um_cliente = Cliente.Cliente("asds")
    um_pedido = Pedido.Pedido()
    um_cupom = Cupom.Cupom("qwdsadas")
    uma_taxa = Taxa.Taxa()
    um_reembolso = Reembolso.Reembolso()
    um_relatorio = Relatorio.Relatorio()

    dict_objetos = {
        "products": um_produto, "orders": um_pedido,  "customers": um_cliente, "coupons": um_cupom,   "taxes": uma_taxa,  "refunds": um_reembolso, "reports": um_relatorio
    }

    # if not loja.get_lista_clientes():

    #     cliente1 = Cliente.Cliente("MARCOS", "11111111111", "11111111111",
    #                                "11111111111", "RUA 1", "MARCOS@GMAIL.COM")
    #     cliente2 = Cliente.Cliente("PEDRO", "22222222222", "22222222222",
    #                                "22222222222", "RUA 2", "PEDRO@GMAIL.COM")
    #     cliente3 = Cliente.Cliente("JULIA", "33333333333", "33333333333",
    #                                "33333333333", "RUA 3", "JULIA@GMAIL.COM")
    #     cliente4 = Cliente.Cliente("JOÃO", "44444444444", "44444444444",
    #                                "44444444444", "RUA 4", "JOAO@GMAIL.COM")
    #     cliente5 = Cliente.Cliente("ANDRESSA", "55555555555", "55555555555",
    #                                "55555555555", "RUA 5", "ANDRESSA@GMAIL.COM")
    #     cliente6 = Cliente.Cliente("MARIA", "66666666666", "66666666666",
    #                                "66666666666", "RUA 6", "MARIA@GMAIL.COM")
    #     cliente7 = Cliente.Cliente("ANA", "77777777777", "77777777777",
    #                                "77777777777", "RUA 7", "ANA@GMAIL.COM")
    #     cliente8 = Cliente.Cliente("JOANA", "88888888888", "88888888888",
    #                                "88888888888", "RUA 8", "JOANA@GMAIL.COM")
    #     cliente9 = Cliente.Cliente("GABRIELA", "99999999999", "99999999999",
    #                                "99999999999", "RUA 9", "GABRIELA@GMAIL.COM")
    #     cliente10 = Cliente.Cliente("FERNANDA", "10101010101", "10101010101",
    #                                 "10101010101", "RUA 10", "FERNANDA@GMAIL.COM")

    #     loja.cadastrar(cliente1)
    #     loja.cadastrar(cliente2)
    #     loja.cadastrar(cliente3)
    #     loja.cadastrar(cliente4)
    #     loja.cadastrar(cliente5)
    #     loja.cadastrar(cliente6)
    #     loja.cadastrar(cliente7)
    #     loja.cadastrar(cliente8)
    #     loja.cadastrar(cliente9)
    #     loja.cadastrar(cliente10)

    # if not loja.get_estoque().get_lista_produtos():

    #     produto1 = Produto.Produto(
    #         "PLAYSTATION 5", "SONY", "SLIM", "PRETO", 3000.00, 10, "CONSOLE")
    #     produto2 = Produto.Produto("XBOX SERIES X", "MICROSOFT",
    #                                "SLIM", "PRETO", 4000.00, 10, "CONSOLE")
    #     produto3 = Produto.Produto("NINTENDO SWITCH", "NINTENDO",
    #                                "SLIM", "PRETO", 3000.00, 10, "CONSOLE")
    #     produto4 = Produto.Produto("GEFORCE RTX 3080 TI", "NVIDIA",
    #                                "TI", "BRANCO", 2000.00, 3, "PLACA DE VIDEO")
    #     produto5 = Produto.Produto(
    #         "RX 6900 XT", "AMD", "60 SERIES", "BRANCO", 1000.00, 3, "PLACA DE VIDEO")
    #     produto6 = Produto.Produto("GEFORCE RTX 3090", "NVIDIA",
    #                                "30 SERIES", "BRANCO", 1000.00, 3, "PLACA DE VIDEO")
    #     produto7 = Produto.Produto(
    #         "DUALSHOCK 4", "SONY", "SLIM", "PRETO", 200.00, 10, "PERIFÉRICOS")
    #     produto9 = Produto.Produto(
    #         "VOLANTE GAMER", "LOGITECH", "G29", "PRETO", 500.00, 5, "PERIFÉRICOS")
    #     produto10 = Produto.Produto(
    #         "MOUSE GAMER", "LOGITECH", "G502", "PRETO", 100.00, 10, "PERIFÉRICOS")
    #     produto11 = Produto.Produto(
    #         "PLAYSTATION 5", "SONY", "PRO", "BRANCO", 6000.00, 30, "CONSOLE")

    #     loja.get_estoque().adicionar_produto(produto1)
    #     loja.get_estoque().adicionar_produto(produto2)
    #     loja.get_estoque().adicionar_produto(produto3)
    #     loja.get_estoque().adicionar_produto(produto4)
    #     loja.get_estoque().adicionar_produto(produto5)
    #     loja.get_estoque().adicionar_produto(produto6)
    #     loja.get_estoque().adicionar_produto(produto7)
    #     loja.get_estoque().adicionar_produto(produto9)
    #     loja.get_estoque().adicionar_produto(produto10)
    #     loja.get_estoque().adicionar_produto(produto11)
    
    def inicializar():

        dados = Banco.Banco.carregar_login()
        if dados:
            API.wcapi.url = dados[0]
            API.wcapi.consumer_key = dados[1]
            API.wcapi.consumer_secret = dados[2]

            if len(API.get_lista_itens("customers")) < 1:

                data = {
                    "email": "lucas@email.com",
                    "first_name": "Lucas",
                    "last_name": "Bastos",
                    "username": "ddelux19"
                }

                print(API.adicionar("customers", data))

                data = {
                    "email": "MARCOS@GMAIL.COM",
                    "first_name": "MARCOS",
                    "last_name": "",
                    "username": "MARCOS"
                }

                print(API.adicionar("customers", data))

                data = {
                    "email": "PEDRO@GMAIL.COM",
                    "first_name": "PEDRO",
                    "last_name": "",
                    "username": "PEDRO"
                }

                print(API.adicionar("customers", data))

                data = {
                    "email": "JULIA@GMAIL.COM",
                    "first_name": "JULIA",
                    "last_name": "",
                    "username": "JULIA"
                }

                print(API.adicionar("customers", data))

                # print(API.get_lista_itens("customers"))

            if len(API.get_lista_itens("coupons")) < 1:

                data = {
                    "email": "free shipping",
                    "first_name": "0.00",
                    "last_name": "fixed_cart",
                }

                print(API.adicionar("coupons", data))

                # print(API.get_lista_itens("coupons"))

            if len(API.get_lista_itens("products")) < 1:

                data = {
                    "name": "PLAYSTATION 5 PRO",
                    "regular_price": "3000.0",
                    "stock_quantity": "10"
                }

                print(API.adicionar("products", data))

                data = {
                    "name": "XBOX SERIES X",
                    "regular_price": "4000.0",
                    "stock_quantity": "10"
                }

                print(API.adicionar("products", data))

                data = {
                    "name": "NINTENDO SWITCH",
                    "regular_price": "3000.0",
                    "stock_quantity": "10"
                }

                print(API.adicionar("products", data))

                data = {
                    "name": "GEFORCE RTX 3080 TI",
                    "regular_price": "2000.0",
                    "stock_quantity": "3"
                }

                print(API.adicionar("products", data))

                # print(API.get_lista_itens("products"))

            if len(API.get_lista_itens("orders")) < 1:

                data = {
                    "status": "processing",
                    "customer_id": "271481149",
                    "currency": "BRL"
                }

                print(API.adicionar("orders", data))

                # print(API.get_lista_itens("orders"))
