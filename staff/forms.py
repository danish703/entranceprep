from courses.models import TestExam
from django import forms
from courses.models import Course

class TestCreateForm(forms.ModelForm):
    class Meta:
        model = TestExam
        fields = ['test_name','course','status','purchased_points','passmarks','image',]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name','image','slug','status']