# Concessionária ou loja de artigos variados

# loja de eletronicos 

## Responder
- What (O que será feito)
    - ..
- Why (Por que será feito)
    - ..
- Where (onde será feito?)
    - ..
- When (quando será feito?)
    - ..
- Who (por quem será feito?)
    - ..
- How (como será feito?)
    - ..
- How much (quanto vai custar?)
    - ..

## Classes: 
- Vendedor
    - Alguém que deseja vender na plaforma
    - Dados: nome, CPF, dados bancários, data de nascimento (precisa ter no minimo 18 anos) 
- Comprador
    - Alguém que deseja comprar na plaforma
    - Dados: nome, CPF, dados bancários, data de nascimento (precisa ter no minimo 18 anos) 
- Loja
    - Armanezamento de clientes, vendedores e produtos 
    - Dados: nome
- Main
    - Inicializa App
- App 
    - Parte central do código onde os métodos são chamados
- Produto
    - Dados: nome, código, cor, valor, marca

## Métodos:
- negociacao : -> Loja 
- editarCliente :  -> Loja ou Cliente 
- cadastrarCliente(Cliente cliente) : boolean -> Loja ou Cliente 
- cadastrarVendedor(Vendedor vendedor) : boolean -> Loja ou  Vendedor
- editarVendedor : -> Loja ou Vendedor
- cadastrarProduto : boolean -> Loja ou Produto
- editarProduto : -> Loja ou Produto
- removerCliente : boolean -> Loja ou Cliente
- removerProduto : boolean -> Loja ou Produto
- removerVendedor : boolean -> Loja ou Vendedor
- consultarClientePorNome(String nome) : Cliente -> Loja

## Pensamentos:
Frete grátis 

Cupons de desconto 

5% de comissao para a loja, resto para o vendedor 

Apenas produtos nacionais 

Produtos mais vendidos 

Login

Tela compatibilidade pc

Tela de retorno de produto. O site pede o tipo de produto, quanto tempo foi usado, estipula um desconto e gera um ticket para o produto ser retornado
