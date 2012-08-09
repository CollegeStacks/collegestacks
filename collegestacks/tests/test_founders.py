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
        #self.fail("Not Implement Yet")

    def test_course_model(self):
        self.uni1 = University.objects.create(name="Chulalongkorn")
        self.faculty1 = Faculty.objects.create(name="Engineering")
        self.course1 = Course.objects.create(title="Formal Language", abbr="Formal Lang", code="2110399",
            description="abc",university=self.uni1,faculty=self.faculty1)
        self.assertEquals(self.uni1.name,'Chulalongkorn') #****************************************************

    def test_create_course_success(self):
        context = {
            'title' : 'noly',
            'code' : '2110455',
            'abbr' : 'form',
            'university' : '1',
            'faculty' : '1',
            'description' : 'test'
        }
        url = '/course/new'
        response = self.client.post(url,context)
        print(response)
        self.assertEqual(response.status_code,302)
        course1 = Course.objects.get(title='noly')
        print(Course.objects.all())
        self.assertIn('course/%d'%course1.id,response.__str__())

    def test_create_course_fail(self):
        context = {
            'title' : 'noly',
            'code' : '2110455',
            'abbr' : 'form',
            'university' : '',
            'faculty' : '',
            'description' : ''
        }
        url = '/course/new'
        response = self.client.post(url,context)
        print(response)
        self.assertEqual(response.status_code,200)
        self.assertIn('please',response.content)


    def test_course_id(self):
        #test case for CS-04 View Course story card --noly

        #add new course to db
        u = University.objects.create(name="Chulalongkorn")
        f = Faculty.objects.create(name="Engineering")
        c = Course.objects.create(title="Formal Language", code="2110399", abbr="FORM LANG",university=u, faculty=f)
        c.save()

        #retrieve course from http call to test
        url = '/course/%(id)d'%{"id":c.id}
        response = self.client.get(url)
        rc = response.content
        print(rc)

        self.assertEqual(response.status_code,200)
        self.assertIn(c.title, rc)
        self.assertIn(c.code, rc)
        self.assertIn(c.abbr, rc)
        self.assertIn(c.university.name, rc)
        self.assertIn(c.faculty.name, rc)




