from wsgiref.util import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from app.forms import CreateCourseForm, UploadFileForm, UploadSourceLinkForm
from app.models import *

def main(request):
    return render_to_response('main.html')

def createCourse(request):
    context = RequestContext(request,
            {
                'form' : CreateCourseForm(),
            }
    )
    if request.method == 'POST':
        creCourseForm = CreateCourseForm(request.POST)
        data = creCourseForm.data
        if creCourseForm.is_valid():
            data = creCourseForm.cleaned_data
            course = Course.objects.get_or_create(title = data['title'], code = data['code'], abbr = data['abbr'],
            university = data['university'], faculty = data['faculty'],department = data['department'], description = data['description'])[0]
            course.save()
            return HttpResponseRedirect('/course/%d'%course.id)
        else:
            context.update(
                    {
                        'form' : CreateCourseForm(
                            initial = {'title':data['title'], 'code':data['code'], 'abbr':data['abbr'],
                                       'university':data['university'], 'faculty':data['faculty'],
                                       'department':data['department'], 'description':data['description']}
                        ),
                        'error' : 'please fill all information'
                    }
            )
            return render_to_response('newCourse.html', context)
    else:
        return render_to_response('newCourse.html', context)

def viewCourse(request,course_id):
    c = get_object_or_404(Course, pk=course_id)
    resource = Resource.objects.filter(course__id = c.id)
    context = RequestContext(request,
        {
            'c' : c,
            'resources' : resource,
            'upFileForm' : UploadFileForm(),
            'upLinkForm' : UploadSourceLinkForm(),
        }
    )

    return render_to_response('course.html',context)

def editCourse(request,course_id):
    c = get_object_or_404(Course, pk=course_id)
    context = RequestContext(request,
            {
            'form' : CreateCourseForm(),
            }
    )
    print("INITIAL ID IS %d"%c.id)
    if request.method == 'GET':
        print("GETTING")
        context = RequestContext(request,
                {
                'form' : CreateCourseForm(
                    initial= {'title':c.title, 'code':c.code, 'abbr':c.abbr,
                              'university':c.university, 'faculty':c.faculty,
                              'department':c.department, 'description':c.description}
                ),
                'cid':c.id
            }
        )
        return render_to_response('editCourse.html', context)
    else :
        print("POSTING")
        creCourseForm = CreateCourseForm(request.POST)
        data = creCourseForm.data
        print("##############DATA\n" + str(data))
        if creCourseForm.is_valid():
            data = creCourseForm.cleaned_data
            c.title=data['title']
            c.code=data['code']
            c.abbr=data['abbr']
            c.description=data['description']
            c.university=data['university']
            c.faculty=data['faculty']
            c.department=data['department']
            c.description=data['description']
            c.save()
            print("EDIT COMPLETE!! REDIRECTING TO %d"%c.id)
            return HttpResponseRedirect('/course/%d'%c.id)
        else:
            print(creCourseForm.data)
            context.update(
                    {
                    'form' : CreateCourseForm(
                        initial = {'title':data['title'], 'code':data['code'], 'abbr':data['abbr'],
                                   'university':data['university'], 'faculty':data['faculty'],
                                   'department':data['department'], 'description':data['description']}
                    ),
                    'error' : 'please fill all information',
                    'cid':c.id,
                    }
            )
            return render_to_response('editCourse.html', context)

def uploadFile(request, course_id):
    if request.method == 'POST':
        c = Course.objects.get(pk=course_id)
        upFile = UploadFileForm(request.POST, request.FILES)
        data = upFile.data
        if upFile.is_valid():
            data = upFile.cleaned_data
            newFile = Resource(name = data['name'], description = data['description'], type = 'File',
                                 docfile = request.FILES['docfile'], sourceLink = '', course = c)
            newFile.save()
            return HttpResponseRedirect('/course/%d'%c.id)
        else:
            resources = Resource.objects.all()
            context = RequestContext(request,
                {
                    'c' : c,
                    'resources' : resources,
                    'upFileForm' : UploadFileForm(
                        initial={'name':data['name'], 'description':data['description']}
                    ),
                    'upLinkForm' : UploadSourceLinkForm(),
                    'errorFile' : 'Please fill all information'
                }
            )

            return render_to_response('course.html',context)
    else:
        return viewCourse(request,course_id)



def upLink(request, course_id):
    if request.method == 'POST':
        c = Course.objects.get(pk=course_id)
        upLink = UploadSourceLinkForm(request.POST)
        data = upLink.data
        if upLink.is_valid():
            data = upLink.cleaned_data
            newLink = Resource(name = data['name'], description = data['description'], type = 'Link',
                             sourceLink = data['sourceLink'], course = c)
            newLink.save()
            return HttpResponseRedirect('/course/%d'%c.id)
        else:
            resources = Resource.objects.all()
            context = RequestContext(request,
                    {
                    'c' : c,
                    'resources' : resources,
                    'upFileForm' : UploadFileForm(
                        initial={'name':data['name'], 'description':data['description']}
                    ),
                    'upLinkForm' : UploadSourceLinkForm(),
                    'errorLink' : 'Please fill all information'
                    }
            )

            return render_to_response('course.html',context)
    else:
        return viewCourse(request,course_id)

def viewUniversities(request):
    universities = University.objects.all()
    context = {'universities' : universities}
    return render_to_response('universities.html',context)

def viewUniversity(request,university_id):
    university = get_object_or_404(University,id=university_id)
    courses = Course.objects.filter(university__id=university_id).order_by('faculty__name')
    context = {
        'courses' : courses,
        'university' : university
    }
    return render_to_response('university.html',context)


def viewFaculties(request):
    faculties = Faculty.objects.all()
    context = {'faculties' : faculties}
    return render_to_response('faculties.html',context)

def viewFaculty(request, faculty_id):
    faculty = get_object_or_404(Faculty,id=faculty_id)
    courses = Course.objects.filter(faculty__id=faculty_id).order_by('university__name')
    context = {
        'courses' : courses,
        'faculty' : faculty
    }
    return render_to_response('faculty.html',context)

def download_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    data = FileWrapper(resource.docfile)
    response = HttpResponse(data, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % resource.docfile
    return response

def search(request):
    if request.method == 'GET' :
        q = request.GET.get('q','')
        if q == '':
            return HttpResponse(content="nothing to search")
        return HttpResponse(content="Searching for " + str(q))
    return HttpResponseNotAllowed()
