from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import ProductImage, Order, OrderItem, Category, ProductComment, Product, Coupon, SpecialCategoryProduct


class ProductImageItemInline(admin.StackedInline):
    model = ProductImage
    list_display = ['get_image', 'product']
    list_display_links = ['get_image', 'product']
    search_fields = ['get_image']
    extra = 1

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="640" height="360"')

    get_image.short_description = "Изображение"


class ProductCommentItemInline(admin.TabularInline):
    model = ProductComment
    list_display = ['email', 'name', 'date_publicate', 'product']
    list_display_links = ['email', 'name', 'date_publicate', 'product']
    search_fields = ['email', 'name']
    readonly_fields = ['email', 'name']
    extra = 1


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'discount_price', 'get_image', 'quantity', 'is_available',
                    'is_publish', 'slug']
    list_display_links = ['title', 'category', 'price', 'discount_price', 'slug']
    list_filter = ['category', 'is_publish']
    readonly_fields = ['is_available']
    search_fields = ('title', 'description', 'price', 'discount_price')
    inlines = [ProductImageItemInline, ProductCommentItemInline]

    def is_available(self, obj):
        return obj.is_available
    is_available.boolean = True
    is_available.short_description = 'В наличии'

    def get_image(self, obj):
        if obj.preview_image:
            return mark_safe(f'<img src={obj.preview_image.url} width="80" height="100"')

    get_image.short_description = "Изображение"


@admin.register(Category)
class AdminCategory(MPTTModelAdmin):
    list_display = ['title', 'slug', 'parent']
    list_display_links = ['title', 'slug', 'parent']
    search_fields = ['title', 'slug']


class AdminOrderItem(admin.StackedInline):
    model = OrderItem
    list_display = ['date_create', 'quantity', 'total_amount']
    list_display_links = ['date_create', 'quantity', 'total_amount']
    extra = 0


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['city', 'address', 'phone', 'order_notes', 'date_create', 'is_paid', 'total_amount']
    list_display_links = ['city', 'address', 'phone', 'order_notes', 'date_create', 'is_paid', 'total_amount']
    search_fields = ('city', 'address', 'phone', 'order_notes', 'date_create', 'is_paid')
    readonly_fields = ('total_amount', )
    inlines = [AdminOrderItem]


@admin.register(Coupon)
class AdminCoupon(admin.ModelAdmin):
    list_display = ['code', 'discount', 'minimum_amount', 'quantity_activation', 'active_from', 'active_to', 'is_valid']
    list_display_links = ['code', 'discount', 'minimum_amount', 'quantity_activation', 'active_from', 'active_to']
    search_fields = ['code', 'discount', 'minimum_amount', 'quantity_activation', 'active_from', 'active_to']

    def is_valid(self, obj):
        return obj.is_valid

    is_valid.boolean = True
    is_valid.short_description = 'Действительный'

@admin.register(SpecialCategoryProduct)
class AdminSpecialCategoryProduct(admin.ModelAdmin):
    pass