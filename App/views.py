from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.models import User
from App.filters import *

# Create your views here.
def homepage(request):
    return  render(request,'dashboard.html')





def user_list(request):
    context=User.objects.all()
    just_user=[]
    for con in context:
        if not con.is_superuser:
            just_user.append(con)

    myFilter = userFilter(request.GET, queryset=User.objects.all())
    user_list=myFilter.qs
    context = {'user_list': user_list,'myFilter':myFilter}
    return render(request,"user_list.html",context)


def user_form_edit(request,id):
        user =User.objects.get(pk=id)
        form = addUserForm(instance=user)
        if request.method == 'POST':
            form = addUserForm(request.POST, instance=form)
            if form.is_valid():
                form.save()

        context = {'form': form}
        return render(request,'user_form_info.html',context)
       # return render(request, 'profile.html', context)

    # instance=get_object_or_404(User,id=id)
    # form=addUserForm(instance=instance)
    # if request.method=='POST':
    #     form=addUserForm(request.POST,instance=instance)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user_list')
    # return render(request,'create_user.html',{'form':form})



def delete_user(request,id):
    user = User.objects.get(pk=id)
    user.delete()
    return redirect('user_list')



def create_user(request):
    form = addUserForm()
    if request.method=='POST':
        form=addUserForm(request.POST)
        if form.is_valid():
            curr_user =form.save()
            if form.clean_user_type() in ('Student', 'student'):
                user=User.objects.get(username=form.clean_chose_teacher())
                teacher = Teacher.objects.get(user=user)
                Student.objects.create(user=curr_user,teacher=teacher)

            elif form.clean_user_type() in ('Teacher', 'teacher'):
                Teacher.objects.create(user=curr_user)
                #Teacher.objects.create(user_id=curr_user)
            return redirect('user_list')
    return render(request,"create_user.html",{"form":form})



def showUser(request,id):
    user=User.objects.get(pk=id)
    context={'user':user}
    return render(request,'show_details.html',context)

# def search(request):
#     if request.method=='POST':
#         searched=request.POST['searched']
#         user_list=User.objects.all()
#         user_filter=user_list.filter(username=searched)
#         return render(request,'user_list.html',{'user_filter':user_filter})
#     else:
#         return render(request,'user_list.html',{})



