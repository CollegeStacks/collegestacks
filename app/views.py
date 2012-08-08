
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from app.forms import CreateCourseForm

def createCourse(request):
    context = RequestContext(request,
        {
            'form' : CreateCourseForm(),
        }
    )
    return render_to_response('newCourse.html', context)