from django.test import TestCase
from django.urls import reverse, resolve


class TestProductURLs(TestCase):
    def test_urls(self):
        self.assertEqual(reverse('product:main'), '/product/')
        self.assertEqual(reverse('product:create'), '/product/create/')
        self.assertEqual(reverse('product:update', kwargs={'id': 1}), '/product/update/1/')
        self.assertEqual(reverse('product:delete'), '/product/delete/')
        self.assertEqual(resolve('/product/').view_name, 'product:main')
        self.assertEqual(resolve('/product/create/').view_name, 'product:create')
        self.assertEqual(resolve('/product/update/1/').view_name, 'product:update')
        self.assertEqual(resolve('/product/delete/').view_name, 'product:delete')
