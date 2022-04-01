from django import template

from core.models import OurBrand
from shop.models import Product

from shop.cart import Cart


register = template.Library()


@register.inclusion_tag('shop/inclusion_html/widget-our-brands.html')
def our_brands():
    return {'our_brands': OurBrand.objects.all()}


@register.inclusion_tag('shop/inclusion_html/widget-breadcrumb-area.html')
def breadcrumb_area(obj_product=None):
    return {'obj_title_product': obj_product.title,
            'obj_category_product': obj_product.category.get_ancestors(include_self=True)}


@register.inclusion_tag('shop/inclusion_html/widget-breadcrumb-area-shop.html')
def breadcrumb_area_shop(obj_selected_category=None):
    if not obj_selected_category:
        return {}
    return {'tree_categories': obj_selected_category.get_ancestors(include_self=True)}


@register.inclusion_tag('shop/inclusion_html/widget-cart.html')
def widget_cart(request):
    cart = Cart(request)
    return {'cart': cart}


@register.inclusion_tag('shop/inclusion_html/widget-top-rated-products.html')
def widget_top_rated_products(obj_selected_category=None):
    if obj_selected_category:
        top_rated_products = Product.objects.filter(category__in=obj_selected_category
                                                    .get_descendants(include_self=True),
                                                    is_publish=True).order_by('-count_views')[:5]
    else:
        top_rated_products = Product.objects.filter(is_publish=True).order_by('-count_views')[:5]
    return {'top_rated_products': top_rated_products}


@register.inclusion_tag('shop/inclusion_html/widget-up-sells-products.html')
def widget_up_sells_products(obj_product):
    up_sells_products = Product.objects.filter(category=obj_product.category).order_by('-count_buys')\
                                                                             .exclude(id=obj_product.id)[:4]
    return {'up_sells_products': up_sells_products}


@register.inclusion_tag('shop/inclusion_html/widget-recent-products.html')
def widget_recent_products(obj_product):
    recent_products = Product.objects.filter(category=obj_product.category).order_by('-date_publicate')\
                                                                             .exclude(id=obj_product.id)[4:]
    return {'recent_products': recent_products}
