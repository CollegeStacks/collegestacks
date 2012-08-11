from django.contrib import admin
from app.models import Course, University, Faculty, Resource

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk', 'code', 'abbr', 'university', 'faculty', 'description']
    search_fields = ['title']
    readonly_fields = ['pk']

admin.site.register(Course, CourseAdmin)
admin.site.register(University)
admin.site.register(Faculty)

class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk', 'description', 'type', 'docfile', 'sourceLink', 'course']
    search_fields = ['name']
    readonly_fields = ['pk']

admin.site.register(Resource, ResourceAdmin)