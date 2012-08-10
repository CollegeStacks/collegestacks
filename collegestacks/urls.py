from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about$',TemplateView.as_view(template_name='about.html')),
    url(r'^course/new$','app.views.createCourse'),
    url(r'^course/(?P<course_id>\d+)$','app.views.viewCourse'),
    url(r'^course/(?P<course_id>\d+)/uploadFile$','app.views.uploadFile'),
    url(r'^course/(?P<course_id>\d+)/upLink$','app.views.uploadFile')

)
