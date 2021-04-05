from django import forms
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class addUserForm(UserCreationForm):
    email=forms.EmailField()
    is_student=forms.CharField(required=False)
    is_teacher=forms.CharField(required=False)

    class Meta:
        model=User
        fields=["username","email","is_student","is_teacher","password1","password2"]
