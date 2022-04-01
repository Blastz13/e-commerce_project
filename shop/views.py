from django.db.models import Min, Max
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.contrib import messages

from .wishlist import WishList
from .cart import Cart
from .forms import CartAddProductForm, OrderUserForm, ProductCommentForm, ApplyCouponForm, WishListAddProduct
from .mixins import ObjectSortPaginate
from .models import Product, Category
from django.db.models import Q


class ProductSearch(ObjectSortPaginate, View):
    def get(self, request):
        query_search = self.request.GET.get('search', '')

        try:
            price_range_min_filter = float(request.GET['min-value'])
        except:
            price_range_min_filter = 0
        try:
            price_range_max_filter = float(request.GET['max-value'])
        except:
            price_range_max_filter = 10**100

        sort_by = sort_by_key.setdefault(request.GET.get('sort_by', ''), 'order')

        all_products = Product.objects.filter(is_publish=True,
                                              price__gte=price_range_min_filter,
                                              price__lte=price_range_max_filter).filter(Q(title__icontains=query_search)|Q(description__icontains=query_search)).order_by(sort_by)
        context = self.get_pagination(all_products, 5)
        context['all_category'] = Category.objects.all()
        context['price_range'] = Product.objects.filter(is_publish=True).aggregate(Min('price'), Max('price'))
        context['price_range']['price__min'] = str(context['price_range']['price__min'])
        context['price_range']['price__max'] = str(context['price_range']['price__max'])
        return render(request, 'shop/shop-list.html', context=context)


class CategoryProductVertical(ObjectSortPaginate, View):
    def get(self, request, slug):
        try:
            price_range_min_filter = float(request.GET['min-value'])
        except:
            price_range_min_filter = 0
        try:
            price_range_max_filter = float(request.GET['max-value'])
        except:
            price_range_max_filter = 10*100
        user_slug = slug
        category_slug = slug.split('/')
        parent = None
        root = Category.objects.all()

        try:
            for slug in category_slug[:-1]:
                parent = root.get(parent=parent, slug=slug)
        except:
            return HttpResponse('404 - 1')

        try:
            category = get_object_or_404(Category, parent=parent, slug=category_slug[-1])

        except:
            product = get_object_or_404(Product, slug=category_slug[-1], is_publish=True)
            product.count_views += 1
            product.save()

            if product.get_product_url() != user_slug:
                return HttpResponse('404 - 2')
            form = CartAddProductForm(request.POST or None, extra={'slug': category_slug[-1],
                                                                   'cart': Cart(request)})
            form_product_comment = ProductCommentForm()
            return render(request, 'shop/product-virtual.html', context={'product': product,
                                                                         'form': form,
                                                                         'form_product_comment': form_product_comment})

        else:
            sort_by = sort_by_key.setdefault(request.GET.get('sort_by', ''), 'order')
            products_by_category = Product.objects.filter(category__in=category.get_descendants(include_self=True),
                                                          is_publish=True,
                                                          price__gte=price_range_min_filter,
                                                          price__lte=price_range_max_filter).order_by(sort_by)
            context = self.get_pagination(products_by_category)
            context['all_category'] = Category.objects.all()
            context['price_range'] = Product.objects.filter(category__in=category.get_descendants(include_self=True),
                                                            is_publish=True).aggregate(Min('price'), Max('price'))
            context['price_range']['price__min'] = str(context['price_range']['price__min'])
            context['price_range']['price__max'] = str(context['price_range']['price__max'])
            context['obj_selected_category'] = category
            return render(request, 'shop/shop-list.html', context=context)


class ProductListVertical(ObjectSortPaginate, View):
    def get(self, request):
        try:
            price_range_min_filter = float(request.GET['min-value'])
        except:
            price_range_min_filter = 0
        try:
            price_range_max_filter = float(request.GET['max-value'])
        except:
            price_range_max_filter = 10**100

        sort_by = sort_by_key.setdefault(request.GET.get('sort_by', ''), 'order')

        all_products = Product.objects.filter(is_publish=True,
                                              price__gte=price_range_min_filter,
                                              price__lte=price_range_max_filter).order_by(sort_by)
        context = self.get_pagination(all_products, 5)
        context['all_category'] = Category.objects.all()
        context['price_range'] = Product.objects.filter(is_publish=True).aggregate(Min('price'), Max('price'))
        context['price_range']['price__min'] = str(context['price_range']['price__min'])
        context['price_range']['price__max'] = str(context['price_range']['price__max'])
        return render(request, 'shop/shop-list.html', context=context)


class ProductList(ObjectSortPaginate, View):
    def get(self, request):
        try:
            price_range_min_filter = float(request.GET['min-value'])
        except:
            price_range_min_filter = 0
        try:
            price_range_max_filter = float(request.GET['max-value'])
        except:
            price_range_max_filter = 10**100

        sort_by = sort_by_key.setdefault(request.GET.get('sort_by', ''), 'order')

        all_products = Product.objects.filter(is_publish=True,
                                              price__gte=price_range_min_filter,
                                              price__lte=price_range_max_filter).order_by(sort_by)
        context = self.get_pagination(all_products, 12)
        context['all_category'] = Category.objects.all()
        context['price_range'] = Product.objects.filter(is_publish=True).aggregate(Min('price'), Max('price'))
        context['price_range']['price__min'] = str(context['price_range']['price__min'])
        context['price_range']['price__max'] = str(context['price_range']['price__max'])
        return render(request, 'shop/shop.html', context=context)


class CategoryProduct(ObjectSortPaginate, View):
    def get(self, request, slug):
        try:
            price_range_min_filter = float(request.GET['min-value'])
        except:
            price_range_min_filter = 0
        try:
            price_range_max_filter = float(request.GET['max-value'])
        except:
            price_range_max_filter = 10**100
        user_slug = slug
        category_slug = slug.split('/')
        parent = None
        root = Category.objects.all()

        try:
            for slug in category_slug[:-1]:
                parent = root.get(parent=parent, slug=slug)
        except:
            return HttpResponse('404 - 1')
        try:
            category = get_object_or_404(Category, parent=parent, slug=category_slug[-1])

        except:
            product = get_object_or_404(Product, slug=category_slug[-1], is_publish=True)
            product.count_views += 1
            product.save()

            if product.get_product_url() != user_slug:
                return HttpResponse('404 - 2')
            form = CartAddProductForm(request.POST or None, extra={'slug': category_slug[-1],
                                                                   'cart': Cart(request)})
            form_product_comment = ProductCommentForm()
            return render(request, 'shop/product-virtual.html', context={'product': product,
                                                                         'form': form,
                                                                         'form_product_comment': form_product_comment})

        else:
            sort_by = sort_by_key.setdefault(request.GET.get('sort_by', ''), 'order')
            products_by_category = Product.objects.filter(category__in=category.get_descendants(include_self=True),
                                                          is_publish=True,
                                                          price__gte=price_range_min_filter,
                                                          price__lte=price_range_max_filter).order_by(sort_by)
            print(products_by_category)
            context = self.get_pagination(products_by_category)
            context['all_category'] = Category.objects.all()
            context['price_range'] = Product.objects.filter(category__in=category.get_descendants(include_self=True),
                                                            is_publish=True).aggregate(Min('price'), Max('price'))
            context['price_range']['price__min'] = str(context['price_range']['price__min'])
            context['price_range']['price__max'] = str(context['price_range']['price__max'])
            context['obj_selected_category'] = category
            return render(request, 'shop/shop.html', context=context)

    def post(self, request, slug):
        cart = Cart(request)

        product = get_object_or_404(Product, slug=slug)
        form = CartAddProductForm(request.POST, extra={'slug': slug,
                                                       'cart': Cart(request)})
        success_form = CartAddProductForm(extra={'slug': slug,
                                                 'cart': Cart(request)})
        if form.is_valid():
            cd = form.cleaned_data
            price = cd.pop('total_price')
            quantity = cd.pop('quantity')
            cart.add(product=product,
                     price=price,
                     quantity=quantity,
                     property=cd)
        else:
            return render(request, 'shop/product-virtual.html', context={'product': product, 'form': form})
        return render(request, 'shop/product-virtual.html', context={'product': product, 'form': success_form})


@require_POST
def add_to_cart_alone_product(request, slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=slug)

    form = CartAddProductForm(request.POST, extra={'slug': slug,
                                                   'cart': Cart(request)})
    if form.is_valid():
        cd = form.cleaned_data
        price = cd.pop('total_price')
        quantity = cd.pop('quantity')
        cart.add(product=product,
                 price=price,
                 quantity=quantity,
                 property=cd)
        return HttpResponse(status=200)
    return HttpResponse(status=404)


class AddProductComment(View):
    def post(self, request, slug):
        form = ProductCommentForm(request.POST)
        product = Product.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


class CartProduct(View):
    def get(self, request):
        cart = Cart(request)
        form = ApplyCouponForm()
        return render(request, 'shop/cart.html', context={'cart': cart, 'form': form})


class Checkout(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Для оформления заказа нужно авторизоваться или создать аккаунт')
            return redirect('Account')
        else:
            form = OrderUserForm()
        cart = Cart(request)
        return render(request, 'shop/checkout.html', context={'cart': cart,
                                                              'form': form})

    def post(self, request):
        form = OrderUserForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            if cart.is_valid():
                cart.create_order(form.cleaned_data)
            return redirect('CartProduct')
        else:
            return render(request, 'shop/checkout.html', context={'cart': cart, 'form': form})


@require_POST
def cart_del(request, slug):
    cart = Cart(request)
    cart.remove(slug)
    return redirect('CartProduct')


@require_POST
def apply_coupon(request):
    cart = Cart(request)
    form = ApplyCouponForm(request.POST)
    if form.is_valid():
        cart.apply_coupon(form.cleaned_data['code'])
    return redirect('CartProduct')


class WishListView(View):
    def get(self, request):
        wish_list = WishList(request)
        return render(request, 'shop/wishlist.html', context={'wish_list': wish_list})


@require_POST
def del_product_to_wish_list(request, slug):
    wish_list = WishList(request)
    wish_list.remove(slug)
    return redirect('WishList')


@require_POST
def add_product_to_wish_list(request):
    form = WishListAddProduct(request.POST)
    if form.is_valid():
        product = get_object_or_404(Product, slug=form.cleaned_data['slug'])
        wish_list = WishList(request)
        wish_list.add(product.slug)
        return HttpResponse(status=200)
    return HttpResponse(status=404)


sort_by_key = {
    'default': '-order',
    'views': '-count_views',
    'newness': '-date_publicate',
    'price': 'price',
    '-price': '-price'
}
