class Cart:
    """Cart class: holds a list of items to be bought by the customer"""
    def __init__(self, tax, shipping, coupon, items=None):
        if items is None:
            items = dict()
        self.tax = tax
        self.shipping = shipping
        self.coupon = coupon
        self.total = 0.00
        self.items = items

    def add_item(self, item):
        self.items.append(item)

    def check_out(self):
        t = self.total
        for item in self.items:
            t += self.items[item]
        t += self.shipping
        t *= (1 + self.tax)
        t -= self.coupon
        self.total = t
