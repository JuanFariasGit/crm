from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from product.models import Product
from stock_exit.models import StockExit
from store.models import Store


class TestStockExitModels(TestCase):
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
        store = Store.objects.create(
            user=user,
            store='Loja 1',
            phone='81 9 9999-9999',
            email='loja1@gmail.com',
            address='Rua Loja 1'
        )
        self.stock_exit = StockExit.objects.create(
            user=user,
            date_of_sale=date(2021, 8, 26),
            product=product,
            store=store,
            quantity=100,
            price_unit=2.15
        )

    def test__str__(self):
        self.assertEqual(self.stock_exit.__str__(), 'Caneta azul (Bic)')

    def test_get_absolute_url(self):
        self.assertEqual(self.stock_exit.get_absolute_url(), '/stock_exit/')

    def test_get_date_of_sale(self):
        self.assertEqual(self.stock_exit.get_date_of_sale(), '26/08/2021')

    def test_get_price_unit(self):
        self.assertEqual(self.stock_exit.get_price_unit(), 'R$ 2,15')

    def test_get_total_sale(self):
        self.assertEqual(self.stock_exit.get_total_sale(), 'R$ 215,00')

    def test_get_link_update(self):
        self.assertEqual(self.stock_exit.get_link_update(), '<a href="update/1/">26/08/2021</a>')

    def test_get_button_delete(self):
        self.assertEqual(self.stock_exit.get_button_delete(),
                         '<button class="btn btn-danger" onclick="deleteStockExitModal(\'1\','
                                                              '\'26/08/2021\',\'Caneta azul (Bic)\')">'
                                                              '<i class="far fa-trash-alt fa-lg"></i></button>')
