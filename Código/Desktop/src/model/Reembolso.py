from datetime import datetime

class Reembolso:
    def __init__(self):
        self.__id	= 0 #	Unique identifier for the resource.read-only
        self.__date_created	= datetime(2025,1,1) #	The date the order refund was created, in the site's timezone.read-only
        self.__date_created_gmt	= datetime(2025,1,1) #	The date the order refund was created, as GMT.read-only
        self.amount	= "" #	Total refund amount. Optional. If this parameter is provided, it will take precedence over line item totals, even when total of line items does not matches with this amount.
        self.reason	= "" #	Reason for refund.
        self.refunded_by	= 0 #	User ID of user who created the refund.
        self.__refunded_payment	= False #	If the payment was refunded via the API. See api_refund.read-only
        self.meta_data	= [] #	Meta data. See Order refund - Meta data properties
        self.line_items	= [] #	Line items data. See Order refund - Line items properties
        self.__tax_lines	= [] #	Tax lines data. See Order refund - Tax lines propertiesread-only
        self.shipping_lines	= [] #	Shipping lines data. See Order refund - Shipping lines properties
        self.fee_lines	= [] #	Fee lines data. See Order refund - Fee lines properties
        self.api_refund	= False #	When true, the payment gateway API is used to generate the refund. Default is true.write-only
        self.api_restock	= False #	When true, the selected line items are restocked Default is true.write-only