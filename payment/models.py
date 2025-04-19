from django.db import models

from django.contrib.auth import get_user_model
from shop.models import Product,ProductProxy, Category

User = get_user_model()

class ShippingAdress(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)

    street_address = models.CharField(max_length=250)
    apartment_address = models.CharField(max_length=250)
    
    country = models.CharField(max_length=250,blank=True, null= True)
    city = models.CharField(max_length=250,blank=True, null= True)
    zip = models.CharField(max_length=250,blank=True, null= True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shipping address object: {self.id}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAdress, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  
        return f"Order object: {self.id}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(ProductProxy, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"OrderItem object: {self.id}"
