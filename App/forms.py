from django import forms
from .models import *
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ('teacher', 'homeWorkTitle', 'homeWorkContent')

    def __init__(self, *args, **kwargs):
        super(HomeworkForm, self).__init__(*args, **kwargs)


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


class SolutionForm(forms.ModelForm):
    class Meta:
        model = StudentSolution
        fields = ('student','homeWork','solutionContent')

    def __init__(self, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)

class studyForm(forms.ModelForm):
    class Meta:
        model = Studies
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(studyForm, self).__init__(*args, **kwargs)
class BugReportForm(forms.ModelForm):
    class Meta:
        model = Bugreport
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BugReportForm, self).__init__(*args, **kwargs)

'''queryset =Teacher.objects.all()
teacher_id=[p.userId for p in queryset]'''

class addUserForm(UserCreationForm):
    email=forms.EmailField()
    user_type=forms.CharField(max_length=50,required=True)
    chose_teacher = forms.CharField(max_length=50,required=False)
    class Meta:
        model=User
        fields=['username','email','user_type','chose_teacher','password1','password2']

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This mail is all ready in system')
        elif not email.endswith('com') and not email.endswith('il'):
            raise forms.ValidationError('This is not a valid email')
        return email

    def clean_user_type(self):
        user_type=self.cleaned_data.get('user_type')
        if user_type not in ('teacher','student','Student','Teacher'):
            raise forms.ValidationError('you need to chose one of this [Student,Teacher]')
        else:
            return user_type


    def clean_chose_teacher(self):
        user_type=self.clean_user_type()
        chose_teacher = self.cleaned_data.get('chose_teacher')
        user = User.objects.get(username=chose_teacher)
        if user_type in ('teacher','Teacher'):
            if chose_teacher !='':
                raise forms.ValidationError('keep this box empty for teacher')
            else:
                return chose_teacher
        elif user_type in ('student','Student'):
            if chose_teacher == '':
                raise forms.ValidationError('you need to pick a teacher')
            elif not  Teacher.objects.filter(user=user).exists():
                raise forms.ValidationError('Teacher name is  not existing ')
            else:
                return chose_teacher
