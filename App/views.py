from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

from App.forms import *
from App.models import *
from App.filters import *


def adminPage(request):
    return render(request, 'dashboard.html')


def home(requset):
    return render(requset, 'home.html')


def profile(request):
    user = request.user
    form = UserCreationForm(instance=user)

    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=form)
        if form.is_valid():
            form.save()

    context = {'form': form}

    return render(request, 'profile.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.groups.filter(name='admins').exists():
            auth.login(request, user)
            return redirect('dashboard')
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
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']
    if password1 == password2:
        if User.objects.filter(username=username):
            return redirect('login')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1,
                                            last_name=last_name,
                                            first_name=first_name)
            user.save()
            Teacher.objects.create(user=user)
            my_group = Group.objects.get(name='teachers')
            my_group.user_set.add(user)
            print("user is created")
            return redirect('login')
    else:
        return redirect('login')


def Student_Signup(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']
    if password1 == password2:
        if User.objects.filter(username=username):
            return redirect('login')
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
        return redirect('login')


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
    messages = list(TeacherMessage.objects.filter(teacher=request.user.teacher))
    return render(request, "teacher_templates/all_messages.html", {'messages': messages})


def showSolutions(request):
    teacher = Teacher.objects.get(user=request.user)
    solutions = StudentSolution.objects.filter(teacher=teacher)
    myFilter = StudentSolutionsFilter(request.GET, queryset=solutions)
    solutions = myFilter.qs
    context = {'solutions': solutions, 'myfilter': myFilter}
    return render(request, "teacher_templates/all_solutions.html", context)


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


def showHomework(request):
    student = Student.objects.get(user=request.user)
    homeworks = HomeWork.objects.filter(teacher=student.teacher).all()
    contex = {'homeworks': homeworks}
    return render(request, 'homework_templates/all_homeworks_student.html',contex)


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


# -------------------------------------- student Views ----------------------------------#
# @author Amar Alsana
def student_dashboard(request):
    # created Dashboard for the student that shown for the teacher after loging in
    student = Student.objects.get(user=request.user)

    context = {'homework_list': HomeWork.objects.filter(teacher=student.teacher).all()[:3],
               'message_list': TeacherMessage.objects.filter(teacher=student.teacher).last(),
               'adminMessage': AdminMessage.objects.last(), 'grade_list': Grade.objects.last(),
               'studies_list': Studies.objects.filter(teacher=student.teacher).all()[:3]
               }
    # context = dictionary that content the whole elements that dashboard need to use

    return render(request, "student_templates/studentDashBoard.html", context)

def showStudentHomeworks(request):
    student = Student.objects.get(user=request.user)
    homeworks=HomeWork.objects.filter(teacher=student.teacher)
    context = {'homework_list': homeworks}
    return render(request, "student_templates/showStudentHomeworks.html", context)


def showSingleHomeWork(request,id):
    homework=HomeWork.objects.get(pk=id)
    form=HomeworkForm(instance=homework)
    context = {'homework': homework}
    return render(request, "student_templates/showSingleHomeWork.html", context)


# ------------------------------------- bug Views ----------------------------------#
# @author Amar Alsana
def bugreport(request):
    if request.method == "GET":

        form = BugReportForm()
        return render(request, "bugReport_templates/bugReport_form.html", {'form': form})
    else:

        form = BugReportForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, "bugReport_templates/thanks.html")

        # @author Amar Alsana


def showStudies(request):
    studet = Student.objects.get(user=request.user)
    studies = StudiesStudent.objects.filter(student=studet)
    return render(request, "studies_templates/studies_to_show.html", {'studies': studies})


def approveStudy(request, id):
    studentStudy = StudiesStudent.objects.get(pk=id)
    studentStudy.finishedFlag = True
    studentStudy.save()
    return redirect('showAllStudies')


def showStudiesTeacher(request):
    teacher = Teacher.objects.get(user=request.user)
    studies = Studies.objects.filter(teacher=teacher)
    return render(request, "studies_templates/studiesTable_template.html", {'studies': studies})


def study_form(request, id=0):
    # creating new form for inserting or editing existed admin messages
    if request.method == "GET":
        if id == 0:
            form = studyForm()


        else:
            message = Studies.objects.get(pk=id)

            form = studyForm(instance=message)

        return render(request, "studies_templates/study_form.html", {'form': form})
    else:
        if id == 0:
            form = studyForm(request.POST)
            teacher = Teacher.objects.get(user=request.user)
            student = Student.objects.filter(teacher=teacher)

            for i in student:
                new_study_student = StudiesStudent.objects.create(student=i, study=form.save(), finishedFlag=False)
                new_study_student.save()

        else:
            study = Studies.objects.get(pk=id)
            form = studyForm(request.POST, instance=study)
        if form.is_valid():
            form.save()
        return redirect('showStudentTeacher')


def study_delete(request, id):
    study = Studies.objects.get(pk=id)
    study.delete()
    return redirect('showStudentTeacher')
