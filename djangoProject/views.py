from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect ,get_object_or_404
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