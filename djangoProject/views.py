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



def user_form_info(request,id=0):

    if request.method=='GET':
        if id==0:
            form = addUserForm()
        else:
             user=User.objects.get(pk=id)
             form=addUserForm(instance=user)
        return render(request,'user_form_info.html',{'form':form})
    else:
        if id==0:
            form = addUserForm(request.POST)
        else:
            user = User.objects.get(pk=id)
            form = addUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
        return redirect('user_list')




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