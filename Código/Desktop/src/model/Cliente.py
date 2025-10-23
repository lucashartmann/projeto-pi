from datetime import datetime

class Cliente:
    def __init__(self, email:str):
        self.__id = 0 #integer	Unique identifier for the resource.
        self.__date_created	= datetime(2025,1,1) #	The date the customer was created, in the site's timezone.read-only
        self.__date_created_gmt	= datetime(2025,1,1) #	The date the customer was created, as GMT.read-only
        self.__date_modified	= datetime(2025,1,1) #	The date the customer was last modified, in the site's timezone.read-only
        self.__date_modified_gmt	= datetime(2025,1,1) #	The date the customer was last modified, as GMT.read-only
        self.email = email  # The email address for the customer.mandatory
        self.first_name = ""  # Customer first name.
        self.last_name = ""  # Customer last name.
        self.__role	= "" #	Customer role.read-only
        self.username = ""  # Customer login name.
        self.password = ""  # Customer password.write-only
        self.billing = object  # List of billing address data. See Customer - Billing properties
        self.shipping = object  # List of shipping address data. See Customer - Shipping properties
        self.__is_paying_customer = False #	Is the customer a paying customer?read-only
        self.__avatar_url = "" #	Avatar URL.read-only
        self.meta_data = []  # Meta data. See Customer - Meta data properties'
