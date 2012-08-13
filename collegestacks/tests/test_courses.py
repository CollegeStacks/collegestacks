from django.test import TestCase
from app.models import Course,University, Faculty

class TestCourseSuite(TestCase):

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
        #test case for CS-04 View Course story card --noly

        #add new course to db
        u = University.objects.get_or_create(name="Chulalongkorn")[0]
        f = Faculty.objects.get_or_create(name="Engineering")[0]
        c = Course.objects.get_or_create(title="Software Engineering", code="2110333", abbr="SE",university=u, faculty=f)[0]
        c.save()

        #retrieve course from http call to test
        url = '/course/%(id)d'%{"id":c.id}
        response = self.client.get(url)
        content = response.content
        print(content)

        self.assertEqual(response.status_code,200)
        self.assertIn(c.title, content)
        self.assertIn(c.code, content)
        self.assertIn(c.abbr, content)
        self.assertIn(c.university.name, content)
        self.assertIn(c.faculty.name, content)

    def test_course_id_notfound(self):
        id = len(Course.objects.all())+5
        url = '/course/%(id)d'% {'id':id}
        response = self.client.get(url)
        print(url)
        self.assertEqual(response.status_code,404)

    def test_edit_course(self):
        # Build
        university = University.objects.create(name="Chulalongkorn")
        faculty = Faculty.objects.create(name="Engineering")
        course = Course.objects.create(title="Software Engineering", code="2110333", abbr="SE",university=university, faculty=faculty)

        # Operate
        url = '/course/%d/edit' % course.id
        response = self.client.get(url)
        print (url)
        print (response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn(course.title, response.content)
        self.assertIn(course.abbr, response.content)
        self.assertIn(course.code, response.content)
        self.assertIn(course.description, response.content)
        self.assertIn('selected="selected">%s' % course.university.name, response.content)
        self.assertIn('selected="selected">%s' % course.faculty.name, response.content)

        new_university = University.objects.create(name="Stanford")
        new_faculty = Faculty.objects.create(name="Laws")

        data = {
            'title' : course.title,
            'code' :  course.code,
            'abbr' : course.abbr,
            'university' : new_university.id,
            'faculty' : new_faculty.id,
            'description' : course.description,
            }
        url = '/course/%d/edit' % course.id
        response = self.client.post(url,data,follow=True)
        print(response)

        # Check
        self.assertEqual(response.status_code, 200)
        self.assertIn(course.title, response.content)
        self.assertIn(course.code, response.content)
        self.assertIn(course.abbr, response.content)
        self.assertIn(course.description, response.content)
        self.assertIn(new_university.name, response.content)
        self.assertNotIn(university.name,response.content)
        self.assertIn(new_faculty.name, response.content)
        self.assertNotIn(faculty.name,response.content)




