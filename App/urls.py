from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('homepage', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('teacher', views.teacher_dashboard, name='teacher'),
    path('delete_homework/<int:id>/', views.homework_delete, name='homework_delete'),
    path('homeworkform/', views.homework_form, name='homework_form'),
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

]
