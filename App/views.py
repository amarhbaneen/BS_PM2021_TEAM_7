from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.models import Group

from App.forms import *
from App.models import *



def homepage(request):
    return render(request, 'dashboard.html')


def home(requset):
    return render(requset, 'home.html')


def profile(requset):
    return render(requset, 'profile.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.groups.filter(name='admins').exists():
            auth.login(request, user)
            return render(request, 'AdminPage.html')
        elif user is not None and user.groups.filter(name='students').exists():
            auth.login(request, user)
            return redirect('student_dashboard')
        elif user is not None and user.groups.filter(name='teachers').exists():
            auth.login(request, user)
            return redirect('teacher')
        else:
            messages.info(request, 'error')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logoutUser(request):
	logout(request)
	return redirect('login')

# -------------------------------------- Teacher Views ----------------------------------#
# @author Amar Alsana
def teacher_dashboard(request):
    # created Dashboard for the Teacher that shown for the teacher after loging in

    context = {'homework_list': HomeWork.objects.all(), 'message_list': TeacherMessage.objects.last(),
               'studentcount': TeacherMessage.objects.all().count(),
               'homeworkcount': HomeWork.objects.all().count(),
               'adminMessage': AdminMessage.objects.first(),
               }
    # context = dictionary that content the whole elements that dashboard need to use
    # @author Amar Alsana

    return render(request, "teacher_templates/teacher_dashboard.html", context)


def teacher_message_form(request, id=0):
    # creating new form for inserting or editing existed teacher messages
    if request.method == "GET":
        if id == 0:
            form = TeacherMessageForm()




        else:
            message = TeacherMessage.objects.get(pk=id)

            form = TeacherMessageForm(instance=message)

        return render(request, "teacher_templates/message_form.html", {'form': form})
    else:
        if id == 0:
            form = TeacherMessageForm(request.POST)

        else:
            message = TeacherMessage.objects.get(pk=id)
            form = TeacherMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
        return redirect('teacher')


def teacher_mesaage_delete(request, id):
    message = TeacherMessage.objects.get(pk=id)
    message.delete()
    return redirect('teacher')


def showMessages(request):
    messages=list(TeacherMessage.objects.filter(teacher=request.user.teacher))
    return render(request,"teacher_templates/all_messages.html",{'messages':messages})


# -------------------------------------- homework Views ----------------------------------#
# @author Amar Alsana
def homework_form(request, id=0):
    # creating new form for inserting or editing existed homework
    if request.method == "GET":
        if id == 0:
            form = HomeworkForm()




        else:
            homework = HomeWork.objects.get(pk=id)

            form = HomeworkForm(instance=homework)

        return render(request, "homework_templates/homework_form.html", {'form': form})
    else:
        if id == 0:
            form = HomeworkForm(request.POST)

        else:
            homework = HomeWork.objects.get(pk=id)
            form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            # homework_1 = form.save(commit=False)
            # homework_1.teacher = Teacher.objects.get(user = request.user)
            form.save()
        return redirect('/teacher')
        # @author Amar Alsana


def homework_delete(request, id):
    # @author Amar Alsana
    # delete existed Homework
    homework = HomeWork.objects.get(pk=id)
    homework.delete()
    return redirect('/teacher')


# -------------------------------------- Admin Views ----------------------------------#
def admin_message_form(request, id=0):
    # creating new form for inserting or editing existed admin messages
    if request.method == "GET":
        if id == 0:
            form = AdminMessageForm()




        else:
            message = AdminMessage.objects.get(pk=id)

            form = AdminMessageForm(instance=message)

        return render(request, "admin_templates/admin_message_form.html", {'form': form})
    else:
        if id == 0:
            form = AdminMessageForm(request.POST)

        else:
            message = AdminMessage.objects.get(pk=id)
            form = AdminMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
        return redirect('homepage')


def admin_mesaage_delete(request, id):
    message = AdminMessage.objects.get(pk=id)
    message.delete()
    return redirect('homepage')
 #-------------------------------------- Teacher Views ----------------------------------#
# @author Amar Alsana
def student_dashboard(request):
    # created Dashboard for the student that shown for the teacher after loging in
    student=Student.objects.get(user=request.user)


    context = {'homework_list': HomeWork.objects.filter(teacher=student.teacher).all()[:3], 'message_list':TeacherMessage.objects.filter(teacher=student.teacher).last(),
    'adminMessage': AdminMessage.objects.last(),'grade_list':Grade.objects.last()
               }
    # context = dictionary that content the whole elements that dashboard need to use
    # @author Amar Alsana

    return render(request, "student_templates/studentDashBoard.html", context)

