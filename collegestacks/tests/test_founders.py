import unittest
from django.test import Client
from app.models import *
import os.path

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

    def test_zadd_link(self):
        print(Course.objects.count())
        u = University.objects.create(name='Kasetsart',abbr='ku')
        f = Faculty.objects.create(name='Engineering',abbr='eng',university=u)
        d = Department.objects.create(name='Computer Engineering', abbr='cpe', faculty=f)
        c = Course.objects.create(title="Formal Language_edit",abbr="formal",code='12345',university=u,faculty=f,department=d,description="fuck you thunder")
        url = '/course/%d/upLink'%c.id
        context = {
            'name' : 'test link name',
            'description' : 'desc test link name na ja',
            'type' : 'link',
            'sourceLink' : 'www.wikipedia.com',
            'docfile' : None,
            }
        response = self.client.post(url,context,follow=True)
        print(response.content)
        self.assertEqual(response.status_code,200)
        self.assertIn('test link name',response.content)
        self.assertIn('www.wikipedia.com',response.content)
#        self.assertIn('desc test link name na ja',response.content)


    def test_upload_file(self):
        u = University.objects.create(name='Kasetsart',abbr='ku')
        f = Faculty.objects.create(name='Engineering',abbr='eng',university=u)
        d = Department.objects.create(name='Computer Engineering', abbr='cpe', faculty=f)
        c = Course.objects.create(title="Formal Language_edit",abbr="formal",code='12345',university=u,faculty=f,department=d,description="fuck you thunder")

        PROJECT_DIR = os.path.dirname(__file__)

        uploadFile = open(PROJECT_DIR+os.sep+'test_files'+os.sep+'testUpload.txt')
        context = (
            {
                'name':'test',
                'description':'test upload file',
                'docfile':uploadFile,
            }
        )
        response = self.client.post('/course/%d/uploadFile'%c.id, context, follow=True)
        uploadFile.close()
        print(PROJECT_DIR)
        #print(response.status_code)
        self.assertEqual(response.status_code,200)
        #print(response.content)
        self.assertIn('test', response.content)
        #self.fail()

    def test_upload_file_fail(self):
        context = (
                {
                'name':'test2',
                'description':'test upload file',
                'docfile':''
                }
            )
        response = self.client.post('/course/1/uploadFile', context, follow=True)
        self.assertEqual(response.status_code,200)
        self.assertIn('Please fill all information', response.content)
        self.assertIn('course/1',response.__str__())

    def test_download_file(self):
        u = University.objects.create(name='Kasetsart',abbr='ku')
        f = Faculty.objects.create(name='Engineering',abbr='eng',university=u)
        d = Department.objects.create(name='Computer Engineering', abbr='cpe', faculty=f)
        c = Course.objects.create(title="Formal Language_edit",abbr="formal",code='12345',university=u,faculty=f,department=d,description="fuck you thunder")

        PROJECT_DIR = os.path.dirname(__file__)

        uploadFile = open(PROJECT_DIR + os.sep + 'test_files' + os.sep + 'testUpload.txt')
        context = (
            {
                'name': 'test_upload_file',
                'description': 'test upload file',
                'docfile': uploadFile,
            }
        )
        response = self.client.post('/course/%d/uploadFile'%c.id, context, follow=True)
        uploadFile.close()

        url = '/course/%d'%c.id
        response = self.client.get(url)
        rid = Resource.objects.get(name='test_upload_file').id
        url_file_to_test = '/course/resource/download/%d' % rid
        self.assertIn('<a href="%s">download</a>' % url_file_to_test, response.content)
        response = self.client.get(url_file_to_test)
        self.assertEqual(response.status_code, 200)