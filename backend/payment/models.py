from decimal import Decimal
from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth import get_user_model
from shop.models import Product,ProductProxy, Category

User = get_user_model()

class ShippingAdress(models.Model):
    class Meta:
        verbose_name = ("Адрес доставки")
        verbose_name_plural = ("Адреса доставки")
        ordering = ['-id']

    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)

    street_address = models.CharField(max_length=250)
    apartment_address = models.CharField(max_length=250)
    
    country = models.CharField(max_length=250,blank=True, null= True)
    city = models.CharField(max_length=250,blank=True, null= True)
    zip = models.CharField(max_length=250,blank=True, null= True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse("payment:shipping")
    
    def __str__(self):
        return f"Shipping address object: {self.full_name}"
    
    @classmethod
    def create_default_shipping_address(cls, user):
        default_shipping_adress = {
            "user": user, 
            "full_name": user.first_name + " " + user.last_name,
            "email": user.email,
            "street_address": "fill address",
            "apartment_address": "fill apartment",
            "country": "fill country",
            "city": "fill city",
            "zip": "fill zip",
        }
        shipping_addres= cls(**default_shipping_adress)
        shipping_addres.save()
        return shipping_addres

class Order(models.Model):
    class Meta:
        verbose_name = ("Заказ")
        verbose_name_plural = ("Заказы")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte=0), name='amount_gte_0')
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAdress, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    def __str__(self): 
        return f"Order object: {self.id}"
    
    def get_absolute_url(self):
        return reverse("payment:order-detail", kwargs={"order_id": self.id})
    
    def get_total_price_before_discount(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total
    @property
    def get_discount(self):
        if (total_cost:=self.get_total_price_before_discount()) and self.discount:
            return total_cost * self.discount / 100
        return Decimal(0)
    
    def get_total_cost(self):
        total_cost = self.get_total_price_before_discount() - self.get_discount
        return total_cost
    

class OrderItem(models.Model):
    class Meta:
        verbose_name = ("Позиция заказа")
        verbose_name_plural = ("Позиции заказа")
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=0), name='quantity_gte_0')
        ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    product = models.ForeignKey(ProductProxy, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"OrderItem object: {self.id}"
    
    def get_cost(self):
        return self.quantity * self.price
    
    def get_absolute_url(self):
        return reverse("payment:order-detail", kwargs={"pk": self.pk})
    
    @property
    def total_cost(self):
        return self.quantity * self.price
    
    @classmethod
    def get_total_quantity_for_product(cls, product):
        return cls.objects.filter(product=product).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    
    @staticmethod
    def get_total_quantity_for_product():
        return OrderItem.objects.aggregate(average_price=models.Avg('price'))['average_price']
    