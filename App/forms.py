from django import forms
from .models import *


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ('teacher', 'homeWorkTitle', 'homeWorkContent')

    def __init__(self, *args, **kwargs):
        super(HomeworkForm, self).__init__(*args, **kwargs)


class SolutionForm(forms.ModelForm):
    class Meta:
        model = StudentSolution
        fields = ('solutionContent', 'student')

    def __init__(self, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)


class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = AdminMessage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AdminMessageForm, self).__init__(*args, **kwargs)


class TeacherMessageForm(forms.ModelForm):
    class Meta:
        model = TeacherMessage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TeacherMessageForm, self).__init__(*args, **kwargs)
