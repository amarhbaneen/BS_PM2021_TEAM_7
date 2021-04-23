from django import forms
from .models import HomeWork, Teacher, TeacherMessage


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields=('teacher','homeWorkTitle','homeWorkContent')

    def __init__(self, *args, **kwargs):
        super(HomeworkForm, self).__init__(*args, **kwargs)




