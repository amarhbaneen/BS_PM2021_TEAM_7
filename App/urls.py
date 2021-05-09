from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('dashboard/', views.adminPage, name='dashboard'),
    path('login/', views.login, name='login'),
    path('Registration/', views.Signup, name='Signup'),
    path('teacher', views.teacher_dashboard, name='teacher'),
    path('delete_homework/<int:id>/', views.homework_delete, name='homework_delete'),
    path('homeworkform/', views.homework_form, name='homework_form'),
    path('SolutionForm/', views.Solution_form, name='Solution_form'),
    path('homeowrk<int:id>/', views.homework_form, name='homework_update'),
    path('profile',views.profile,name='profile'),
    path('createmessage/', views.admin_message_form, name='createmessage'),
    path('editAdminMessage/<int:id>', views.admin_message_form, name='editAdminMessage'),
    path('deleteAdminMessage/<int:id>', views.admin_mesaage_delete, name='deleteAdminMessage'),
    path('createTeacherMessage', views.teacher_message_form, name='create_teacher_message'),
    path('editTeacherMessage/<int:id>', views.teacher_message_form, name='editTeacherMessage'),
    path('deleteTeacherMessage/<int:id>', views.teacher_mesaage_delete, name='deleteTeacherMessage'),
    path('teacherMessages',views.showMessages,name="teacherMessages"),
    path('logout',views.logoutUser,name="logout"),
    path('studentdashboard',views.student_dashboard,name="student_dashboard"),
    path('bugreport',views.bugreport,name="bugreport"),
    path('showSolutions', views.showSolutions, name="showSolutions"),
    path('allstudies',views.showStudies,name='showAllStudies'),
    path('approveStudy/<int:id>',views.approveStudy,name="approve_study"),
    path('studiesTeacher',views.showStudiesTeacher,name="showStudentTeacher"),
    path('studyForm',views.study_form,name="addstudy"),
    path('studyform/<int:id>',views.study_form,name="study_update"),
    path('studyform_delete/<int:id>', views.study_delete, name="study_delete"),
    path('allhomework_student',views.showHomework,name='showhomeworkstudent'),
    path('myHomeWorks',views.showStudentHomeworks,name="myHomeWorks"),
    path('showHomeWork/<int:id>',views.showSingleHomeWork,name="showHomeWork"),
    path('addGrade/<int:id>', views.addGrade, name="addGrade"),



    path('user_list/',views.user_list,name="user_list"),
    path('update/<int:id>',views.user_form_edit,name="update_user_info"),
    path('delete/<int:id>',views.delete_user,name="delete_user"),
    path('create_user/',views.create_user,name="create_user"),
    path('show_details/<int:id>',views.showUser,name="show_details"),
    path('createSolution/<int:id>',views.createSolution,name="createSolution")
]
