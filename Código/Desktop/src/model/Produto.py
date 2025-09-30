from datetime import datetime

class Produto:

    def __init__(self, nome, marca, modelo, cor, preco, quantidade, categoria):
        self.id = 0
        self.nome = nome
        self.cor = cor
        self.preco = preco
        self.marca = marca
        self.modelo = modelo
        self.quantidade = quantidade
        self.categoria = categoria

    def editar_campo(self, nome_campo, setter):
        while True:
            novo_valor = input(f"Digite o novo {nome_campo}: ").upper()
            validacao = len(novo_valor) > 0
            if validacao:
                setter(novo_valor)
                print(f"{nome_campo} atualizado com sucesso!\n")
                break
            print(f"{nome_campo} inválido!")

    def get_quantidade(self):
        return self.quantidade

    def get_nome(self):
        return self.nome

    def get_categoria(self):
        return self.categoria

    def get_marca(self):
        return self.marca

    def get_modelo(self):
        return self.modelo

    def get_cor(self):
        return self.cor

    def get_preco(self):
        return self.preco

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def set_nome(self, nome):
        self.nome = nome

    def set_categoria(self, categoria):
        self.categoria = categoria

    def set_cor(self, cor):
        self.cor = cor

    def set_preco(self, preco):
        self.preco = preco

    def set_marca(self, marca):
        self.marca = marca

    def set_modelo(self, modelo):
        self.modelo = modelo

    def set_quantidade(self, quantidade):
        self.quantidade = quantidade

    def __str__(self):
        return (f"Produto [id = {self.get_id()}, nome = {self.get_nome()}, marca = {self.get_marca()}, modelo = {self.get_modelo()}, cor = {self.get_cor()}, "
                f"preco = {self.get_preco()}, quantidade = {self.get_quantidade()}, categoria = {self.get_categoria()}]")

class Produto:
    def __init__(self):
        self.name	= "" #	Product name.
        self.slug	= "" #	Product slug.
        self.type	= "" #	Product type. Options: simple, grouped, external and variable. Default is simple.
        self.status	= "" #	Product status (post status). Options: draft, pending, private and publish. Default is publish.
        self.featured	= False #	Featured product. Default is false.
        self.catalog_visibility	= "" #	Catalog visibility. Options: visible, catalog, search and hidden. Default is visible.
        self.description	= "" #	Product description.
        self.short_description	= "" #	Product short description.
        self.sku	= "" #	Unique identifier.
        self.global_unique_id	= "" #	GTIN, UPC, EAN or ISBN - a unique identifier for each distinct product and service that can be purchased.
        self.regular_price	= "" #	Product regular price.
        self.sale_price	= "" #	Product sale price.
        self.date_on_sale_from = datetime(2025,1,1) #	Start date of sale price, in the site's timezone.
        self.date_on_sale_from_gmt = datetime(2025,1,1) #	Start date of sale price, as GMT.
        self.date_on_sale_to = datetime(2025,1,1) #	End date of sale price, in the site's timezone.
        self.date_on_sale_to_gmt = datetime(2025,1,1) #	End date of sale price, as GMT.
        self.virtual	= False #	If the product is virtual. Default is false.
        self.downloadable	= False #	If the product is downloadable. Default is false.
        self.downloads = [] #	List of downloadable files. See Product - Downloads properties
        self.download_limit	= 0 #	Number of times downloadable files can be downloaded after purchase. Default is -1.
        self.download_expiry	= 0 #	Number of days until access to downloadable files expires. Default is -1.
        self.external_url	= "" #	Product external URL. Only for external products.
        self.button_text	= "" #	Product external button text. Only for external products.
        self.tax_status	= "" #	Tax status. Options: taxable, shipping and none. Default is taxable.
        self.tax_class	= "" #	Tax class.
        self.manage_stock	= False #	Stock management at product level. Default is false.
        self.stock_quantity	= 0 #	Stock quantity.
        self.stock_status	= "" #	Controls the stock status of the product. Options: instock, outofstock, onbackorder. Default is instock.
        self.backorders	= "" #	If managing stock, this controls if backorders are allowed. Options: no, notify and yes. Default is no.
        self.sold_individually	= False #	Allow one item to be bought in a single order. Default is false.
        self.weight	= "" #	Product weight.
        self.dimensions:object	# Product dimensions. See Product - Dimensions properties
        self.shipping_class	= "" #	Shipping class slug.
        self.reviews_allowed	= False #	Allow reviews. Default is true.
        self.upsell_ids = [] #	List of up-sell products IDs.
        self.cross_sell_ids = [] #	List of cross-sell products IDs.
        self.parent_id	= 0 #	Product parent ID.
        self.purchase_note	= "" #	Optional note to send the customer after purchase.
        self.categories = [] #	List of categories. See Product - Categories properties
        self.tags = [] #	List of tags. See Product - Tags properties
        self.images = [] #	List of images. See Product - Images properties
        self.attributes = [] #	List of attributes. See Product - Attributes properties
        self.default_attributes = [] #	Defaults variation attributes. See Product - Default attributes properties
        self.grouped_products = [] #	List of grouped products ID.
        self.menu_order	= 0 #	Menu order, used to custom sort products.
        self.meta_data = [] #	Meta data. See Product - Meta data properties
        self.__id	= 0 #	Unique identifier for the resource.read-only
        self.__permalink	= "" #	Product URL.read-only
        self.__date_created	= datetime(2025,1,1) #	The date the product was created, in the site's timezone.read-only
        self.__date_created_gmt	= datetime(2025,1,1) #	The date the product was created, as GMT.read-only
        self.__date_modified	= datetime(2025,1,1) #	The date the product was last modified, in the site's timezone.read-only
        self.__date_modified_gmt	= datetime(2025,1,1) #	The date the product was last modified, as GMT.read-only
        self.__price	= "" #	Current product price.read-only
        self.__price_html	= "" #	Price formatted in HTML.read-only
        self.__on_sale	= False #	Shows if the product is on sale.read-only
        self.__purchasable	= False #	Shows if the product can be bought.read-only
        self.__total_sales	= 0 #	Amount of sales.read-only
        self.__backorders_allowed	= False #	Shows if backorders are allowed.read-only
        self.__backordered	= False #	Shows if the product is on backordered.read-only
        self.__shipping_required	= False #	Shows if the product need to be shipped.read-only
        self.__shipping_taxable	= False #	Shows whether or not the product shipping is taxable.read-only
        self.__shipping_class_id	= 0 #	Shipping class ID.read-only
        self.__average_rating	= "" #	Reviews average rating.read-only
        self.__rating_count	= 0 #	Amount of reviews that the product have.read-only
        self.__related_ids	= [] #	List of related products IDs.read-only
        self.__variations	= [] #	List of variations IDs.read-only