from django.shortcuts import render,redirect
from .forms import *
from schoolSystemManagment.models import  *
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render

def Teacherbase(request):
    return render(request,"teacher_base.html")
from django.shortcuts import render, redirect

from schoolSystemManagment.forms import AdminMessageForm, TeacherMessageForm


def index(request):
    return render(request, "index.html", )

def addMessage(request):
    if request.method =="POST":
        form = AdminMessageForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/index')

    else:
        form = AdminMessageForm()
        return render(request, "AddAmessages.html", {'form': form})




def addUser(response):
    if response.method=='POST':
        form=addUserForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form=addUserForm()
    return render(response,"addUser.html",{"form":form})





def message_base(request):
    contex = {'message_list': TeacherMessage.objects.all()}
    return render(request, "message_base.html", contex)



def message_form(request,id=0):
    if request.method == "GET":
        if id == 0:
            form = TeacherMessageForm()

        else:
            message = TeacherMessage.objects.get(pk=id)
            form = TeacherMessageForm(instance=message)

        return render(request, "mess_form.html", {'form': form})
    else:
        if id ==0:
            form = TeacherMessageForm(request.POST)
        else:
            message = TeacherMessage.objects.get(pk=id)
            form=TeacherMessageForm(request.POST,instance=message)
        if form.is_valid():
            form.save()
        return redirect('/messages')


def homework_delete(request, id):
    message = TeacherMessage.objects.get(pk=id)
    message.delete()
    return redirect('/messages')

def showMessages(request):
    contex = {'message_list': TeacherMessage.objects.all()}
    return render(request, "all_messages.html", contex)

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'welcome.html')
        else:
            messages.info(request, 'error')
            return redirect('login')
    else:
        return render(request, 'login.html')


def adminlogout(request):
    auth.logout(request)
    return redirect('/login')