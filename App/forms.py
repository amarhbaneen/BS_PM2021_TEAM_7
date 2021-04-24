from django import forms
from .models import *


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ('teacher', 'homeWorkTitle', 'homeWorkContent')

    def __init__(self, *args, **kwargs):
        super(HomeworkForm, self).__init__(*args, **kwargs)


class BugReportForm(forms.ModelForm):
    class Meta:
        model = Bugreport
        fields = ('User', 'bugContent ')


