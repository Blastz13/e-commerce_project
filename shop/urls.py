from django.urls import path
from .views import ProductList, add_to_cart_alone_product, add_product_to_wish_list, del_product_to_wish_list
from .views import CategoryProduct, cart_del, CartProduct, Checkout, WishListView, \
                   AddProductComment, ProductListVertical, CategoryProductVertical, ProductSearch, apply_coupon

urlpatterns = [
    path('', ProductList.as_view(), name='ProductList'),
    path('list/', ProductListVertical.as_view(), name='ProductListVertical'),
    path('category/<path:slug>/', CategoryProduct.as_view(), name='CategoryProduct'),
    path('category-list/<path:slug>/', CategoryProductVertical.as_view(), name='CategoryProductVertical'),
    path('search/', ProductSearch.as_view(), name='ProductSearch'),
    path('cart/', CartProduct.as_view(), name='CartProduct'),
    path('cart/<str:slug>', add_to_cart_alone_product, name='add_to_cart_alone_product'),
    path('cart/del/<str:slug>/', cart_del, name='CartDel'),
    path('cart/apply-coupon/', apply_coupon, name='ApplyCoupon'),
    path('wish-list/', WishListView.as_view(), name='WishList'),
    path('wish-list/add/', add_product_to_wish_list, name='add_product_to_wish_list'),
    path('wish-list/del/<str:slug>', del_product_to_wish_list, name='del_product_to_wish_list'),
    path('place-order/', Checkout.as_view(), name='Checkout'),
    path('add-product-comment/<str:slug>/', AddProductComment.as_view(), name='AddProductComment'),
]
