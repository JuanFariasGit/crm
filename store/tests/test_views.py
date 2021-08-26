from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Store


class TestStoreViews(TestCase):
    def setUp(self):
        Store.objects.create(
            user=User.objects.create_user(username='juanfarias', password='12345'),
            store='Loja 1',
            phone='81 9 9999-9999',
            email='loja1@gmail.com',
            address='Rua Loja 1'
        )

    def test_main(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.get('/store/')
        self.assertEqual(resp.status_code, 200)

    def test_list(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/store/list/')
        self.assertJSONEqual(str(resp.content, encoding='utf-8'), {'data': [
            {
                'DT_RowId': 'row_1',
                'Loja': '<a href="update/1/">Loja 1</a>',
                'Telefone': '81 9 9999-9999',
                'E-mail': 'loja1@gmail.com',
                'Endereço': 'Rua Loja 1',
                '': '<button class="btn btn-danger" onclick="deleteStoreModal(\'1\',\'Loja 1\')">'
                    '<i class=\"far fa-trash-alt fa-lg\"></i></button>'
            },
        ]})

    def test_create(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/store/create/',
            {
                'store': 'Loja 2',
                'phone': '81 9 8888-8888',
                'email': 'loja2@gmail.com',
                'address': 'Rua Loja 2'
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Loja cadastrada com sucesso !')

    def test_create_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/store/create/',
            {
                'store': 'Loja 2',
                'phone': '',
                'email': 'loja2@gmail.com',
                'address': 'Rua Loja 2'
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao cadastrar loja !')
        self.assertFormError(resp, 'form', 'phone', 'Este campo é obrigatório.')

    def test_update(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/store/update/1/',
            {
                'id': 1,
                'store': 'Loja 1',
                'phone': '81 9 7777-7777',
                'email': 'loja1@hotmail.com',
                'address': 'Rua Loja 1'
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Loja atualizada com sucesso !')

    def test_update_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/store/update/1/',
            {
                'id': 1,
                'store': 'Loja 1',
                'phone': '',
                'email': 'loja1@hotmail.com',
                'address': 'Rua Loja 1'
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao atualizar loja !')
        self.assertFormError(resp, 'form', 'phone', 'Este campo é obrigatório.')

    def teste_delete_status_200(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/store/delete/', {'id': 1}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'),
                             {'type': 'success', 'message': 'Loja deletada com sucesso !'})

    def test_delete_status_404(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/store/delete/', {'id': 2}, follow=True)
        self.assertEqual(resp.status_code, 404)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'),
                             {'type': 'danger', 'message': 'Loja inexistente !'})
