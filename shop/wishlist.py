from django.conf import settings
from .models import Product


class WishList:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        wish_list = self.session.get(settings.WISH_LIST_SESSION_ID)
        if not wish_list:
            wish_list = self.session[settings.WISH_LIST_SESSION_ID] = {}
        self.wish_list = wish_list

    def add(self, slug):
        is_added = False
        try:
            product_id = str(int(list(self.wish_list.keys())[-1]) + 1)
        except IndexError:
            product_id = '1'

        for key, product_wish_list in self.wish_list.items():
            if product_wish_list['slug'] == slug:
                is_added = True

        if not is_added:
            self.wish_list[product_id] = {'product_id': product_id,
                                           'slug': slug}
        self.save()

    def save(self):
        self.session[settings.WISH_LIST_SESSION_ID] = self.wish_list
        self.session.modified = True

    def remove(self, product_num):
        product_id = str(product_num)
        if product_id in self.wish_list:
            del self.wish_list[product_id]
            self.save()

    def __iter__(self):
        for item in self.wish_list.values():
            item['product'] = Product.objects.get(slug=item['slug'])
            yield item

    def __len__(self):
        return len(self.wish_list.values())

    def clear(self):
        del self.session[settings.WISH_LIST_SESSION_ID]
        self.session.modified = True
