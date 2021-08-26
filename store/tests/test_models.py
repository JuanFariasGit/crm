from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Store


class TestStoreModels(TestCase):
    def setUp(self):
        self.store = Store.objects.create(
            user=User.objects.create_user(username='juanfarias', password='12345'),
            store='Loja 1',
            phone='81 9 9999-9999',
            email='loja1@gmail.com',
            address='Rua Loja 1'
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.store.get_absolute_url(), '/store/')

    def test_get_link_update(self):
        self.assertEqual(self.store.get_link_update(), '<a href="update/1/">Loja 1</a>')

    def test_get_button_delete(self):
        self.assertEqual(self.store.get_button_delete(),
                         '<button class="btn btn-danger" onclick="deleteStoreModal(\'1\',\'Loja 1\')">'
                         '<i class="far fa-trash-alt fa-lg"></i></button>')
