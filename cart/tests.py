from urllib import request
from django.test import TestCase
from decimal import Decimal
from django.contrib.sessions.middleware import SessionMiddleware

from django.test import Client,RequestFactory, TestCase
from django.urls import reverse

from shop.models import ProductProxy, Category

from .views import cart_view, cart_update, cart_add, cart_delete
import json
class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory().get(reverse('cart:cart-view'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        request = self.factory
        response = cart_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.client.get(reverse('cart:cart-view')), 'cart/cart-view.html')

class CartAddViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Category1', slug='category1')
        self.product = ProductProxy.objects.create(category=self.category, title='Product1', price=10.0, available=True)
        self.factory = RequestFactory().post(reverse('cart:cart-add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        request = self.factory
        response = cart_add(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 2)
        self.assertEqual(data['product'], "Product1")

class CartDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Category1', slug='category1')
        self.product = ProductProxy.objects.create(category=self.category, title='Product1', price=10.0, available=True)
        self.factory = RequestFactory().post(reverse('cart:cart-delete'), {
            'action': 'post',
            'product_id': self.product.id,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        request = self.factory
        response = cart_delete(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 0)    
        self.assertEqual(data['total'], 0.0)

class CartUpdateViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category1', slug='category1')
        self.product = ProductProxy.objects.create(category=self.category, title='Product1', price=10.0, available=True)
        self.factory = RequestFactory().post(reverse('cart:cart-add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 5
        })
        self.factory = RequestFactory().post(reverse('cart:cart-update'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 3
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        request = self.factory
        response = cart_add(request)
        response = cart_update(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 3)    
        self.assertEqual(Decimal(data['total']), 30.0)
