from django.contrib.auth.models import User
from django.test import TestCase

from product.models import Product


class TestProductModels(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            user=User.objects.create_user(username='juanfarias', password='12345'),
            item='Caneta azul (Bic)',
            code='P001',
            unit_of_measure='unidade',
            level_minimum=50,
            level_maximum=150
        )

    def test_get_absolute_url(self):
        self.client.login(username='juanfarias', password='12345')
        self.assertEqual(self.product.get_absolute_url(), '/product/')

    def test_item(self):
        self.client.login(username='juanfarias', password='12345')
        self.assertEqual(self.product.item, 'Caneta azul (Bic)')
        self.assertEqual(self.product.user.username, 'juanfarias')
