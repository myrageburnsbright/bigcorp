from django.urls import path   
from .views import product_view, ProductListView, category_list, search_product

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('search_product/', search_product, name='search_product'),
    path('search/<slug:slug>/', category_list, name='category_list'),
    path('<slug:slug>/', product_view, name='product'),
]