from django.contrib import admin
from .models import Order, OrderItem, ShippingAdress

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAdress)

