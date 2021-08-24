from django.contrib.auth.models import User
from django.test import TestCase

from product.models import Product


class TestProductViews(TestCase):
    def setUp(self):
        Product.objects.create(
            user=User.objects.create_user(username='juanfarias', password='12345'),
            item='Caneta azul (Bic)',
            code='P001',
            unit_of_measure='unidade',
            level_minimum=50,
            level_maximum=150
        )

    def test_main(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.get('/product/')
        self.assertEqual(resp.status_code, 200)

    def test_list(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/product/list/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'), {'data': [
            {
                "DT_RowId": "row_1",
                "Item": "<a href=\"update/1/\">Caneta azul (Bic)</a>",
                "Código do Produto": "P001",
                "Unidade de Medida": "unidade",
                "Estoque Mínimo": 50,
                "Estoque Máximo": 150,
                "": "<button class=\"btn btn-danger\" onclick=\"deleteProductModal('1','Caneta azul (Bic)')\">"
                    "<i class=\"far fa-trash-alt fa-lg\"></i></button>"
            }
        ]
        })

    def test_create(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/product/create/',
            {
                'item': 'Caneta preta (Bic)',
                'code': 'P002',
                'unit_of_measure': 'unidade',
                'level_minimum': 50,
                'level_maximum': 100
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Produto cadastrado com sucesso !')

    def test_create_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/product/create/',
            {
                'item': 'Caneta preta (Bic)',
                'code': '',
                'unit_of_measure': 'unidade',
                'level_minimum': 50,
                'level_maximum': 100
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao cadastrar produto !')
        self.assertFormError(resp, 'form', 'code', 'Este campo é obrigatório.')

    def test_update(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/product/update/1/',
            {
                'id': 1,
                'item': 'Caneta azul (Bic)',
                'code': 'P001',
                'unit_of_measure': 'unidade',
                'level_minimum': 50,
                'level_maximum': 150
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Produto atualizado com sucesso !')

    def test_update_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/product/update/1/',
            {
                'id': 1,
                'item': 'Caneta azul (Bic)',
                'code': '',
                'unit_of_measure': 'unidade',
                'level_minimum': 50,
                'level_maximum': 150
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao atualizar produto !')
        self.assertFormError(resp, 'form', 'code', 'Este campo é obrigatório.')

    def test_delete_status_200(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/product/delete/', {'id': 1}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'),
                             {'type': 'success', 'message': 'Produto deletado com sucesso !'})

    def test_delete_status_404(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/product/delete/', {'id': 2}, follow=True)
        self.assertEqual(resp.status_code, 404)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'),
                             {'type': 'danger', 'message': 'Produto inexistente !'})
