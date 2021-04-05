from django.shortcuts import render,redirect
from .forms import addUserForm

def Teacherbase(request):
    return render(request,"teacher_base.html")


def addUser(response):
    if response.method=='POST':
        form=addUserForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form=addUserForm()
    return render(response,"addUser.html",{"form":form})