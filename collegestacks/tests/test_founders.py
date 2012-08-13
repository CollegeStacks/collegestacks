from django.test import TestCase
class TestFoundersSuite(TestCase):

    def test_has_about_url(self):
        url = '/about'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_has_founders_name_on_page(self):
        url = '/about'
        response = self.client.get(url)
        print(response.content)
        self.assertIn('Atthaphong Limsupanark',response.content)
        self.assertIn("Wattanai Lattikul", response.content)
        self.assertIn('Thitikom Yansombat', response.content)
        self.assertIn("Khemin Kongchumnian", response.content)