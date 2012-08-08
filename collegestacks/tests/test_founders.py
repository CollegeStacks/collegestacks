import unittest
from django.test import Client
from app.models import Course,University, Faculty

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

    def test_new_course_form(self):
        url = '/course/new'
        response = self.client.get(url)
        print(response.content)
        self.assertIn("form",response.content)
        self.fail("Not Implement Yet")

    def test_course_model(self):
        self.uni1 = University.objects.create(name="Chulalongkorn")
        self.faculty1 = Faculty.objects.create(name="Engineering")
        self.course1 = Course.objects.create(title="Formal Language", abbr="Formal Lang", code="2110399",
            description="abc",university=self.uni1,faculty=self.faculty1)
        self.assertEquals(self.uni1.name,'Chulalongkorn')






