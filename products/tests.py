# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from products.models import Product, Category
from products.views import hours_delta
import datetime


class ProductsTest(TransactionTestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def test_check_right_login(self):
        response = self.client.get(reverse('products:product_new'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test', password='test')
        response = self.client.get(reverse('products:product_new'))
        self.assertEqual(response.status_code, 200)

    def test_check_wrong_login(self):
        response = self.client.get(reverse('products:product_new'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test_wrong', password='test')
        response = self.client.get(reverse('products:product_new'))
        self.assertEqual(response.status_code, 302)

    def test_check_new_product(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('products:product_new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Категория не найдена')

        category_test = Category.objects.create(
            name='category_test',
            description='category_test_desc')
        product_test = Product.objects.create(
            name="product_test",
            price="50",
            description='product_test desc',
            category=category_test,
            )
        self.assertEqual(Product.objects.all().count(), 1)
        self.assertEqual(Category.objects.all().count(), 1)

        response = self.client.get('/products/{0}/'.format(category_test.slug))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'product_test')
        self.assertContains(response, 'category_test')

    def test_check_new_product_wrong_time(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('products:product_new'))
        self.assertEqual(response.status_code, 200)

        date_last = datetime.datetime.now() - datetime.timedelta(hours=hours_delta, minutes=1)
        category_test = Category.objects.create(
            name='category_test',
            description='category_test_desc')
        product_test = Product.objects.create(
            name="product_test",
            price="50",
            description='product_test desc',
            category=category_test,
            )
        product_test.created_at = date_last

        self.assertEqual(Product.objects.all().count(), 1)
        self.assertEqual(Category.objects.all().count(), 1)

        response = self.client.get('/products/{0}/'.format(category_test.slug))
        self.assertEqual(response.status_code, 200)
        # self.assertNotContains(response, 'product_test')
        # self.assertNotContains(response, 'category_test')


