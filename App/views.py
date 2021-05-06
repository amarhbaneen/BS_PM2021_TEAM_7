from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

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
            return render(request, 'StudentPage.html')
        elif user is not None and user.groups.filter(name='teachers').exists():
            auth.login(request, user)
            return render(request, 'teacher_templates/teacher_dashboard.html')
        else:
            messages.info(request, 'required field')
            return redirect('login')
    else:
        return render(request, 'login.html')


def Signup(request):
    if request.method == 'POST':
        result = request.POST.get('register_as:', True)
        if result == "teacher":
            return Teacher_Signup(request)
        elif result == "student":
            return Student_Signup(request)
        else:
            return redirect('Signup')
    else:
        return render(request, 'signup.html')


def Teacher_Signup(request):
    if request.method == 'POST':
        ID = request.POST['ID']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username):
                messages.info(request, 'username is taken')
                return redirect('teacher_register')
            else:
                # Teacher_ID = User.objects.get(pk=request.user.id)
                # if Teacher_ID==ID:
                user = User.objects.create_user(username=username, email=email, password=password1,
                                                last_name=last_name, first_name=first_name, ID=ID)
                user.save()
                Teacher.objects.create(user=user)
                my_group = Group.objects.get(name='teachers')
                my_group.user_set.add(user)
                print("user is created")
                return redirect('login')
        else:
            messages.info(request, 'passwords doesnt mach')
            return redirect('teacher_register')
    else:
        return render(request, 'teacher_register.html')


def Student_Signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        student_teacher = request.POST.get('teachers', True)
        if password1 == password2:
            if User.objects.filter(username=username):
                messages.info(request, 'username is taken')
                return redirect('student_register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1,
                                                last_name=last_name,
                                                first_name=first_name)
                user.save()
                Teacher.objects.create(user=user)
                my_group = Group.objects.get(name='students')
                my_group.user_set.add(user)
                print("user is created")
                return redirect('login')
        else:
            messages.info(request, 'passwords doesnt mach')
            return redirect('student_register')
    else:
        return render(request, 'student_register.html')


def Solution_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = HomeworkForm()
        else:
            solution = StudentSolution.objects.get(pk=id)

            form = SolutionForm(instance=solution)

        return render(request, "student_solution.html", {'form': form})
    else:
        if id == 0:
            form = SolutionForm(request.POST)

        else:
            solution = StudentSolution.objects.get(pk=id)
            form = SolutionForm(request.POST, instance=solution)
        if form.is_valid():
            # homework_1 = form.save(commit=False)
            # homework_1.teacher = Teacher.objects.get(user = request.user)
            form.save()
        return render(request, 'StudentPage.html')


def showStudies(request):
    student = Student.objects.get(user=request.user)
    studies = StudiesStudent.objects.filter(student=student)
    return render(request, "studies_to_show.html", {'studies': studies})


def logoutUser(request):
    logout(request)
    return redirect('login')


def load_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'student_register.html', {'teachers': teachers})


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
    messages = list(TeacherMessage.objects.filter(teacher=request.user.teacher))
    return render(request, "teacher_templates/all_messages.html", {'messages': messages})


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
