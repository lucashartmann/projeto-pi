### Ideias:
- Fazer o sistema de realizar compra para o cliente ou fazer o sistema de cadastrar/realizar venda para o admin?
- Fazer o programa ser para cliente e admin ou só o admin?
- Criar classe Venda() ou Pedido()?

### Falta fazer:
####  App:
- Implementar opção de remover produto do carrinho
- Falta implementar opção do cliente procurar produtos por nome, marca, categoria e etc, ou ver todos os produtos
#### Loja e App:
- Implementar sistema de pagamento (cartão, juros, parcelas, etc) (nota fiscal/recibo)
#### Loja:
- Implementar numero_vendas, get_numero_vendas() (mensal, anual, semanal, diaria)
#### Fornecedor/Funcionario/Cliente:
- Ver qual é a diferença dessas classes. Se não tiver diferença, então remover elas

# Modelagem: 
## Pessoa
- Atributos:
    - nome
    - cpf/cnpj
    - rg
    - telefone 
    - endereco
    - email
- Métodos:
    - get_cpf(self)
## Cliente
- Atributos:
    - super()
- Métodos:
## Fornecedor
- Atributos:
    - super()
- Métodos:
## Funcionario
- Atributos:
    - super()
- Métodos:
## Produto
- Atributos:
    - nome
    - codigo
    - cor
    - preco 
    - marca 
    - modelo
    - quantidade
- Métodos:
## Estoque
- Atributos:
    - podutos
    - quantidade
- Métodos:
    - adicionar_produto(self, produto)
    - remover_produto(self, produto)
    - listar_produtos(self)
    - get_quantidade(self)
    - consultar_produtos_por_nome(nome)
## Loja
- Atributos:
    - nome
    - cnpj
    - Estoque 
    - funcionarios
    - clientes
    - fornecedores
    - quantidade_funcionarios
    - quantidade_clientes
    - quantidade_fornecedores
    - faturamento
- Métodos:
    - realizar_compra(cliente, produto)
    - adicionar_funcionario(self, funcionario)
    - adicionar_cliente(self, cliente)
    - adicionar_fornecedor(self, fornecedor)
    - remover_funcionario(self, funcionario)
    - remover_cliente(self, cliente)
    - remover_fornecedor(self, fornecedor)
    - get_quantidade_funcionarios(self)
    - get_quantidade_clientes(self)
    - get_quantidade_fornecedores(self)
    - get_faturamento(self)
    - is_cliente_cadastrado(self, cpf)
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