from datetime import datetime

class Cupom:
    def __init__(self, code:str):
        self.__id	= 0 #	Unique identifier for the object
        self.code = code  # Coupon code.mandatory
        self.amount = "" # The amount of discount. Should always be numeric, even if setting a percentage.
        self.__date_created	= datetime(2025,1,1) #	The date the coupon was created, in the site's timezone.read-only
        self.__date_created_gmt	= datetime(2025,1,1) #	The date the coupon was created, as GMT.read-only
        self.__date_modified	= datetime(2025,1,1) #	The date the coupon was last modified, in the site's timezone.read-only
        self.__date_modified_gmt	= datetime(2025,1,1) #	The date the coupon was last modified, as GMT.read-only
        self.discount_type = "" # Determines the type of discount that will be applied. Options: percent, fixed_cart and fixed_product. Default is fixed_cart.
        self.description = ""  # Coupon description.
        self.date_expires = ""         # The date the coupon expires, in the site's timezone.
        self.date_expires_gmt = ""  # The date the coupon expires, as GMT.
        self.__usage_count	= 0 #	Number of times the coupon has been used already.read-only
        self.individual_use = False # If true, the coupon can only be used individually. Other applied coupons will be removed from the cart. Default is false.
        self.product_ids = []  # List of product IDs the coupon can be used on.
        self.excluded_product_ids = [] # List of product IDs the coupon cannot be used on.
        self.usage_limit = 0  # How many times the coupon can be used in total.
        self.usage_limit_per_user = 0 # How many times the coupon can be used per customer.
        self.limit_usage_to_x_items = 0 # Max number of items in the cart the coupon can be applied to.
        self.free_shipping = False # If true and if the free shipping method requires a coupon, this coupon will enable free shipping. Default is false.
        self.product_categories = [] # List of category IDs the coupon applies to.
        self.excluded_product_categories = [] # List of category IDs the coupon does not apply to.
        self.exclude_sale_items = False # If true, this coupon will not be applied to items that have sale prices. Default is false.
        self.minimum_amount = "" # Minimum order amount that needs to be in the cart before coupon applies.
        self.maximum_amount = "" # Maximum order amount allowed when using the coupon.
        self.email_restrictions = [] # List of email addresses that can use this coupon.
        self.__used_by	= [] #	List of user IDs (or guest email addresses) that have used the coupon.read-only
        self.meta_data = []  # Meta data. See Coupon - Meta data properties