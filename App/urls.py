from django.urls import path, include
from . import views

urlpatterns = [

    path('homepage', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('teacher', views.teacher_dashboard, name='teacher'),
    path('delete_homework/<int:id>/', views.homework_delete, name='homework_delete'),
    path('homeworkform/', views.homework_form, name='homework_form'),
    path('homeowrk<int:id>/', views.homework_form, name='homework_update'),
    path('bugreportform/', views.bug_report_form, name='bugreportform'),
]
