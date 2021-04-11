from django import forms
from .models import HomeWork, Teacher, TeacherMessage


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ('teacherId', 'homeWorkContent')

    def __init__(self, *args, **kwargs):
        super(HomeworkForm, self).__init__(*args, **kwargs)
        self.fields['teacherId'].empty_label = "select"
from .models import AdminMessage, Grade


class AdminMessageForm(forms.ModelForm):

    class Meta:
        model = AdminMessage
        fields =('messageContent',)



class TeacherMessageForm(forms.ModelForm):

    class Meta:
        model = TeacherMessage
        fields =('teacherId','messageContent',)

    def __init__(self, *args, **kwargs):
        super(TeacherMessageForm, self).__init__(*args, **kwargs)
        self.fields['teacherId'].empty_label = "select"

