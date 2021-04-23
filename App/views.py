from django.contrib import auth
from django.contrib import messages
from django.shortcuts import render, redirect

from App.forms import HomeworkForm
from App.models import *


def homepage(request):
    return render(request, 'dashboard.html')


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
            return render(request, 'StudentPage.html')
        elif user is not None and user.groups.filter(name='teachers').exists():
            auth.login(request, user)
            return render(request, 'teacher_templates/teacher_dashboard.html')
        else:
            messages.info(request, 'error')
            return redirect('login')
    else:
        return render(request, 'login.html')


# -------------------------------------- Teacher Views ----------------------------------#
# @author Amar Alsana
def teacher_dashboard(request):
    # created Dashboard for the Teacher that shown for the teacher after loging in
    context = {'homework_list': HomeWork.objects.all(), 'student_list': Student.objects.all(),
               'studentcount': Student.objects.all().count(),
               'homeworkcount': HomeWork.objects.all().count()}
    # context = dictionary that content the whole elements that dashboard need to use
    # @author Amar Alsana

    return render(request, "teacher_templates/teacher_dashboard.html", context)


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
            form.save()
        return redirect('/teacher')
        # @author Amar Alsana


def homework_delete(request, id):
    # @author Amar Alsana
    # delete existed Homework
    homework = HomeWork.objects.get(pk=id)
    homework.delete()
    return redirect('/teacher')
