from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from collegestacks import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'collegestacks.views.home', name='home'),
    # url(r'^collegestacks/', include('collegestacks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'app.views.main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about$',TemplateView.as_view(template_name='about.html')),
    #Search
    url(r'^search', 'app.views.search'),
    #Listing
    url(r'^universities', 'app.views.viewUniversities'),
    url(r'^university/(?P<university_id>\d+)$','app.views.viewUniversity'),
    url(r'^faculties', 'app.views.viewFaculties'),
    url(r'^faculty/(?P<faculty_id>\d+)$','app.views.viewFaculty'),
    #Course
    url(r'^course/new$','app.views.createCourse'),
    url(r'^course/(?P<course_id>\d+)$','app.views.viewCourse'),
    url(r'^course/(?P<course_id>\d+)/edit$','app.views.editCourse'),
    #Resource
    url(r'^course/(?P<course_id>\d+)/uploadFile$','app.views.uploadFile'),
    url(r'^course/(?P<course_id>\d+)/upLink$','app.views.upLink'),
    url(r'^course/resource/download/(?P<resource_id>\d+)$', 'app.views.download_resource'),

)


urlpatterns += patterns('',
    (r'^course/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT})
)