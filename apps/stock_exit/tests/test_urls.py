from django.test import TestCase
from django.urls import reverse, resolve


class TestStockExitURLs(TestCase):
    def test_urls(self):
        self.assertEqual(reverse('stock_exit:main'), '/stock_exit/')
        self.assertEqual(reverse('stock_exit:list'), '/stock_exit/list/')
        self.assertEqual(reverse('stock_exit:create'), '/stock_exit/create/')
        self.assertEqual(reverse('stock_exit:update', kwargs={'id': 1}), '/stock_exit/update/1/')
        self.assertEqual(reverse('stock_exit:delete'), '/stock_exit/delete/')
        self.assertEqual(resolve('/stock_exit/').view_name, 'stock_exit:main')
        self.assertEqual(resolve('/stock_exit/list/').view_name, 'stock_exit:list')
        self.assertEqual(resolve('/stock_exit/create/').view_name, 'stock_exit:create')
        self.assertEqual(resolve('/stock_exit/update/1/').view_name, 'stock_exit:update')
        self.assertEqual(resolve('/stock_exit/delete/').view_name, 'stock_exit:delete')
