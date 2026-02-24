from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['Course_name', 'Course_detail', 'Course_fee', 'Course_duration','Course_photo']