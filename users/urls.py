from django.urls import path
from .views import Account, sign_up, log_out, OrdersUser, DetailOrder, EditProfile, ChangePasswordProfile
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login/', Account.as_view(), name='Account'),
    path('logout/', log_out, name='Logout'),
    path('signup/', sign_up, name='SignUp'),
    path('my-account/', login_required(OrdersUser.as_view()), name='OrdersUser'),
    path('edit-profile/', login_required(EditProfile.as_view()), name='EditProfile'),
    path('change-password-profile/', login_required(ChangePasswordProfile.as_view()), name='ChangePasswordProfile'),
    path('detail-order/<int:pk>', login_required(DetailOrder.as_view()), name='DetailOrder'),
]
