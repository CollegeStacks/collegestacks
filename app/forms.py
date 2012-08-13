__author__ = 'User'
from django import forms
from app.models import Course, University, Faculty

class CreateCourseForm(forms.Form):
    title = forms.CharField(max_length=100)
    code = forms.CharField(max_length=20)
    abbr = forms.CharField(max_length=50)
    university = forms.ModelChoiceField(University.objects.all())
    faculty = forms.ModelChoiceField(Faculty.objects.all())
    description = forms.CharField(widget=forms.Textarea)