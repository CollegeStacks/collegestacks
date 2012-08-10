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

class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    type = models.CharField(max_length=10)
    docfile = models.FileField(upload_to='resources/')
    sourceLink = models.CharField(max_length=500)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.name



