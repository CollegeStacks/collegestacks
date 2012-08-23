import unittest
from django.test import Client
from app.models import Course,University, Faculty, Resource
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
        uni1 = University.objects.get_or_create(name="Chulalongkorn")[0]
        faculty1 = Faculty.objects.get_or_create(name="Engineering")[0]
        course1 = Course.objects.get_or_create(title="Formal Language", abbr="Formal Lang", code="2110399",
            description="abc",university=uni1,faculty=faculty1)[0]
        course1.save()
        c = Course.objects.get(pk=course1.id)
        self.assertEquals(c.title,'Formal Language')
        self.assertEqual(c.abbr, 'Formal Lang')
        self.assertEqual(c.code, '2110399')
        self.assertEqual(c.description,'abc')
        self.assertEqual(c.university.name,"Chulalongkorn")
        self.assertEqual(c.faculty.name,'Engineering')

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
        #CS-04 View Course

        #add new course to db
        u = University.objects.get_or_create(name="Chulalongkorn")[0]
        f = Faculty.objects.get_or_create(name="Engineering")[0]
        c = Course.objects.get_or_create(title="Software Engineering", code="2110333", abbr="SE",university=u, faculty=f)[0]
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

    def test_course_id_notfound(self):
        #CS-04 View Course
        id = len(Course.objects.all())+5
        url = '/course/%(id)d'% {'id':id}
        response = self.client.get(url)
        print(url)
        self.assertEqual(response.status_code,404)

    def test_zadd_link(self):
        print(Course.objects.count())
        c = Course.objects.filter(title="Formal Language_edit")[0]
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

    def test_edit_course(self):
        #CS-02: Edit Course
        #test edit url exists
        c = Course.objects.filter(title="Formal Language")[0]
        url = '/course/%d/edit'%c.id
        response = self.client.get(url)
        print (url)
        print (response.content)
        self.assertEqual(response.status_code, 200)

        self.assertIn(c.title, response.content)
        self.assertIn(c.abbr, response.content)
        self.assertIn(c.code, response.content)
        self.assertIn(c.description, response.content)
        self.assertIn('selected="selected">%s'%c.university.name, response.content)
        self.assertIn('selected="selected">%s'%c.faculty.name, response.content)

        #test post edited info
        u_e = University.objects.get_or_create(name='%s_edit'%c.university.name)[0]
        f_e = Faculty.objects.get_or_create(name='%s_edit'%c.faculty.name)[0]
        u_e.save()
        f_e.save()

        context = {
            'title' : '%s_edit'%c.title,
            'code' : '%s_edit'%c.code,
            'abbr' : '%s_edit'%c.abbr,
            'university' : u_e.id,
            'faculty' : f_e.id,
            'description' : '%s_edit'%c.description ,
        }
        url = '/course/%d/edit'%c.id
        response = self.client.post(url,context,follow=True)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn("<title>View Course</title>",response.content)
        self.assertIn('%s_edit'%c.title, response.content)
        self.assertIn('%s_edit'%c.code, response.content)
        self.assertIn('%s_edit'%c.abbr, response.content)
        self.assertIn('%s_edit'%c.description, response.content)
        self.assertIn(u_e.name, response.content)
        self.assertIn(f_e.name, response.content)

    def test_upload_file(self):
        PROJECT_DIR = os.path.dirname(__file__)

        uploadFile = open(PROJECT_DIR+os.sep+'test_files'+os.sep+'testUpload.txt')
        context = (
            {
                'name':'test',
                'description':'test upload file',
                'docfile':uploadFile,
            }
        )
        response = self.client.post('/course/1/uploadFile', context, follow=True)
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
        PROJECT_DIR = os.path.dirname(__file__)

        uploadFile = open(PROJECT_DIR + os.sep + 'test_files' + os.sep + 'testUpload.txt')
        context = (
            {
                'name': 'test_upload_file',
                'description': 'test upload file',
                'docfile': uploadFile,
            }
        )
        response = self.client.post('/course/1/uploadFile', context, follow=True)
        uploadFile.close()

        url = '/course/1'
        response = self.client.get(url)
        rid = Resource.objects.get(name='test_upload_file').id
        url_file_to_test = '/course/resource/download/%d' % rid
        self.assertIn('<a href="%s">download</a>' % url_file_to_test, response.content)
        response = self.client.get(url_file_to_test)
        self.assertEqual(response.status_code, 200)