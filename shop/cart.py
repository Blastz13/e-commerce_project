from django.conf import settings
from shop.models import Product, Order, OrderItem
from django.contrib import messages

from .models import Coupon

import copy
from decimal import Decimal


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {'products': {}}
        self.cart = cart

    def add(self, product, price, quantity=1, property=None):
        is_added = False
        try:
            product_id = str(int(list(self.cart['products'].keys())[-1]) + 1)
        except IndexError:
            product_id = '1'

        for key, product_cart in self.cart['products'].items():
            if product_cart['product_slug'] == product.slug and product_cart['property'] == property:
                self.cart['products'][key]['quantity'] += quantity
                is_added = True

        if not is_added:
            self.cart['products'][product_id] = {'product_id': product_id,
                                                 'product_slug': product.slug,
                                                 'quantity': 0,
                                                 'property': property,
                                                 'price': price}

            self.cart['products'][product_id]['quantity'] += quantity
        self.save()

    def apply_coupon(self, code):
        try:
            coupon = Coupon.objects.get(code=code)
            if self.check_valid_coupon(coupon):
                self.cart['coupon'] = coupon.code
                self.save()
                messages.info(self.request, 'Купон успешно применен')
            else:
                messages.error(self.request, 'Данный купон не валиден')
        except Coupon.DoesNotExist:
            messages.error(self.request, 'Проверьте правильность ввода купона')

    def create_order(self, cd):
        order = Order.objects.create(city=cd['city'],
                                     address=cd['address'],
                                     phone=cd['phone'],
                                     order_notes=cd['order_notes'],
                                     buyer=self.request.user,
                                     coupon=self.get_coupon_in_cart())
        for order_item in self.__class__.__iter__(self):
            product = order_item['product']
            OrderItem.objects.create(order=order, product=order_item['product'],
                                     price=order_item['price'], quantity=order_item['quantity'])
            product.quantity -= order_item['quantity']
            product.count_buys += 1
            product.save()
        messages.info(self.request, 'Заказ успешно оформлен')
        self.clear()

    def is_valid(self):
        if not (self.check_valid_products_in_cart()) or not (self.check_valid_coupon_in_cart()):
            return False
        else:
            return True

    def check_valid_products_in_cart(self):
        is_valid = True

        if self.__len__() <= 0:
            messages.error(self.request, 'Ваша корзина пуста')
            return False

        for item in self.__class__.__iter__(self):
            product = item['product']

            if not (product.is_available and product.is_publish and product.quantity != 0):
                is_valid = False
                self.remove(item['product_id'])

            if product.quantity < item['quantity']:
                is_valid = False
                self.cart[item['product_id']]['quantity'] = product.quantity

            if product.discount_price:
                if str(product.discount_price) != item['price']:
                    is_valid = False
                    self.cart[item['product_id']]['price'] = str(product.discount_price)
            else:
                if str(product.price) != item['price']:
                    is_valid = False
                    self.cart[item['product_id']]['price'] = str(product.price)

        if not is_valid:
            self.save()
            messages.error(self.request, 'Ваша корзина изменилась, не все товары доступны')
            return False
        return True

    def get_coupon_in_cart(self):
        try:
            return Coupon.objects.get(code=self.cart['coupon'])
        except (Coupon.DoesNotExist, KeyError):
            return None

    def check_valid_coupon_in_cart(self):
        coupon = self.get_coupon_in_cart()
        if coupon and not(self.check_valid_coupon(coupon)):
            messages.error(self.request, 'Купон истек')
            self.remove_coupon_in_cart()
            return False
        return True

    def check_valid_coupon(self, coupon):
        if coupon.is_valid and self.get_total_price() > coupon.minimum_amount:
            return True
        else:
            return False

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product_num):
        product_id = str(product_num)
        if product_id in self.cart['products']:
            del self.cart['products'][product_id]
            self.save()

    def remove_coupon_in_cart(self):
        del self.cart['coupon']
        self.save()

    def __iter__(self):
        self.cart_order = copy.deepcopy(self.cart)
        for key in self.cart_order['products'].keys():
            # TODO: try get object
            product = Product.objects.get(slug=self.cart['products'][key]['product_slug'])
            self.cart_order['products'][key]['product'] = product

        for item in self.cart_order['products'].values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart['products'].values())

    def sum_cart(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart['products'].values())

    def get_total_price_(self):
        coupon = self.get_coupon_in_cart()
        if coupon:
            return (self.sum_cart()*Decimal((100-coupon.discount)/100)).quantize(Decimal("1.00"))
        else:
            return self.sum_cart()

    def get_total_price(self):
        coupon = self.get_coupon_in_cart()
        if coupon:
            return (sum(Decimal(item['price']) * item['quantity'] for item in
                    self.cart['products'].values())*Decimal((100-coupon.discount)/100)).quantize(Decimal("1.00"))
        else:
            return sum(Decimal(item['price']) * item['quantity'] for item in
                       self.cart['products'].values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
