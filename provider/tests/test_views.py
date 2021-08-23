from django.contrib.auth.models import User
from django.test import TestCase

from provider.models import Provider


class TestProviderViews(TestCase):
    def setUp(self):
        Provider.objects.create(
            user=User.objects.create_user(username='juanfarias', password='12345'),
            company='Fornecedor 1',
            phone='81 9 9999-9999',
            email='fornecedo1@gmail.com',
            address='Rua Fornecedor 1'
        )

    def test_main(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.get('/provider/')
        self.assertEqual(resp.status_code, 200)

    def test_list(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/provider/list/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/provider/create/',
            {
                'company': 'Fornecedor 2',
                'phone': '81 9 8888-8888',
                'email': 'fornecedor2@gmail.com',
                'address': 'Rua Fornecedor 2'
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Fornecedor cadastrado com sucesso !')

    def test_create_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/provider/create/',
            {
                'company': 'Fornecedor 2',
                'phone': '',
                'email': 'fornecedor2@gmail.com',
                'address': 'Rua Fornecedor 2'
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Erro ao cadastrar fornecedor !')
        self.assertFormError(resp, 'form', 'phone', 'Este campo é obrigatório.')

    def test_update(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/provider/update/1/',
            {
                'id': 1,
                'company': 'Fornecedor 1',
                'phone': '81 9 7777-7777',
                'email': 'fornecedor1@hotmail.com.br',
                'address': 'Ruan Fornecedor 1'
            },
            follow=True
        )
        self.assertContains(resp, 'juanfarias')
        self.assertContains(resp, 'Fornecedor atualizado com sucesso !')

    def test_update_field_required(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post(
            '/provider/update/1/',
            {
                'id': 1,
                'company': 'Fornecedor 1',
                'phone': '',
                'email': 'fornecedor1@hotmail.com.br',
                'address': 'Ruan Fornecedor 1'
            }
        )
        self.assertContains(resp, 'juanfarias')
        self.assertFormError(resp, 'form', 'phone', 'Este campo é obrigatório.')

    def test_delete_status_200(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/provider/delete/', {'id': 1}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf8'),
                             {'type': 'success', 'message': 'Fornecedor deletado com sucesso !'})

    def test_delete_status_404(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.post('/provider/delete/', {'id': 2}, follow=True)
        self.assertEqual(resp.status_code, 404)
        self.assertJSONEqual(str(resp.content, encoding='utf8'),
                             {'type': 'danger', 'message': 'Fornecedor inexistente !'})
