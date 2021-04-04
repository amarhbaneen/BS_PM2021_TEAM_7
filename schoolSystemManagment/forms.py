from django import forms
from .models import HomeWork, Teacher


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ('teacherId', 'homeWorkContent')

    def __init__(self, *args, **kwargs):
        super(HomeworkForm, self).__init__(*args, **kwargs)
        self.fields['teacherId'].empty_label = "select"
