from decimal import Decimal

from django.contrib import sessions

from shop.models import ProductProxy

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def __len__(self):
        return sum(value['qty'] for value in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'qty':quantity, 'price':str(product.get_discount_price())}
        self.cart[product_id]['qty'] = quantity

        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
    
    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[str(product.id)]
            self.session.modified = True

    
    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[str(product.id)]['qty'] = quantity
            self.session.modified = True