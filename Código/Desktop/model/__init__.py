from model import Cliente, Loja, Produto, Cupom, Reembolso, Relatorio, Pedido, Usuario

class Init:

    usuario = ""
    cliente_atual = None
    loja = Loja.Loja("GameStart", "00000000000")

    um_produto = Produto.Produto(
                "PLAYSTATION 5", "SONY", "SLIM", "PRETO", 3000.00, 10, "CONSOLE")
    um_cliente = Cliente.Cliente("MARCOS", "11111111111", "11111111111",
                                       "11111111111", "RUA 1", "MARCOS@GMAIL.COM")
    um_pedido = Pedido.Pedido()
    um_cupom = Cupom.Cupom("qwdsadas")
    um_reembolso = Reembolso.Reembolso()
    um_relatorio = Relatorio.Relatorio()
  

    dict_objetos = {
        "products": um_produto, "orders": um_pedido,  "customers": um_cliente, "coupons": um_cupom,  "refunds": um_reembolso, "reports": um_relatorio
    }

    def inicializar():
        
            
        if not Init.loja.get_lista_usuarios():
            admin = Usuario.Usuario("admin", "admin", "admin", "administrador")
            gerente = Usuario.Usuario("gerente", "gerente", "gerente", "gerente")
            funcionario = Usuario.Usuario("funcionario", "funcionario", "funcionario", "funcionario")
            cliente = Usuario.Usuario("cliente", "cliente", "cliente", "cliente")

            Init.loja.cadastrar_usuario(admin)
            Init.loja.cadastrar_usuario(gerente)
            Init.loja.cadastrar_usuario(funcionario)
            Init.loja.cadastrar_usuario(cliente)

        if not Init.loja.get_lista_clientes():

          
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

            Init.loja.cadastrar(cliente3)
            Init.loja.cadastrar(cliente2)
            Init.loja.cadastrar(cliente4)
            Init.loja.cadastrar(cliente5)
            Init.loja.cadastrar(cliente6)
            Init.loja.cadastrar(cliente7)
            Init.loja.cadastrar(cliente8)
            Init.loja.cadastrar(cliente9)
            Init.loja.cadastrar(cliente10)

        if not Init.loja.get_estoque().get_lista_produtos():

          
            produto2 = Produto.Produto("XBOX SERIES X", "MICROSOFT",
                                       "SLIM", "PRETO", 4000.00, 10, "CONSOLE")
            produto3 = Produto.Produto("NINTENDO SWITCH", "NINTENDO",
                                       "SLIM", "PRETO", 3000.00, 10, "CONSOLE")
            produto4 = Produto.Produto("GEFORCE RTX 3080 TI", "NVIDIA",
                                       "TI", "BRANCO", 2000.00, 3, "PLACA DE VIDEO")
            produto5 = Produto.Produto(
                "RX 6900 XT", "AMD", "60 SERIES", "BRANCO", 1000.00, 3, "PLACA DE VIDEO")
            produto6 = Produto.Produto("GEFORCE RTX 3090", "NVIDIA",
                                       "30 SERIES", "BRANCO", 1000.00, 3, "PLACA DE VIDEO")
            produto7 = Produto.Produto(
                "DUALSHOCK 4", "SONY", "SLIM", "PRETO", 200.00, 10, "PERIFÉRICOS")
            produto9 = Produto.Produto(
                "VOLANTE GAMER", "LOGITECH", "G29", "PRETO", 500.00, 5, "PERIFÉRICOS")
            produto10 = Produto.Produto(
                "MOUSE GAMER", "LOGITECH", "G502", "PRETO", 100.00, 10, "PERIFÉRICOS")
            produto11 = Produto.Produto(
                "PLAYSTATION 5", "SONY", "PRO", "BRANCO", 6000.00, 30, "CONSOLE")

            Init.loja.get_estoque().adicionar_produto(produto2)
            Init.loja.get_estoque().adicionar_produto(produto3)
            Init.loja.get_estoque().adicionar_produto(produto4)
            Init.loja.get_estoque().adicionar_produto(produto5)
            Init.loja.get_estoque().adicionar_produto(produto6)
            Init.loja.get_estoque().adicionar_produto(produto7)
            Init.loja.get_estoque().adicionar_produto(produto9)
            Init.loja.get_estoque().adicionar_produto(produto10)
            Init.loja.get_estoque().adicionar_produto(produto11)
