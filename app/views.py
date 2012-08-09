
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from app.forms import CreateCourseForm
from app.models import Course,University, Faculty

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





