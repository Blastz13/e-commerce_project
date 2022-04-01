from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.views.generic import View

from .forms import CustomUserCreationForm, LoginForm, EditProfileForm, ChangePasswordForm
from shop.models import Order


class Account(View):
    def get(self, request):
        form_registration = CustomUserCreationForm()
        form_login = LoginForm()
        return render(request, 'users/login.html', context={'form_registration': form_registration,
                                                            'form_login': form_login})

    def post(self, request):
        form_registration = CustomUserCreationForm()
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            cd = form_login.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if (user is not None) and user.is_active:
                login(request, user)
                request.session.cycle_key()
                return redirect('HomePage')
            else:
                return render(request, 'users/login.html', context={'form_registration': form_registration,
                                                                    'form_login': form_login})
        return render(request, 'users/login.html', context={'form_registration': form_registration,
                                                            'form_login': form_login})


@require_POST
def sign_up(request):
    form_registration = CustomUserCreationForm(request.POST)
    form_login = LoginForm()

    if form_registration.is_valid():
        user = form_registration.save()
        login(request, user)
        return redirect('HomePage')
    else:
        return render(request, 'users/login.html', {'form_registration': form_registration,
                                                    'form_login': form_login})


def log_out(request):
    logout(request)
    return redirect('HomePage')


class OrdersUser(View):
    def get(self, request):
        orders = Order.objects.filter(buyer=request.user)
        return render(request, 'users/my-account.html', context={'orders': orders})


class DetailOrder(View):
    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk, buyer=request.user)
        except Order.DoesNotExist:
            raise PermissionDenied()
        return render(request, 'users/detail-order.html', context={'order': order})


class EditProfile(View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, 'users/edit-profile.html', context={'form': form})

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, 'users/edit-profile.html', context={'form': form})


class ChangePasswordProfile(View):
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'users/edit-profile.html', context={'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.POST, request=request)
        if form.is_valid():
            form.save()
        return render(request, 'users/edit-profile.html', context={'form': form})
