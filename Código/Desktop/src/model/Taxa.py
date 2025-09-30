class Taxa:

    def __init__(self):
        self.country = "" # Country ISO 3166 code. See ISO 3166 Codes (Countries) for more details
        self.state = ""  # State code.
        self.postcode = "" # Postcode/ZIP, it doesn't support multiple values. Deprecated as of WooCommerce 5.3, postcodes should be used instead.
        self.city = "" # City name, it doesn't support multiple values. Deprecated as of WooCommerce 5.3, postcodes should be used instead.
        self.postcodes = "" # [] Postcodes/ZIPs. Introduced in WooCommerce 5.3.
        self.cities = ""  # [] City names. Introduced in WooCommerce 5.3.
        self.rate = ""  # Tax rate.
        self.name = ""  # Tax rate name.
        self.priority = 0 # Tax priority. Only 1 matching rate per priority will be used. To define multiple tax rates for a single area you need to specify a different priority per rate. Default is 1.
        self.compound = False # Whether or not this is a compound tax rate. Compound rates are applied on top of other tax rates. Default is false.
        self.shipping = False # Whether or not this tax rate also gets applied to shipping. Default is true.
        self.order = 0  # Indicates the order that will appear in queries.
        self.classe = ""  # Tax class. Default is standard.
        self.__id = 0 #	integer	Unique identifier for the resource.read-only
