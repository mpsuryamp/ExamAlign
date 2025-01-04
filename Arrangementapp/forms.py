from django import forms
from .models import *

  # specify the fields you want in the form

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['branch','semester','subjectname', 'subjectcode']
# class Studentform(forms.ModelForm):
#     class Meta:
#         model = Studentprofile
#         fields = ['registerno']
class Subsembranchform(forms.ModelForm):
    class Meta:
        model= Subject
        fields=['branch','semester','subjectname','subjectcode']


class Addnotificationform(forms.ModelForm):
    class Meta:
        model = ExamNotification
        fields = ['notification']