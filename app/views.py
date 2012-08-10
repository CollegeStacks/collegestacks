
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from app.forms import CreateCourseForm, UploadFileForm, UploadSourceLinkForm
from app.models import Course,University, Faculty, Resource

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
            course = Course.objects.create(title = data['title'], code = data['code'], abbr = data['abbr'],
            university = data['university'], faculty = data['faculty'], description = data['description'])
            course.save()
            return HttpResponseRedirect('/course/%d'%course.id)
        else:
            context.update(
                    {
                        'form' : CreateCourseForm(
                            initial = {'title':data['title'], 'code':data['code'], 'abbr':data['abbr'],
                                       'university':data['university'], 'faculty':data['faculty'],
                                       'description':data['description']}
                        ),
                        'error' : 'please fill all information'
                    }
            )
            return render_to_response('newCourse.html', context)
    else:
        return render_to_response('newCourse.html', context)

def viewCourse(request,course_id):
    c = get_object_or_404(Course, pk=course_id)
    resource = Resource.objects.all()
    context = RequestContext(request,
        {
            'c' : c,
            'resource' : resource,
            'upFileForm' : UploadFileForm(),
            'upLinkForm' : UploadSourceLinkForm(),
        }
    )

    return render_to_response('course.html',context)

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
                    }
            )

            return render_to_response('course.html',context)
        # handle in case submit incomplete form********************************************
    else:
        return viewCourse(request,course_id)




