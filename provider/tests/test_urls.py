from django.test import TestCase
from django.urls import reverse, resolve


class TestProviderURLs(TestCase):
    def test_urls(self):
        self.assertEqual(reverse('provider:main'), '/provider/')
        self.assertEqual(reverse('provider:list'), '/provider/list/')
        self.assertEqual(reverse('provider:create'), '/provider/create/')
        self.assertEqual(reverse('provider:update', kwargs={'id': 1}), '/provider/update/1/')
        self.assertEqual(reverse('provider:delete'), '/provider/delete/')
        self.assertEqual(resolve('/provider/').view_name, 'provider:main')
        self.assertEqual(resolve('/provider/list/').view_name, 'provider:list')
        self.assertEqual(resolve('/provider/create/').view_name, 'provider:create')
        self.assertEqual(resolve('/provider/update/1/').view_name, 'provider:update')
        self.assertEqual(resolve('/provider/delete/').view_name, 'provider:delete')
