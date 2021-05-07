from django.test import TestCase
from django.urls import reverse
from django.test import Client
from App.models import *
import requests
# Create your tests here.


# ------------tests for some admin functionality  ------     -- ------------------
class AdminMessageFormTests(TestCase):
    def test_Add_Message_GET(self):
        c = Client()
        response = c.get(reverse('createmessage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'admin_templates/admin_message_form.html')

    def test_Add_Message_GET2(self):
        c = Client()
        response = c.get(reverse('createmessage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'teacher_templates/message_form.html')



    def test_delete_message_POST(self):
        url="http://127.0.0.1:8000/deleteAdminMessage/4"
        response=requests.delete(url)
        print(response.status_code)
        self.assertEquals(response.status_code,403)

# -----------------------------tests for  Teacher user functionality --------------------

class TeacherMessageFormTests(TestCase):
    def test_Add_Teacher_Message_GET(self):
        c = Client()
        response = c.get(reverse('create_teacher_message'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'teacher_templates/message_form.html')

    def test_Add_Message_Template(self):
        c = Client()
        response = c.get(reverse('create_teacher_message'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'login.html')



    def test_deleteTeacher_message_POST(self):
        url="http://127.0.0.1:8000/deleteTeacherMessage/4"
        response=requests.delete(url)
        print(response.status_code)
        self.assertEquals(response.status_code,403)






