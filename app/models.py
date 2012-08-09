from django.contrib import admin
from django.db import models

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=140)

    def __unicode__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length= 140)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    abbr = models.CharField(max_length=50)
    university = models.ForeignKey(University)
    faculty = models.ForeignKey(Faculty)
    description = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.title

class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "code", "abbr", "university", "faculty", "description"]
    search_fields = ["title"]

class CourseInLine(admin.TabularInline):
    model = Course

class UnivAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

class UnivInLine(admin.TabularInline):
    model = University

class FacultyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

class FacultyInLine(admin.TabularInline):
    model = Faculty

admin.site.register(Course,CourseAdmin)
admin.site.register(University,UnivAdmin)
admin.site.register(Faculty,FacultyAdmin)
