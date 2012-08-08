import unittest
from django.test import Client
from django.db import models

class TestFoundersSuite(unittest.TestCase):
    def setUp(self):
        self.client = Client()

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

class TestCourseSuite(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_course_url(self):
        url = '/course/new'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)




