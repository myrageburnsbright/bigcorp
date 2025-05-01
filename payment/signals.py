from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShippingAdress

User = get_user_model()

@receiver(post_save, sender=User)
def create_default_shipping_address(sender, instance, created, **kwargs):
    print("SIGNAL CHECK!")
    if created:
        if not ShippingAdress.objects.filter(user=instance).exists():
            ShippingAdress.create_default_shipping_address(user=instance)