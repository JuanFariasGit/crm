from django.test import TestCase
from django.urls import reverse, resolve


class TestStockEntryURLs(TestCase):
    def test_urls(self):
        self.assertEqual(reverse('stock_entry:main'), '/stock_entry/')
        self.assertEquals(reverse('stock_entry:list'), '/stock_entry/list/')
        self.assertEquals(reverse('stock_entry:create'), '/stock_entry/create/')
        self.assertEquals(reverse('stock_entry:update', kwargs={'id': 1}), '/stock_entry/update/1/')
        self.assertEquals(reverse('stock_entry:delete'), '/stock_entry/delete/')
        self.assertEquals(resolve('/stock_entry/').view_name, 'stock_entry:main')
        self.assertEqual(resolve('/stock_entry/create/').view_name, 'stock_entry:create')
        self.assertEqual(resolve('/stock_entry/update/1/').view_name, 'stock_entry:update')
        self.assertEqual(resolve('/stock_entry/delete/').view_name, 'stock_entry:delete')
