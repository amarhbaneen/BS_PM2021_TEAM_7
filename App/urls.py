from django.urls import path, include
from . import views

urlpatterns = [

    path('homepage', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),

]
