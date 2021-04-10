from django import forms
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from schoolSystemManagment.models import models,Teacher

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
        if user_type in ('teacher','Teacher'):
            if chose_teacher !='':
                raise forms.ValidationError('keep this box empty for teacher')
            else:
                return chose_teacher
        elif user_type in ('student','Student'):
            if chose_teacher == '':
                raise forms.ValidationError('you need to pick a teacher')
            elif not Teacher.objects.filter(userId__username=chose_teacher).exists():
                raise forms.ValidationError('Teacher name is  not existing ')
            else:
                return chose_teacher