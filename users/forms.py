from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.error_messages['password_mismatch'] = 'Пароли не совпадают'

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'password')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone')

    def save(self, commit=True):
        self.instance.email = self.cleaned_data['email']
        self.instance.first_name = self.cleaned_data['first_name']
        self.instance.last_name = self.cleaned_data['last_name']
        self.instance.phone = self.cleaned_data['phone']
        self.instance.save()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Старый пароль')
    new_password_1 = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    new_password_2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cd = super(ChangePasswordForm, self).clean()
        if not(self.request.user.check_password(cd['old_password'])):
            raise ValidationError('Введен неверный пароль')
        elif cd['new_password_1'] != cd['new_password_2']:
            raise ValidationError('Пароли не совпали')

    def save(self):
        self.request.user.set_password(self.cleaned_data['new_password_1']).save()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super(LoginForm, self).clean()
        user = authenticate(email=cd['email'], password=cd['password'])
        if user is None:
            raise ValidationError('Неверный логин или пароль')
