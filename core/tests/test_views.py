from django.contrib.auth.models import User
from django.test import TestCase


class TestCoreViews(TestCase):
    def setUp(self):
        User.objects.create_user(username='juanfarias', password='12345')

    def test_dashboard(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.get('')
        self.assertContains(resp, 0)
        self.assertContains(resp, 'R$ 0,00')
        self.assertEqual(resp.status_code, 200)

    def test_inventory(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.get('/inventory/')
        self.assertEqual(resp.status_code, 200)

    def test_inventory_data(self):
        self.client.login(username='juanfarias', password='12345')
        resp = self.client.get('/inventory/data/')
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf-8'), {'data': []})
