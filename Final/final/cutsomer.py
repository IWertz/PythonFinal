class Customer:
    """Customer Class: holds a cart class that can access all their carted items"""
    def __init__(self, fname, lname, balance):
        self.fname = fname
        self.lname = lname
        self.balance = balance
        self.cart = None

    class Cart:
        """Cart class: holds a list of items to be bought by the customer"""
        def __init__(self, tax, shipping, coupon):
            self.tax = tax
            self.shipping = shipping
            self.coupon = coupon
            self.subtotal = 0.00
            self.total = 0.00
            self.items = dict()

        def add_item(self, key, value):
            while self.items.get(key) is not None:
                key = key + "_1"
            self.items[key] = value

    def check_out(self):
        t = self.cart.total
        for item in self.cart.items:
            t += float(self.cart.items[item])
        self.cart.subtotal = t
        t += self.cart.shipping
        t *= (1 + self.cart.tax)
        t -= self.cart.coupon
        t = round(t, 2)
        self.cart.total = t
        self.balance = float(self.balance) - t

    def add_cart(self, tax, shipping, coupon):
        self.cart = self.Cart(tax, shipping, coupon)
