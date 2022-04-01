from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from mptt.models import MPTTModel, TreeForeignKey

from PIL import Image
from decimal import Decimal
from django.utils import timezone

from .utils import path_upload


User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название товара')
    description = models.TextField(max_length=10000, verbose_name='Описание товара')
    preview_image = models.ImageField(upload_to=path_upload('Shop/Product'), default='default_img/product.jpg',
                                      blank=True, null=True,
                                      verbose_name='Изображения для предпросмотра')
    slug = models.SlugField(unique=True, verbose_name='Ссылка на товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         verbose_name='Цена по скидке')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product', verbose_name='Категория')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество товара')
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления товара')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок показа товара')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовать')
    count_views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    count_buys = models.PositiveIntegerField(default=0, verbose_name='Количество покупок')

    @property
    def is_available(self):
        if self.quantity > 0:
            return True
        return False

    def get_product_image(self):
        return self.image.all()

    def get_product_url(self):
        return self.category.get_category_url() + '/' + self.slug

    def get_absolute_url(self):
        path = self.get_product_url()
        return reverse('CategoryProduct', kwargs={
            'slug': path
        })

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        image = Image.open(self.preview_image.path)
        if image.width < 480 or image.height < 606:
            fill_color = '#A36FFF'
            back = Image.new('RGB', (480, 606), fill_color)
            w = int((480 - image.width) / 2)
            h = int((606 - image.height) / 2)
            back.paste(image, (w, h))
            back.save(self.preview_image.path, quality=70, optimize=True)
        else:
            image.save(self.preview_image.path, quality=70, optimize=True)
        return image

    class Meta:
        ordering = ['order', '-date_publicate']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    image = models.ImageField(upload_to=path_upload('Shop/Product/Image'), verbose_name='Изображения товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image', verbose_name='Товар')

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)
        image = Image.open(self.image.path)
        image.save(self.image.path, quality=70, optimize=True)
        return image

    def __str__(self):
        return f"{self.product.title}"

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'


class ProductComment(models.Model):
    email = models.EmailField(verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name="Имя")
    text = models.TextField(max_length=5000, verbose_name="Сообщение")
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE, verbose_name="Товар")

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        ordering = ["-date_publicate"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Category(MPTTModel):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='Ссылка категории')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child',
                            verbose_name='Подкатегория')

    def get_category_url(self):
        return '/'.join([x['slug'] for x in self.get_ancestors(include_self=True).values()])

    def get_absolute_url(self):
        path = self.get_category_url()
        return reverse('CategoryProduct', kwargs={
            'slug': path
        })

    def get_absolute_url_vertical(self):
        path = self.get_category_url()
        return reverse('CategoryProductVertical', kwargs={
            'slug': path
        })

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['title']


class SpecialCategoryProduct(models.Model):
    CHOICES = (('row1', 'Строка тип 1'),
               ('row2', 'Строка тип 2'),
               ('grid', 'Сетка'))
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    product = models.ManyToManyField(Product, related_name='special_categories', verbose_name='Продукт')
    type_slider = models.CharField(max_length=16, choices=CHOICES, verbose_name='Тип слайдера')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специальная категория'
        verbose_name_plural = 'Специальные категории'


class Coupon(models.Model):
    code = models.CharField(max_length=16, unique=True, verbose_name='Купон')
    discount = models.PositiveIntegerField(max_length=100, verbose_name='Скидка %')
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Минимальная сумма активации')
    quantity_activation = models.PositiveIntegerField(verbose_name='Количество активаций')
    active_from = models.DateTimeField(verbose_name='Активен от')
    active_to = models.DateTimeField(verbose_name='Активен до')

    @property
    def is_valid(self):
        if (self.active_from < timezone.now() < self.active_to) and (self.quantity_activation > 0):
            return True
        else:
            return False

    def __str__(self):
        return f'{self.code} - {self.discount}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class Order(models.Model):
    city = models.CharField(max_length=128, verbose_name='Город')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    order_notes = models.CharField(max_length=512, blank=True, verbose_name='Примечания к заказу')
    date_create = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен заказ')

    def get_absolute_url(self):
        return reverse('DetailOrder', kwargs={'pk': self.id})

    @property
    def total_amount(self):
        if self.coupon:
            return (sum([order_item.total_amount for order_item in self.order_items.all()])*Decimal(
                   (100-self.coupon.discount)/100)).quantize(Decimal("1.00"))
        else:
            return sum([order_item.total_amount for order_item in self.order_items.all()])

    def __str__(self):
        return f'{self.buyer} - {self.date_create}'

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')

    @property
    def total_amount(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Оформленный товар'
        verbose_name_plural = 'Оформленные товары'
