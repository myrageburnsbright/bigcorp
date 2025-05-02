from django import forms
from .models import Order, OrderItem, ShippingAdress

class ShippingAdressForm(forms.ModelForm):
    class Meta:
        model = ShippingAdress
        fields = [
            'full_name',
            'email',
            'street_address',
            'apartment_address',
            'country',
            'city',
            'zip',
        ]
        exclude = ['user',]
        