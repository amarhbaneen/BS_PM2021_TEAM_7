from django.shortcuts import render,redirect
from .forms import *
from schoolSystemManagment.models import  *
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect ,get_object_or_404
from djangoProject.forms import addUserForm
from schoolSystemManagment.models import models,Student,Teacher


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






def addUser(request):
    if request.method=='POST':
        form=addUserForm(request.POST)
        if form.is_valid():
            curr_user = form.save()
            if form.clean_user_type() in ('Student', 'student'):
                teacher = Teacher.objects.get(userId__username=form.clean_chose_teacher())
                Student.objects.create(userId=curr_user, teacherId_id=teacher.id)

            elif form.clean_user_type() in ('Teacher', 'teacher'):
                Teacher.objects.create(userId=curr_user)
            return redirect('user_list')
    else:
        form=addUserForm()
    return render(request,"user_form_info.html",{"form":form})





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
    return render(request,"user_form_info.html",{"form":form})


def user_form_edit(request,id=None):
    instance=get_object_or_404(User,id=id)
    form=addUserForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        return redirect('user_list')
    return render(request,'user_form_info.html',{'form':form})

def user_list(request):
    context=User.objects.all()
    just_user=[]
    for con in context:
        if not con.is_superuser:
            just_user.append(con)

    context = {'user_list': just_user}
    return render(request,"user_list.html",context)


def delete_user(request,id):
    user = User.objects.get(pk=id)
    user.delete()
    return redirect('user_list')
