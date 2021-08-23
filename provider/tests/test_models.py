from django.contrib.auth.models import User
from django.test import TestCase

from provider.models import Provider


class TestProviderModels(TestCase):
    def setUp(self):
        self.provider = Provider.objects.create(
            user=User.objects.create_user(username='juanfarias', password='12345'),
            company='Fornecedor 1',
            phone='81 9 9999-9999',
            email='fornecedo1@gmail.com',
            address='Rua fornecedor 1'
        )

    def test_get_absolute_url(self):
        self.client.login(username='juanfarias', password='12345')
        self.assertEqual(self.provider.get_absolute_url(), '/provider/')

    def test_company(self):
        self.client.login(username='juanfarias', password='12345')
        self.assertEqual(self.provider.company, 'Fornecedor 1')
