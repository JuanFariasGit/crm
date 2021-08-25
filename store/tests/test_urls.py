from django.test import TestCase
from django.urls import reverse, resolve


class TestStoreURLs(TestCase):
    def test_urls(self):
        self.assertEqual(reverse('store:main'), '/store/')
        self.assertEqual(reverse('store:list'), '/store/list/')
        self.assertEqual(reverse('store:create'), '/store/create/')
        self.assertEqual(reverse('store:update', kwargs={'id': 1}), '/store/update/1/')
        self.assertEqual(reverse('store:delete'), '/store/delete/')
        self.assertEqual(resolve('/store/').view_name, 'store:main')
        self.assertEqual(resolve('/store/list/').view_name, 'store:list')
        self.assertEqual(resolve('/store/create/').view_name, 'store:create')
        self.assertEqual(resolve('/store/update/1/').view_name, 'store:update')
        self.assertEqual(resolve('/store/delete/').view_name, 'store:delete')
