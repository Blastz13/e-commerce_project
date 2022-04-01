from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms.widgets import Select

from shop.models import Product, ProductComment

User = get_user_model()


class CustomSelectWidget(Select):

    def __init__(self, attrs=None, choices=(), disabled_choices=(), price_choices=()):
        super(Select, self).__init__(attrs, choices=choices)
        # disabled_choices is a list of disabled values
        self.disabled_choices = disabled_choices
        self.price_choices = price_choices

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(Select, self).create_option(name, value, label, selected, index, subindex, attrs)
        if value in self.disabled_choices:
            option['attrs']['disabled'] = True
        for price_choice in self.price_choices:
            if value in price_choice:
                option['attrs']['data-price'] = price_choice[1]
        return option


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, initial=1, label="Количество: ")
    total_price = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}), label="")

    def __init__(self, *args, **kwargs):

        extra = kwargs.pop('extra')

        super().__init__(*args, **kwargs)

        self.obj = Product.objects.get(slug=extra['slug'])
        self.cart = extra['cart']

        # if self.obj.property:
        #     for field in self.obj.property:
        #         CHOICES = []
        #         DISABLED = []
        #         PRICE = []
        #         for value in self.obj.property[field]:
        #             if int(self.obj.property[field][value]['quantity']) <= 0:
        #                 DISABLED.append(value)
        #             PRICE.append((value, self.obj.property[field][value]['price']))
        #             wrap = (value, value)
        #             CHOICES.append(wrap)
        #
        #         self.price_choices = PRICE
        #         self.fields[field] = forms.CharField(label=field,  widget=CustomSelectWidget(choices=CHOICES,
        #                                                                                      disabled_choices=DISABLED,
        #                                                                                      price_choices=PRICE, attrs={'id': 'property'}))

    def clean(self):
        quantity_cart = 0
        cleaned_data = super(CartAddProductForm, self).clean()
        quantity_select = cleaned_data['quantity']
        del cleaned_data['quantity']

        total_price = cleaned_data['total_price']
        del cleaned_data['total_price']

        breadcump = []

        if cleaned_data:

            for item in cleaned_data.items():
                for prop in item:
                    breadcump.append(prop)

            obj_quantity = int(self.obj.property[breadcump[0]][breadcump[1]]['quantity'])
            obj_property_price = Decimal(self.obj.property[breadcump[0]][breadcump[1]]['price'])

            if Decimal(obj_property_price) * Decimal(quantity_select) != Decimal(total_price):
                raise ValidationError(f'Произошла ошибка')

            for key, product_cart in self.cart.cart.items():
                if product_cart['product_slug'] == self.obj.slug and product_cart['property'] == cleaned_data:
                    quantity_cart = product_cart['quantity']

            if obj_quantity < quantity_select + quantity_cart:
                raise ValidationError(f'Товар закончился, доступно только - {obj_quantity}')

            cleaned_data['total_price'] = str(obj_property_price)
        else:
            if self.obj.discount_price:
                cleaned_data['total_price'] = str(Decimal(self.obj.discount_price))
            else:
                cleaned_data['total_price'] = str(Decimal(self.obj.price))

            for key, product_cart in self.cart.cart['products'].items():
                if product_cart['product_slug'] == self.obj.slug:
                    quantity_cart = product_cart['quantity']

            if self.obj.quantity < quantity_select + quantity_cart:
                raise ValidationError(f'Товар закончился, доступно только - {self.obj.quantity}')

        cleaned_data['quantity'] = quantity_select


class OrderUserForm(forms.Form):
    city = forms.CharField()
    address = forms.CharField()
    phone = forms.CharField(max_length=12)
    order_notes = forms.CharField(widget=forms.Textarea(attrs={"style": "width:100%; height: 42px"}), required=False)


class OrderUnregisteredUserForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    phone = forms.CharField(max_length=12)
    city = forms.CharField()
    address = forms.CharField()
    order_notes = forms.CharField(widget=forms.Textarea())

    def clean(self):
        cd = super(OrderUnregisteredUserForm, self).clean()
        if cd['password'] != cd['confirm_password'] and self.password and self.confirm_password:
            raise ValidationError('Пароли не совпадают')
        if User.objects.get(email=cd['email']):
            raise ValidationError('Аккаунт с таким email уже существует')


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['email', 'name', 'text']

        widgets = {
            "email": forms.EmailInput(attrs={'placeholder': 'Your email'}),
            "name": forms.TextInput(attrs={'placeholder': 'Your name'}),
            "text": forms.Textarea(attrs={'placeholder': 'Your Rating',  'id': 'product-message'},)
        }


class ApplyCouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Coupon code'}))


class WishListAddProduct(forms.Form):
    slug = forms.SlugField(widget=forms.TextInput)
