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

    def test__str__(self):
        self.assertEqual(self.product.__str__(), 'Caneta azul (Bic)')

    def test_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), '/product/')

    def test_get_link_update(self):
        self.assertEqual(self.product.get_link_update(), '<a href="update/1/">Caneta azul (Bic)</a>')

    def test_get_button_delete(self):
        self.assertEqual(self.product.get_button_delete(),
                         '<button class="btn btn-danger" onclick="deleteProductModal(\'1\',\'Caneta azul (Bic)\')">'
                         '<i class="far fa-trash-alt fa-lg"></i></button>')
