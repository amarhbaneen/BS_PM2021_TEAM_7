
from django.urls import path,include
from . import views

urlpatterns = [

    path('homepage',views.homepage,name='homepage'),
    path('user_list/',views.user_list,name="user_list"),
    path('update/<int:id>',views.user_form_edit,name="update_user_info"),
    path('delete/<int:id>',views.delete_user,name="delete_user"),
    path('create_user/',views.create_user,name="create_user"),
    path('show_details/<int:id>',views.showUser,name="show_details")
]
