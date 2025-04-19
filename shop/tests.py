from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Product, Category, ProductProxy

class ProductsViewTest(TestCase):
    def test_get_products(self):
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )

    
        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django', slug='django')
        product_1 = Product.objects.create( 
            category=category,
            title='Product 1',
            slug='product-1',
            image=uploaded,
            description='Product 1 description',
            price=10.00,
            available=True
        )
        product_2 = Product.objects.create( 
            category=category, 
            title = 'Product 2',
            slug='product-2',
            image=uploaded,
            description='Product 2 description',
            price=20.00,
            available=True
        )

        response = self.client.get(reverse('shop:products'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/products.html')
        self.assertEqual(response.context['products'].count() , 2)
        self.assertEqual(list(response.context['products']), [product_1, product_2])
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)

class ProductViewTest(TestCase):
    def test_get_product(self):
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )
    
        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django', slug='django')
        product = Product.objects.create( 
            category=category,
            title='Product 1',
            slug='product-1',
            image=uploaded,
            description='Product 1 description',
            price=10.00,
            available=True
        )
        # product_proxy = ProductProxy.objects.filter(slug=product.slug).first()

        response = self.client.get(reverse('shop:product', kwargs={'slug': product.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['product'].slug, product.slug)

class CategoryListViewTest(TestCase):
    def setUp(self):
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(name='django', slug='django')
        self.product = ProductProxy.objects.create( 
            category=self.category,
            title='Product 1',
            slug='product-1',
            image=uploaded,
            available=True
        )
        
    def test_status_code(self):
        response = self.client.get(reverse('shop:category_list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
    
    def test_template_user(self):
        response = self.client.get(reverse('shop:category_list', args=[self.category.slug]))
        self.assertTemplateUsed(response, 'shop/category_list.html')

    def test_context_data(self):
        response = self.client.get(reverse('shop:category_list', args=[self.category.slug]))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)