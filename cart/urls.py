from django.urls import path

import cart   
from .views import cart_view, cart_update, cart_add, cart_delete

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart-view'),
    path('cart_add/', cart_add, name='cart-add'),
    path('cart_delete/', cart_delete, name='cart-delete'),
    path('cart_update/', cart_update, name='cart-update'),
]