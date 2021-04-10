from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.teacher_base),
    path('homeworkform/',views.homework_form),
    path('delete/<int:id>/',views.homework_delete,name='homework_delete'),
    path('<int:id>/', views.homework_form, name='homework_update'),

]