#### Falta fazer:

- Melhorar pagamento
- Usar Try e Expect
- Implementar Shelve

#### model/Loja:

- Implementar get número/quantidade de vendas no dia, semana, mês, ano. get faturamento no dia, semana, mês, ano.

#### model/Fornecedor/Funcionario/Cliente:

- Ver qual é a diferença dessas classes. Se não tiver diferença, então remover elas

#### model/Produto e Pessoa:

- Separar view, model e controller em editar_campo()

#### controller/Controller:

- Melhorar mensagens de erro

#### view/TelaEstoque e view/TelaClientela:

- Permitir filtrar mais, ex: "marca: SONY MiCROSOFT"
- Filtragem não ta funcionando com espaços, ex: "endereco RUA 1"

# Modelagem:

## Pessoa

- Atributos:
  - nome
  - cpf
  - rg
  - telefone
  - endereco
  - email
- Métodos:
  - editar_campo(self, nome_campo, setter)
  - get_nome(self)
  - get_rg(self)
  - get_telefone(self)
  - get_endereco(self)
  - get_email(self)
  - get_cpf(self)
  - set_nome(self, nome)
  - set_cpf(self, cpf)
  - set_rg(self, rg)
  - set_telefone(self, telefone)
  - set_endereco(self, endereco)
  - set_email(self, email)

## Cliente

- Atributos:
  - super()
  - isCadastrado
- Métodos:
  - get_is_cadastrado(self)
  - set_is_cadastrado(self, isCadastrado)
  - get_carrinho(self)
  - **str**(self)

## Fornecedor

- Atributos:
  - super()
- Métodos:
  - **str**(self)

## Funcionario

- Atributos:
  - super()
- Métodos:
  - **str**(self)

## Produto

- Atributos:
  - id
  - nome
  - codigo
  - cor
  - preco
  - marca
  - modelo
  - quantidade
- Métodos:
  - editar_campo(self, nome_campo, setter)
  - get_quantidade(self)
  - get_nome(self)
  - get_codigo(self)
  - get_marca(self)
  - get_modelo(self)
  - get_cor(self)
  - get_preco(self)
  - get_id(self)
  - set_nome(self, nome)
  - set_cor(self, cor)
  - set_preco(self, preco)
  - set_marca(self, marca)
  - set_modelo(self, modelo)
  - set_quantidade(self, quantidade)
  - **str**(self)

## Estoque

- Atributos:
  - podutos[]
- Métodos:
  - adicionar_produto(self, produto)
  - remover_produto(self, produto)
  - get_lista_produtos(self)
  - verifica_produto(self, produto)
  - get_produtos_por_nome(self, nome)
  - get_produtos_por_marca(self, marca)
  - get_produtos_por_modelo(self, modelo)
  - get_produtos_por_categoria(self, categoria)
  - get_produto_por_id(self, id)
  - get_quantidade_produto_por_marca(self, marca)
  - get_quantidade_produto_por_modelo(self, modelo)
  - get_quantidade_produto_por_categoria(self, categoria)
  - get_quantidade_produtos(self)

## Loja

- Atributos:
  - nome
  - cnpj
  - Estoque
  - pessoas[]
  - quantidade_funcionarios
  - quantidade_clientes
  - quantidade_fornecedores
  - faturamento
- Métodos:
  - cadastrar(self, pessoa)
  - remover(self, pessoa)
  - set_quantidade(self)
  - get_estoque(self)
  - get_nome(self)
  - get_cnpj(self)
  - get_quantidade_funcionarios(self)
  - get_quantidade_clientes(self)
  - get_quantidade_fornecedores(self)
  - get_faturamento(self)
  - get_cliente_por_cpf(self, cpf)
  - get_produto_por_id(self, id)
  - is_cpf_cadastrado(self, cpf)
  - is_rg_cadastrado(self, rg)
  - is_telefone_cadastrado(self, telefone)

## Venda

- Atributos:
  - cliente
  - itens[]
  - modo_pagamento
  - parcelas
  - total
- Métodos:
  - calcular_total(self)
  - aplicar_venda(self, loja)
  - gerar_recibo(self, loja)

## Carrinho

- Atributos:
  - itens[]
- Métodos:
  - adicionar_produto(self, produto, quantidade)
  - remover_produto_por_id(self, id_produto)
  - listar_produtos(self)
  - esta_vazio(self)
  - limpar(self)
  - get_total(self)

## App:

Administrador cadastra produtos, funcionários, fornecedores<br/>
Admin consulta o estoque onde pode cadastrar produtos, editar produtos, ver quantidade de certo produto por categoria, marca, nome, remover produto<br/>
Admin consulta os dados onde pode ver o faturamento da loja, a quantidade de produtos, clientes, fornecedores e funcionários.

Quando se acessa a Kabum pelo site, o usuário pode ver os produtos, e se cadastrar como cliente. Mas não tem opção de se cadastrar como admin ou funcionário. Isso deve ser do sistema interno da loja.

Para realizar a venda o administrador precisa dizer qual cliente comprou, quais produtos foram compradas (lista de produtos), e diminuir ou remover esses produtos do estoque.
admin -> cadastrar_venda(cliente, lista_produtos)

Para realizar a compra o cliente precisa adicionar um ou mais produtos ao carrinho, e depois selecionar se quiser finalizar a compra. Entao a loja recebe o pedido de compra que é passado para o funcionario ou admin. Esse pedido contem o valor total dos produtos, quais produtos (lista de produtos), estimativa de entrega (prazo), valor da entrega<br/>
cliente -> adicionar_produto_carrinho(produto)<br/>
cliente -> realizar_compra(lista_produtos) ou gera_pedido_compra()<br/>
Criar classe Venda() ou Pedido()?<br/>
admin, funcionario -> receber_pedido_compra(pedido)<br/>
admin, funcionario -> realiza_compra ou gera_recibo()<br/>
cliente -> receber_recibo() e dados da compra (data_entrega, valor_total, produtos_comprados)

# Explicações:

A loja não tem vendedores, e sim fornecedores.
