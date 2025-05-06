from django.urls import path

from payment import webhooks
from . import views
from django.shortcuts import render

app_name='payment'

urlpatterns = [
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    path('shipping/', views.shipping, name='shipping'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete-order/', views.complete_order, name='complete-order'),
    path('webhook-stripe/', webhooks.stripe_webhook, name='webhooks'),
    path('my_webhook_view/', webhooks.my_webhook_view, name='my_webhook_view'),
    path('order/<int:order_id>/pdf', views.admin_order_pdf, name='admin_order_pdf'),
]