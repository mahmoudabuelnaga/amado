from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart(object):

    # start initialize function
    def __init__(self, request):
        """
            initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    # end initialize function
    
    # start add function
    def add(self, product, quantity=1, update_quantity=False):
        """
            Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                        'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    # end add function

    # start save function
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
    # end save function

    # start remove function
    def remove(self, product):
        """
            Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    # end remove function

    # start __iter__ function
    def __iter__(self):
        """
            Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    # end __iter__ function

    # start __len__ function
    def __len__(self):
        """
            Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    # end __len__ function

    # start get_total_price function
    # def get_sub_total_price(self):
    #     return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    # end get_total_price function


    # start get_total_price function
    def get_total_price(self):
        # delevry = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) #+ Decimal(((int(delevry)/10) * 100))
    # end get_total_price function

    # start clear function
    def clear(self):
        """
            remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
    # end clear function