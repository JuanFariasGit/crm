from django.contrib.auth.models import User
from django.test import TestCase

from product.models import Product
from provider.models import Provider
from stock_entry.models import StockEntry

from datetime import date


class TestStockEntryModels(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='juanfarias', password='12345')
        product = Product.objects.create(
            user=user,
            item='Caneta azul (Bic)',
            code='P001',
            unit_of_measure='unidade',
            level_minimum=50,
            level_maximum=150
        )
        provider = Provider.objects.create(
            user=user,
            company='Fornecedor 1',
            phone='81 9 9999-9999',
            email='fornecedo1@gmail.com',
            address='Rua fornecedor 1'
        )
        self.stock_entry = StockEntry.objects.create(
            user=user,
            purchase_date=date(2021, 8, 26),
            product=product,
            provider=provider,
            quantity=100,
            cost_unit=1.25
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.stock_entry.get_absolute_url(), '/stock_entry/')

    def test_get_purchase_date(self):
        self.assertEqual(self.stock_entry.get_purchase_date(), '26/08/2021')

    def test_get_total_purchase(self):
        self.assertEqual(self.stock_entry.get_total_purchase(), 'R$ 125,00')

    def test_get_cost_unit(self):
        self.assertEqual(self.stock_entry.get_cost_unit(), 'R$ 1,25')

    def test_get_expiration_date(self):
        self.assertEqual(self.stock_entry.get_expiration_date(), 'Sem validade')

    def test_get_link_update(self):
        self.assertEqual(self.stock_entry.get_link_update(), '<a href="update/1/">26/08/2021</a>')

    def test_get_button_delete(self):
        self.assertEqual(self.stock_entry.get_button_delete(),
                         '<button class="btn btn-danger" onclick="deleteStockEntryModal(\'1\','
                         '\'26/08/2021\',\'Caneta azul (Bic)\')">'
                         '<i class="far fa-trash-alt fa-lg"></i></button>')
