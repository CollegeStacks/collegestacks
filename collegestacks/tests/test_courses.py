from django.test import TestCase
from app.models import *

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
        uni = University.objects.create(name="Chulalongkorn",abbr="chula")
        faculty = Faculty.objects.create(name="Engineering",abbr='eng',university=uni)
        dep = Department.objects.create(name="Computer Engineering",abbr='cp',faculty=faculty)
        course1 = Course.objects.create(title="Formal Language", abbr="Formal Lang", code="2110399",
            description="abc",university=uni,faculty=faculty,department=dep)
        c = Course.objects.get(pk=course1.id)
        self.assertEquals(c.title,'Formal Language')
        self.assertEqual(c.abbr, 'Formal Lang')
        self.assertEqual(c.code, '2110399')
        self.assertEqual(c.description,'abc')
        self.assertEqual(c.university.name,"Chulalongkorn")
        self.assertEqual(c.faculty.name,'Engineering')

    def test_create_course_success(self):
        university = University.objects.create(name="MIT",abbr='mit')
        faculty = Faculty.objects.create(name="Science",abbr='sci',university=university)
        department = Department.objects.create(name="Physics",abbr='phy',faculty=faculty)

        context = {
            'title' : 'noly',
            'code' : '2110455',
            'abbr' : 'form',
            'university' : university.id,
            'faculty' : faculty.id,
            'department' : department.id,
            'description' : 'test',
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
            'department' : '',
            'description' : '',
        }
        url = '/course/new'
        response = self.client.post(url,context)
        print(response)
        self.assertEqual(response.status_code,200)
        self.assertIn('please',response.content)


    def test_course_id(self):
        #test case for CS-04 View Course story card --noly

        #add new course to db
        university = University.objects.create(name="Chulalongkorn",abbr="chula")
        faculty = Faculty.objects.create(name="Engineering",abbr="eng",university=university)
        department = Department.objects.create(name="Computer Engineering",abbr="cp",faculty=faculty)
        course = Course.objects.create(title="Software Engineering", code="2110333", abbr="SE",university=university, faculty=faculty, department=department)

        #retrieve course from http call to test
        url = '/course/%(id)d'%{"id":course.id}
        response = self.client.get(url)
        content = response.content
        print(content)

        self.assertEqual(response.status_code,200)
        self.assertIn(course.title, content)
        self.assertIn(course.code, content)
        self.assertIn(course.abbr, content)
        self.assertIn(course.university.name, content)
        self.assertIn(course.faculty.name, content)
        self.assertIn(course.department.name, content)

    def test_course_id_notfound(self):
        id = len(Course.objects.all())+5
        url = '/course/%(id)d'% {'id':id}
        response = self.client.get(url)
        print(url)
        self.assertEqual(response.status_code,404)

    def test_edit_course(self):
        # Build
        university = University.objects.create(name="Chulalongkorn",abbr='chula')
        faculty = Faculty.objects.create(name="Engineering",abbr='eng',university=university)
        department = Department.objects.create(name="Computer Engineering", abbr='cp',faculty=faculty)
        course = Course.objects.create(title="Software Analysis", code="2110333", abbr="SE",university=university, faculty=faculty,department=department, description="desc")

        # Operate
        url = '/course/%d/edit' % course.id
        response = self.client.get(url)
        print (url)
        print (response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn("<title>Edit Course %d</title>"%course.id,response.content)
        self.assertIn(course.title, response.content)
        self.assertIn(course.abbr, response.content)
        self.assertIn(course.code, response.content)
        self.assertIn(course.description, response.content)
        self.assertIn('selected="selected">%s' % course.university.name, response.content)
        self.assertIn('selected="selected">%s' % course.faculty.name, response.content)
        self.assertIn('selected="selected">%s' % course.department.name, response.content)

        new_university = University.objects.create(name="Stanford",abbr='stanford')
        new_faculty = Faculty.objects.create(name="Law",abbr='law',university=new_university)
        new_department = Department.objects.create(name="International",abbr='int',faculty=new_faculty)
        context = {
            'title' : course.title,
            'code' : course.code,
            'abbr' : course.abbr,
            'university' : new_university.id,
            'faculty' : new_faculty.id,
            'department' : new_department.id,
            'description' : course.description
        }

        url = '/course/%d/edit'%course.id
        response = self.client.post(url,context,follow=True)
        print(url)
        print(response)
        print("FUCKYOUTHUNDER#######################")
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertIn("<title>View Course</title>",response.content)
        self.assertIn(course.title, response.content)
        self.assertIn(course.code, response.content)
        self.assertIn(course.abbr, response.content)
        self.assertIn(course.description, response.content)
        self.assertIn(new_university.name, response.content)
        self.assertNotIn(university.name, response.content)
        self.assertIn(new_faculty.name, response.content)
        self.assertNotIn(faculty.name,response.content)
        self.assertIn(new_department.name, response.content)
        self.assertNotIn(department.name,response.content)


    def test_list_universities(self):
        #no universities
        url = '/universities'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertIn('NO UNIVERSITY FOUND',response.content)

        u1 = University.objects.create(name="Chula")
        u2 = University.objects.create(name="MIT")
        u3 = University.objects.create(name="Harvard")

        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertNotIn('NO UNIVERSITY FOUND',response.content)
        self.assertIn(u1.name,response.content)
        self.assertIn('/university/' + str(u1.id) ,response.content)
        self.assertIn(u2.name,response.content)
        self.assertIn('/university/' + str(u2.id) ,response.content)
        self.assertIn(u3.name,response.content)
        self.assertIn('/university/' + str(u3.id) ,response.content)

    def test_list_faculties(self):
        #no universities
        url = '/faculties'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertIn('NO FACULTY FOUND',response.content)
        u = University.objects.create(name="Chulalongkorn", abbr='chula')

        f1 = Faculty.objects.create(name="Engineering",abbr='eng',university=u)
        f2 = Faculty.objects.create(name="Law",abbr='law',university=u)
        f3 = Faculty.objects.create(name="Arts",abbr='arts',university=u)

        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertNotIn('NO FACULTY FOUND',response.content)
        self.assertIn(f1.name,response.content)
        self.assertIn('/faculty/' + str(f1.id) ,response.content)
        self.assertIn(f2.name,response.content)
        self.assertIn('/faculty/' + str(f2.id) ,response.content)
        self.assertIn(f3.name,response.content)
        self.assertIn('/faculty/' + str(f3.id) ,response.content)

    def test_view_faculty(self):

        university1 = University.objects.create(name = 'Chula',abbr='chula')
        university2 = University.objects.create(name = 'MIT',abbr='mit')
        faculty1 = Faculty.objects.create(name = 'Engineering',abbr='eng',university=university1)
        faculty2 = Faculty.objects.create(name = 'Engineering',abbr='eng',university=university2)
        dep1 = Department.objects.create(name = 'Computer Engineering',abbr='cp',faculty=faculty1)
        dep2 = Department.objects.create(name = 'Computer Engineering',abbr='cp',faculty=faculty2)

        course1 = Course.objects.create(title='Formal Language', abbr='FORM LANG', code='2110211', description="yay",faculty=faculty1, university=university1,department=dep1)
        course2 = Course.objects.create(title='Calculus', abbr='CAL', code='EE999', description="fuck",faculty=faculty2, university=university2,department=dep2)
        course3 = Course.objects.create(title='Programming', abbr='PROG', code='2110101', description="yay",
            faculty=faculty1, university=university1,department=dep1)

        url = '/faculty/%d'%faculty1.id
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(course1.title, response.content)
        self.assertNotIn(course2.title, response.content)
        self.assertIn(course3.title, response.content)

    def test_view_university(self):
        university = University.objects.create(name='Chulalongkorn',abbr='chula')
        faculty1 = Faculty.objects.create(name='Engineering',abbr='eng',university=university)
        faculty2 = Faculty.objects.create(name='Law',abbr='law',university=university)
        department1 = Department.objects.create(name='Computer Engineering',abbr='cp',faculty=faculty1)
        department2 = Department.objects.create(name='International',abbr='int',faculty=faculty2)
        course1 = Course.objects.create(title='Formal Language', abbr='FORM LANG', code='2110211', description="yay",
            faculty=faculty1, university=university, department=department1)
        course2 = Course.objects.create(title='Calculus', abbr='CAL', code='EE999', description="fuck",faculty=faculty2, university=university,department=department2)
        course3 = Course.objects.create(title='Programming', abbr='PROG', code='2110101', description="yay",
            faculty=faculty1, university=university,department=department1)

        url = '/university/1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(course1.title, response.content)
        self.assertIn(course2.title, response.content)
        self.assertIn(course3.title, response.content)
