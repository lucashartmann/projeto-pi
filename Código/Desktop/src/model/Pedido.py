from datetime import datetime

class Pedido:
    def __init__(self):
        self.parent_id = 0  # Parent order ID.
        self.created_via = "" # Shows where the order was created. It can only be set during order creation and cannot be modified afterward.
        self.status = "" # Order status. Options: pending, processing, on-hold, completed, cancelled, refunded, failed and trash. Default is pending.
        self.currency = "" # Currency the order was created with, in ISO format. Default is USD.
        self.prices_include_tax = False
        self.customer_id = 0 # User ID who owns the order. 0 for guests. Default is 0.
        self.customer_note = ""  # Note left by customer during checkout.
        self.billing = object  # Billing address. See Order - Billing properties
        self.shipping = object  # Shipping address. See Order - Shipping properties
        self.payment_method = ""  # Payment method ID.
        self.payment_method_title = ""  # Payment method title.
        self.transaction_id = ""  # Unique transaction ID.
        self.meta_data = []  # Meta data. See Order - Meta data properties
        self.line_items = []  # Line items data. See Order - Line items properties
        self.shipping_lines = []  # Shipping lines data. See Order - Shipping lines properties
        self.fee_lines = []  # Fee lines data. See Order - Fee lines properties
        self.coupon_lines = []  # Coupons line data. See Order - Coupon lines properties
        self.set_paid = False  # Define if the
        self.__id	= 0 #	Unique identifier for the resource.read-only
        self.__number	= "" #	Order number.read-only
        self.__order_key	= "" #	Order key.read-only
        self.__version	= "" #	Version of WooCommerce which last updated the order.read-only
        self.__date_created	= datetime(2025,1,1) #	The date the order was created, in the site's timezone.read-only
        self.__date_created_gmt	= datetime(2025,1,1) #	The date the order was created, as GMT.read-only
        self.__date_modified	= datetime(2025,1,1) #	The date the order was last modified, in the site's timezone.read-only
        self.__date_modified_gmt	= datetime(2025,1,1) #	The date the order was last modified, as GMT.read-only
        self.__discount_total	= "" #	Total discount amount for the order.read-only
        self.__discount_tax	= "" #	Total discount tax amount for the order.read-only
        self.__shipping_total	= "" #	Total shipping amount for the order.read-only
        self.__shipping_tax	= "" #	Total shipping tax amount for the order.read-only
        self.__cart_tax	= "" #	Sum of line item taxes only.read-only
        self.__total	= "" #	Grand total.read-only
        self.__total_tax	= "" #	Sum of all taxes.read-only
        self.__prices_include_tax	= False #	True the prices included tax during checkout.read-only
        self.__customer_ip_address	= "" #	Customer's IP address.read-only
        self.__customer_user_agent	= "" #	User agent of the customer.read-only
        self.__date_paid	= datetime(2025,1,1) #	The date the order was paid, in the site's timezone.read-only
        self.__date_paid_gmt	= datetime(2025,1,1) #	The date the order was paid, as GMT.read-only
        self.__date_completed	= datetime(2025,1,1) #	The date the order was completed, in the site's timezone.read-only
        self.__date_completed_gmt	= datetime(2025,1,1) #	The date the order was completed, as GMT.read-only
        self.__cart_hash	= "" #	MD5 hash of cart items to ensure orders are not modified.read-only
        self.__tax_lines	= [] #	Tax lines data. See Order - Tax lines propertiesread-only
        self.__refunds	= [] #	List of refunds. See Order - Refunds propertiesread-only