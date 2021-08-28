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

    def test__str__(self):
        self.assertEqual(self.provider.__str__(), 'Fornecedor 1')

    def test_get_absolute_url(self):
        self.assertEqual(self.provider.get_absolute_url(), '/provider/')

    def test_get_link_update(self):
        self.assertEqual(self.provider.get_link_update(), '<a href="update/1/">Fornecedor 1</a>')

    def test_get_button_delete(self):
        self.assertEqual(self.provider.get_button_delete(),
                         '<button class="btn btn-danger" onclick="deleteProviderModal(\'1\',\'Fornecedor 1\')">'
                         '<i class="far fa-trash-alt fa-lg"></i></button>')
