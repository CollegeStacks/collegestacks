from django.contrib import admin
from app.models import Course, University, Faculty

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'abbr', 'university', 'faculty', 'description']
    search_fields = ['title']

admin.site.register(Course, CourseAdmin)
admin.site.register(University)
admin.site.register(Faculty)