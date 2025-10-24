from datetime import datetime


class Cupom:
    def __init__(self, code: str):
        self.id = 0
        self.code = code
        self.amount = ""
        self.date_created = datetime(2025, 1, 1)
        self.date_modified = datetime(2025, 1, 1)
        self.description = ""
        self.date_expires = ""
        self.usage_count = 0
        self.individual_use = False
        self.product_ids = []
        self.usage_limit = 0
        self.usage_limit_per_user = 0
        self.limit_usage_to_x_items = 0
        self.free_shipping = False
        self.product_categories = []
        self.minimum_amount = ""
        self.maximum_amount = ""
        self.used_by = []
