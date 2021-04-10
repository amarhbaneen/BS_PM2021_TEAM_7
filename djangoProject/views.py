from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from djangoProject.forms import addUserForm
from schoolSystemManagment.models import models,Student,Teacher


def Teacherbase(request):
    return render(request,"teacher_base.html")

def addUser(request):
    if request.method=='POST':
        form=addUserForm(request.POST)
        if form.is_valid():
            curr_user=form.save()
            if form.clean_user_type() in('Student','student'):
                teacher = Teacher.objects.get(userId__username=form.clean_chose_teacher()) ###
                Student.objects.create(userId=curr_user,teacherId_id=teacher.userId)
                print(teacher.userId)
                ###

            elif form.clean_user_type() in('Teacher','teacher'):
                Teacher.objects.create(userId=curr_user)
    else:
        form=addUserForm()
    return render(request,"addUser.html",{"form":form})

def checkValue(value):
    return value!=None and value==True