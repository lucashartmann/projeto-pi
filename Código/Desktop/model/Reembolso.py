from datetime import datetime


class Reembolso:
    def __init__(self):
        self.id = 0
        self.ate_created = datetime(2025, 1, 1)
        self.amount = ""
        self.reason = ""
        self.refunded_by = 0
        self.line_items = []
        self.shipping_lines = []
