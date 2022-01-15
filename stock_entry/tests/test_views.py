from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from product.models import Product
from provider.models import Provider
from stock_entry.models import StockEntry


class TestStockEntryViews(TestCase):
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
        StockEntry.objects.create(
            user=user,
            purchase_date=date(2021, 8, 26),
            product=product,
            provider=provider,
            quantity=100,
            cost_unit=1.25
        )

    def test_main(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.get('/stock_entry/')
        self.assertEqual(resp.status_code, 200)

    def test_list(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/stock_entry/list/', follow=True)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'), {'data': [
            {
                "DT_RowId": "row_1",
                "ID": 1,
                "Data da Compra": '<a href="update/1/">26/08/2021</a>',
                "Produto": "Caneta azul (Bic)",
                "Data de Validade": "Sem validade",
                "Fornecedor": "Fornecedor 1",
                "Quantidade": 100,
                "Custo Unitário": "R$ 1,25",
                "Total": "R$ 125,00",
                "": '<button class="btn btn-danger" onclick="deleteStockEntryModal(\'1\','
                    '\'26/08/2021\',\'Caneta azul (Bic)\')">'
                    '<i class="far fa-trash-alt fa-lg"></i></button>'
            }
        ]})

    def test_create(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_entry/create/',
            {
                'purchase_date': date(2021, 8, 27),
                'product': 1,
                'provider': 1,
                'quantity': 100,
                'cost_unit': 1.45
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Entrada cadastrada com sucesso !')

    def test_create_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_entry/create/',
            {
                'purchase_date': date(2021, 8, 27),
                'product': '',
                'provider': 1,
                'quantity': 100,
                'cost_unit': 1.45
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao cadastrar entrada !')
        self.assertFormError(resp, 'form', 'product', 'Este campo é obrigatório.')

    def test_update(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_entry/update/1/',
            {
                'id': 1,
                'purchase_date': date(2021, 8, 27),
                'product': 1,
                'provider': 1,
                'quantity': 100,
                'cost_unit': 1.99
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Entrada atualizada com sucesso !')

    def test_update_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/stock_entry/update/1/',
            {
                'id': 1,
                'purchase_date': date(2021, 8, 27),
                'product': '',
                'provider': 1,
                'quantity': 100,
                'cost_unit': 1.45
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao atualizar entrada !')
        self.assertFormError(resp, 'form', 'product', 'Este campo é obrigatório.')

    def test_delete_status_200(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/stock_entry/delete/', {'id': 1}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'),
                             {'type': 'success', 'message': 'Entrada deletada com sucesso !'})

    def test_delete_status_404(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/stock_entry/delete/', {'id': 2}, follow=True)
        self.assertEqual(resp.status_code, 404)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'),
                             {'type': 'danger', 'message': 'Entrada inexistente !'})
