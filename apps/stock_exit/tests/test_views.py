from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from apps.product.models import Product
from apps.provider.models import Provider
from apps.stock_entry.models import StockEntry
from apps.stock_exit.models import StockExit
from apps.store.models import Store


class TestStockExitViews(TestCase):
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
        provider = Provider.objects.create(
            user=user,
            company='Fornecedor 1',
            phone='81 9 9999-9999',
            email='fornecedo1@gmail.com',
            address='Rua fornecedor 1'
        )
        StockEntry.objects.create(
            user=user,
            purchase_date=date(2021, 8, 26),
            product=product,
            provider=provider,
            quantity=200,
            cost_unit=1.25
        )
        self.stock_exit = StockExit.objects.create(
            user=user,
            date_of_sale=date(2021, 8, 26),
            product=product,
            store=store,
            quantity=100,
            price_unit=2.15
        )

    def test_main(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.get('/stock_exit/')
        self.assertEqual(resp.status_code, 200)

    def test_list(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/stock_exit/list/', follow=True)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'), {'data': [
            {
                "DT_RowId": f"row_1",
                "ID": 1,
                "Data da Venda": '<a href="update/1/">26/08/2021</a>',
                "Produto": 'Caneta azul (Bic)',
                "Loja": 'Loja 1',
                "Quantidade": 100,
                "Preço Unitário": 'R$ 2,15',
                "Total": 'R$ 215,00',
                "": '<button class="btn btn-danger" onclick="deleteStockExitModal(\'1\','
                    '\'26/08/2021\',\'Caneta azul (Bic)\')">'
                    '<i class="far fa-trash-alt fa-lg"></i></button>'
            }
        ]})

    def test_create(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_exit/create/',
            {
                'date_of_sale': date(2021, 8, 26),
                'product': 1,
                'store': 1,
                'quantity': 100,
                'price_unit': 3.25
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Saída cadastrada com sucesso !')

    def test_create_clean_quantity(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_exit/create/',
            {
                'date_of_sale': date(2021, 8, 26),
                'product': 1,
                'store': 1,
                'quantity': 200,
                'price_unit': 3.25
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao cadastrar saída !')
        self.assertFormError(resp, 'form', 'quantity', 'Disponível em estoque 100 Caneta azul (Bic).')

    def test_create_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_exit/create/',
            {
                'date_of_sale': date(2021, 8, 26),
                'product': '',
                'store': 1,
                'quantity': 200,
                'price_unit': 3.25
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao cadastrar saída !')
        self.assertFormError(resp, 'form', 'product', 'Este campo é obrigatório.')

    def test_update(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_exit/update/1/',
            {
                'id': 1,
                'date_of_sale': date(2021, 8, 26),
                'product': 1,
                'store': 1,
                'quantity': 120,
                'price_unit': 3.25
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Saída atualizada com sucesso !')

    def test_update_clean_quantity(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_exit/update/1/',
            {
                'id': 1,
                'date_of_sale': date(2021, 8, 26),
                'product': 1,
                'store': 1,
                'quantity': 250,
                'price_unit': 3.25
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao atualizar saída !')
        self.assertFormError(resp, 'form', 'quantity', 'Disponível em estoque 200 Caneta azul (Bic).')

    def test_update_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_exit/update/1/',
            {
                'id': 1,
                'date_of_sale': date(2021, 8, 26),
                'product': '',
                'store': 1,
                'quantity': 250,
                'price_unit': 3.25
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao atualizar saída !')
        self.assertFormError(resp, 'form', 'product', 'Este campo é obrigatório.')

    def test_delete_status_200(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/stock_exit/delete/', {'id': 1}, follow=True)
        self.assertEquals(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'),
                             {'type': 'success', 'message': 'Saída deletada com sucesso !'})

    def test_delete_status_404(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/stock_exit/delete/', {'id': 2}, follow=True)
        self.assertEquals(resp.status_code, 404)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'),
                             {'type': 'danger', 'message': 'Saída inexistente !'})
