from django.contrib import auth
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django import template
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import UpdateView

from App.forms import *
from App.models import *
from App.filters import *


def adminPage(request):
    userList = User.objects.all()[:3]
    messageList = AdminMessage.objects.all()[:3]
    totalusers = User.objects.all().count()
    countTeacher = Teacher.objects.all().count()
    countStudent = Student.objects.all().count()
    context = {'userList': userList, 'messageList': messageList, 'totalusers': totalusers, 'countTeacher': countTeacher,
               'countStudent': countStudent}
    return render(request, 'dashboard.html', context)


def home(requset):
    return render(requset, 'home.html')


def profile(request):
    user = request.user
    form = User_edit_form(instance=user)
    if request.method == 'POST':

        form = User_edit_form(request.POST, instance=user)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'profile.html', context)


def login(request):
    if request.user.is_authenticated == False:
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
    else:
        if request.user.groups.filter(name='admins'):
            return redirect('dashboard')
        if request.user.groups.filter(name='students'):
            return redirect('student_dashboard')
        if request.user.groups.filter(name='teachers'):
            return redirect('teacher')


def Teacher_Signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        id = request.POST['id']
        email = request.POST['email']
        if password1 == password2:
            if not TeacherId.objects.filter(teacherId=id).count() == 1:
                messages.error(request, 'your id is wrong')
            elif User.objects.filter(username=username):
                messages.error(request, 'username is taken')

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
            messages.error(request, 'passwords doesnt mach')




    return render(request, 'teacher_templates/teacher_register.html')


def Student_Signup(request):
    teachers = ((teacher.user)
                for teacher in Teacher.objects.all())
    context = {'teachers': teachers}

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        teacherusername = request.POST.get('teachers')
        teacheruser = User.objects.get(username=teacherusername)
        teacher = Teacher.objects.get(user=teacheruser)
        if password1 == password2:
            if User.objects.filter(username=username):
                messages.error(request, 'username is taken')

            else:
                user = User.objects.create_user(username=username, email=email, password=password1,
                                                last_name=last_name,
                                                first_name=first_name)
                user.save()
                Student.objects.create(user=user, teacher=teacher)
                my_group = Group.objects.get(name='students')
                my_group.user_set.add(user)
                print("user is created")
                return redirect('login')
        else:
            messages.error(request, 'passwords doesnt mach')

    return render(request, 'student_templates/student_register.html', context)


def createSolution(request, id):
    SolutionFormSet = inlineformset_factory(Student, StudentSolution, fields=('solutionContent',), extra=1,
                                            can_delete=False)
    student = Student.objects.get(user=request.user)
    homeWork = HomeWork.objects.get(pk=id)
    teacher = student.teacher
    initial = {'homeWork': homeWork, 'teacher': teacher, 'student': student}

    formset = SolutionFormSet(queryset=StudentSolution.objects.none(), instance=student)
    if request.method == 'POST':
        formset = SolutionFormSet(request.POST, instance=student)
        if formset.is_valid():
            sol = formset.save(commit=False)
            sol[0].homeWork = homeWork
            sol[0].teacher = teacher
            sol[0].save()
            return redirect('student_dashboard')
    context = {'form': formset}
    return render(request, 'student_templates/createSolution.html', context)


def editSolution(request, id):
    if request.method == "GET":
        if id == 0:
            form = SolutionForm()
        else:
            solution = StudentSolution.objects.get(pk=id)
            form = SolutionForm(instance=solution)
        return render(request, "student_templates/EditSolution.html", {'form': form})

    else:
        if id == 0:
            form = SolutionForm(request.POST)

        else:
            solution = StudentSolution.objects.get(pk=id)
            form = SolutionForm(request.POST, instance=solution)
        if form.is_valid():
            form.save()
        return redirect('student_dashboard')


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


# ------------------------ Grades Views ---------------------
def addGrade(request, id):
    GradeFormSet = inlineformset_factory(StudentSolution, Grade, fields=('grade', 'teacherComment'), extra=1)
    solution = StudentSolution.objects.get(pk=id)
    formset = GradeFormSet(instance=solution)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = OrderForm(request.POST)
        formset = GradeFormSet(request.POST, instance=solution)
        if formset.is_valid():
            formset.save()
            return redirect('teacher')

    context = {'form': formset, 'solution': solution}
    return render(request, 'teacher_templates/addGrade.html', context)


# -------------------------------------- homework Views ----------------------------------#
def homework_form(request, id=0):
    user=User.objects.get(username=request.user)
    teacher=Teacher.objects.get(user=user)
    data={'teacher':teacher}
    # creating new form for inserting or editing existed homework
    if request.method == "GET":
        if id == 0:
            form = HomeworkForm(initial=data)




        else:
            homework = HomeWork.objects.get(pk=id)
            form = HomeworkForm(instance=homework,initial=data)

        return render(request, "homework_templates/homework_form.html", {'form': form})
    else:
        if id == 0:
            form = HomeworkForm(request.POST,initial=data)

        else:
            homework = HomeWork.objects.get(pk=id)
            form = HomeworkForm(request.POST, instance=homework,initial=data)
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
    return render(request, 'homework_templates/all_homeworks_student.html', contex)




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
        return redirect('dashboard')


def admin_mesaage_delete(request, id):
    message = AdminMessage.objects.get(pk=id)
    message.delete()
    return redirect('dashboard')


def showAdminMessages(request):
    messages = list(AdminMessage.objects.all())
    return render(request, "admin_templates/all_messages.html", {'messages': messages})


# -------------------------------------- student Views ----------------------------------#
# @author Amar Alsana
def student_dashboard(request):
    # created Dashboard for the student that shown for the teacher after loging in
    homeWorks_Exist = []

    student = Student.objects.get(user=request.user)
    homeworks = HomeWork.objects.filter(teacher=student.teacher).all()[:3]
    for hw in homeworks:
        sol = StudentSolution.objects.filter(homeWork=hw, student=student, teacher=student.teacher)
        if sol.count() > 0:
            homeWorks_Exist.append([hw, False, sol.first()])
        else:
            homeWorks_Exist.append([hw, True, None])

    context = {'homeWorks_Exist': homeWorks_Exist,
               'message_list': TeacherMessage.objects.filter(teacher=student.teacher).last(),
               'adminMessage': AdminMessage.objects.last(), 'grade_list': Grade.objects.last(),
               'studies_list': Studies.objects.filter(teacher=student.teacher).all()[:3]
               }
    # context = dictionary that content the whole elements that dashboard need to use

    return render(request, "student_templates/studentDashBoard.html", context)


def showStudentHomeworks(request):
    homeWorks_Exist = []

    student = Student.objects.get(user=request.user)
    homeworks = HomeWork.objects.filter(teacher=student.teacher)
    for hw in homeworks:
        sol = StudentSolution.objects.filter(homeWork=hw, student=student, teacher=student.teacher)
        if sol.count()>0:
            homeWorks_Exist.append([hw,False,sol.first()])
        else:
            homeWorks_Exist.append([hw, True,None])



    context = {'homework_list': homeworks, 'homeWorks_Exist': homeWorks_Exist}
    return render(request, "student_templates/showStudentHomeworks.html", context)


def showSingleHomeWork(request, id):
    homework = HomeWork.objects.get(pk=id)
    student = Student.objects.get(user=request.user)
    form = HomeworkForm(instance=homework)
    isSolutionExist=True
    sol=StudentSolution.objects.filter(homeWork=homework,student=student,teacher=student.teacher)
    if sol.count()>0:
        isSolutionExist=False
    context = {'homework': homework,'isSolutionExist':isSolutionExist,'solution':sol.first()}
    return render(request, "student_templates/showSingleHomeWork.html", context)


def Solution_form(request):
    form = SolutionForm(request.POST or None)
    if form.is_valid():
        if request.user.is_authenticated:
            student_username = request.user.username
        form.student = student_username
        form.save()
    context = {
        'form': form
    }
    return render(request, 'student_solution.html', context)


def myGrades(request):
    student = Student.objects.get(user=request.user)
    solutions = StudentSolution.objects.filter(student=student)

    grades = Grade.objects.filter(solution__in=solutions).all()
    context = {'grades': grades}
    return render(request, 'student_templates/studentGrades.html', context)


def myTeacherComment(request, id):
    grade = Grade.objects.get(pk=id)

    context = {'grade': grade}
    return render(request, 'student_templates/myteacherComment.html', context)


def createSolution(request, id):
    student = Student.objects.get(user=request.user)
    homeWork = HomeWork.objects.get(pk=id)
    teacher = student.teacher
    data = [{'student': student, 'homeWork': homeWork, 'teacher': teacher}]
    SolutionFormSet = modelformset_factory(StudentSolution, form=SolutionForm,
                                           exclude=('homeWork', 'teacher', 'student',), extra=1)
    formset = SolutionFormSet(queryset=StudentSolution.objects.none())

    if request.method == 'POST':
        formset = SolutionFormSet(request.POST)
        if formset.is_valid():
            instance = formset.save(commit=False)
            instance[0].student = student
            instance[0].homeWork = homeWork
            instance[0].teacher = teacher
            instance[0].save()
            return redirect('myHomeWorks')
    context = {'form': formset,'homeWork':homeWork}
    return render(request, 'student_templates/createSolution.html', context)


def editSolution(request, id, sol_id):
    student = Student.objects.get(user=request.user)
    homeWork = HomeWork.objects.get(pk=id)
    teacher = student.teacher
    data = [{'student': student, 'homeWork': homeWork, 'teacher': teacher}]
    SolutionFormSet = modelformset_factory(StudentSolution, form=SolutionForm,
                                           exclude=('homeWork', 'teacher', 'student',), extra=0)
    formset = SolutionFormSet(queryset=StudentSolution.objects.filter(pk=sol_id))

    if request.method == 'POST':
        formset = SolutionFormSet(request.POST)
        if formset.is_valid():
            if formset.has_changed():
                instance = formset.save(commit=False)
                instance[0].student = student
                instance[0].homeWork = homeWork
                instance[0].teacher = teacher
                instance[0].save()
            return redirect('myHomeWorks')
    context = {'form': formset}
    return render(request, 'student_templates/createSolution.html', context)


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


def user_list(request):
    myFilter = userFilter(request.GET, queryset=User.objects.all())

    user_list = myFilter.qs

    context = {'user_list': user_list, 'myFilter': myFilter}

    return render(request, "user_list.html", context)


def user_form_edit(request, id):
    user = User.objects.get(pk=id)
    form = User_edit_form(instance=user)
    if request.method == 'POST':
        a = request.POST['username']
        form = User_edit_form(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    context = {'form': form}
    return render(request, 'user_form_info.html', context)


def delete_user(request, id):
    user = User.objects.get(pk=id)
    user.delete()
    return redirect('user_list')


def create_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            curr_user = form.save()
            Teacher.objects.create(user=curr_user)
            return redirect('user_list')
    return render(request, "create_user.html", {"form": form})


def showUser(request, id):
    user = User.objects.get(pk=id)
    context = {'user': user}
    return render(request, 'show_details.html', context)


def addTeacher(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            curr_user = form.save()
            Teacher.objects.create(user=curr_user)
            my_group = Group.objects.get(name='teachers')
            my_group.user_set.add(curr_user)
            return redirect('user_list')
    return render(request, "admin_templates/addTeacher.html", {"form": form})


# def search(request):
#     if request.method=='POST':
#         searched=request.POST['searched']
#         user_list=User.objects.all()
#         user_filter=user_list.filter(username=searched)
#         return render(request,'user_list.html',{'user_filter':user_filter})
#     else:
#         return render(request,'user_list.html',{})


def addStudent(request):
    form = UserCreationForm()
    teachers = ((teacher.user)
                for teacher in Teacher.objects.all())
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        teacherusername = request.POST.get('teacher')
        teacheruser = User.objects.get(username=teacherusername)
        teacher = Teacher.objects.get(user=teacheruser)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user, teacher=teacher)
            my_group = Group.objects.get(name='students')
            my_group.user_set.add(user)
            return redirect('user_list')
    context = {'form': form, 'teachers': teachers}
    return render(request, 'admin_templates/addStudent.html', context)


def showMyStudents(request):
    students = list(Student.objects.filter(teacher=request.user.teacher))
    return render(request, "teacher_templates/allStudent.html", {'students': students})


def showStudy(request ,id):
    study = Studies.objects.get(pk=id)
    contex = {'studies': study}
    return render(request, 'student_templates/allStudies.html', contex)