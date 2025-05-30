import weasyprint
from decimal import Decimal
import string
import uuid
from django.templatetags.static import static
from django.utils.http import urlencode
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
import stripe
from cart.cart import Cart
from yookassa import Configuration, Payment
from .forms import ShippingAdressForm
from .models import ShippingAdress, Order, OrderItem
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

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
        shipping_address = ShippingAdress.objects.filter(user=request.user).first()
        if shipping_address:
            return render(
                request, "payment/checkout.html", {"shipping_address": shipping_address}
            )
        else:
            messages.error(request, "Please add shipping address")
            return redirect(reverse("payment:shipping"))
    
    messages.error(request, "Please authorize")
    url = reverse("account:login") + "?" + urlencode({"next": reverse("cart:cart-view")})
    return redirect(url)

@login_required
def complete_order(request):
    if request.method == "POST":
        payment_type = request.POST.get("stripe-payment",'yookassa-payment')

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
        
        match payment_type:
            case "stripe-payment":
                session_data = {
                    'mode' : 'payment',
                    'success_url' : request.build_absolute_uri(reverse('payment:payment-success')),
                    'cancel_url' : request.build_absolute_uri(reverse('payment:payment-failed')),
                    'line_items' : []
                }
                
                if request.user.is_authenticated:
                    try:
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
                            session_data['line_items'].append({
                                'price_data' : {
                                    'currency' : 'usd',
                                    'unit_amount' : int(item['price'] * Decimal(100)),
                                    'product_data' : {
                                        'name' : item['product'].title
                                    }
                                },
                                'quantity' : item['qty'],
                            })
                        session_data['client_reference_id'] = str(order.id)
                        session = stripe.checkout.Session.create(**session_data)
                        return redirect(session.url, code=303)
                    except Exception as e:
                        messages.error(request, f"{e}")
                        return redirect(reverse("cart:cart-view"))
                else:
                    messages.error(request, "Please authorize")
                    url = reverse("account:login") + "?" + urlencode({"next": reverse("cart:cart-view")})
                    return redirect(url)
            case "yookassa-payment":
                idempotence_key = uuid.uuid4()
                currency = "RUB"
                description = "товары в корзине"
                payment=Payment.create({
                    'amount' : {
                        "value" : str(total_price * 93),
                        "currency" : currency
                    },
                    "confirmation" : {
                        "type": "redirect",
                        "return_url" : request.build_absolute_uri(reverse('payment:payment-success')),
                        "cancel_url" : request.build_absolute_uri(reverse('payment:payment-failed'))
                    
                    },
                    "capture" : True,
                    'test' : True,
                    "description" : description, 
                }, idempotence_key)

                confirmation_url = payment.confirmation.confirmation_url
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
                return redirect(confirmation_url)

                    
def payment_success(request):
    del request.session['session_key'] #delete cart
    return render(request, "payment/payment-success.html")    


def payment_failed(request):
    return render(request, "payment/payment-failed.html")

@staff_member_required
def admin_order_pdf(request, order_id):
    try:
        order = Order.objects.select_related('user', 'shipping_address').get(id=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")
    
    html = render_to_string('payment/order/pdf/pdf_invoice.html', {'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    css_path=static('payment/css/pdf.css').lstrip('/')
    stylesheets = [weasyprint.CSS(css_path)]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
    return response
