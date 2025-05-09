from calendar import c
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Category, ProductProxy
from django.shortcuts import redirect
from django.contrib import messages
# def products_view(request):
#     products = ProductProxy.objects.all()
#     return render(request, "shop/products.html", {"products": products})

class ProductListView(ListView):
    model = ProductProxy
    context_object_name = "products"
    paginate_by = 15

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return "shop/components/product_list.html"
        return "shop/products.html"
    


# def product_view(request, slug):
#     product = get_object_or_404(ProductProxy, slug=slug)
#     return render(request, "shop/product_detail.html", {"product": product})
def product_view(request, slug):
    product = get_object_or_404(
        ProductProxy.objects.select_related('category'), slug=slug)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if product.reviews.filter(created_by=request.user).exists():
                messages.error(
                    request, 'You have already made a review for this product.')
            else:
                rating = request.POST.get('rating', 3)
                content = request.POST.get('content', '')
                if content:
                    product.reviews.create(
                        rating=rating, content=content, created_by=request.user, product=product)
                    return redirect(request.path)
        else:
            messages.error(
                request, 'You need to be logged in to make a review.')

    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related("category").filter(category=category)
    context = {"category": category, "products": products}

    return render(request, "shop/category_list.html", context=context)

def search_product(request):
    query = request.GET.get('q')
    products = ProductProxy.objects.filter(title__icontains=query).distinct()
    context = {"products": products}
    if not query or not products:
        return redirect('shop:products')
    return render( request, "shop/products.html", context=context)     
