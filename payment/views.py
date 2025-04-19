from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from cart.cart import Cart

from .forms import ShippingAdressForm
from .models import ShippingAdress, Order, OrderItem


@login_required
def shipping(request):
    try:
        shipping_address = ShippingAdress.objects.get(user=request.user)
    except ShippingAdress.DoesNotExist:
        shipping_address = None

    if request.method == "POST":
        form = ShippingAdressForm(instance=shipping_address, data=request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect(reverse("account:dashboard"))
    else:
        form = ShippingAdressForm(instance=shipping_address)

    context = {"form": form}
    return render(request, "shipping/shipping.html", context=context)


def checkout(request):
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAdress, user=request.user)
        if shipping_address:
            return render(
                request, "payment/checkout.html", {"shipping_address": shipping_address}
            )

    return redirect(reverse("payment:checkout"))


def complete_order(request):
    if request.method == "POST":
        if request.POST.get("action") == "payment":
            name = request.POST.get("name")
            email = request.POST.get("email")
            street_address = request.POST.get("street_address")
            apartment_address = request.POST.get("apartment_address")
            country = request.POST.get("country")
            city = request.POST.get("city")
            zip = request.POST.get("zip")

            cart = Cart(request)
            total_price = cart.get_total_price()

            shipping_address, _ = ShippingAdress.objects.get_or_create(
                user=request.user,
                defaults={
                    "full_name": name,
                    "email": email,
                    "street_address": street_address,
                    "apartment_address": apartment_address,
                    "country": country,
                    "city": city,
                    "zip": zip,
                },
            )

            if request.user.is_authenticated:
                order = Order.objects.create(
                    user=request.user,
                    amount=total_price,
                    shipping_address=shipping_address,
                )
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        price=item["price"],
                        quantity=item["qty"],
                        user=request.user,
                    )
            else:
                order = Order.objects.create(
                    amount=total_price,
                    shipping_address=shipping_address,
                )
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        price=item["price"],
                        quantity=item["qty"],
                    )
            return JsonResponse({"success": True })

def payment_success(request):
    for key in list(request.session.keys()):
        del request.session[key]

    return render(request, "payment/payment-success.html")    


def payment_failed(request):
    return render(request, "payment/payment-failed.html")
