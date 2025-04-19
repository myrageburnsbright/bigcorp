from calendar import c
from django.shortcuts import render, get_object_or_404
from shop.models import ProductProxy, Category
from .cart import Cart
from django.http import JsonResponse

def cart_view(request):
    ctx = {
        'cart': Cart(request)
    }
    return render(request, 'cart/cart-view.html')
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.add(product=product, quantity = product_qty)

        cart_qty = cart.__len__()

        ctx = {
            'qty': cart_qty,
            'product': product.title    
        }

        return JsonResponse(ctx)
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.update(product=product, quantity=product_qty)

        cart_qty = cart.__len__()
        
        cart_total_price = cart.get_total_price()

        ctx = {
            'qty': cart_qty,
            'total': cart_total_price    
        }

        return JsonResponse(ctx)
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.delete(product=product)

        cart_qty = cart.__len__()
        
        cart_total_price = cart.get_total_price()

        ctx = {
            'qty': cart_qty,
            'total': cart_total_price    
        }

        return JsonResponse(ctx)



