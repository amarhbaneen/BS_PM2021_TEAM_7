from django.contrib.auth.decorators import login_required
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
        self.assertTemplateUsed(response, 'admin_templates/admin_message_form.html')

    def test_Add_Message_GET2(self):
        c = Client()
        response = c.get(reverse('createmessage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'teacher_templates/message_form.html')

    def test_Add_Teacher_Message_GET(self):
        c = Client()
        response = c.get(reverse('create_teacher_message'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_templates/message_form.html')
    '''
    def test_deleteTeacher_message_POST(self):
        url = "http://127.0.0.1:8000/deleteTeacherMessage/4"
        response = requests.delete(url)
        print(response.status_code)
        self.assertEquals(response.status_code, 403)
    def test_delete_homework(self):
        url = "http://127.0.0.1:8000/delete_homework/4"
        response = requests.delete(url)
        print(response.status_code)
        self.assertEquals(response.status_code, 403)

    def test_delete_study(self):
        url = "http://127.0.0.1:8000/studyform_delete/4"
        response = requests.delete(url)
        print(response.status_code)
        self.assertEquals(response.status_code, 403)

    def test_update_homework(self):
        url = "http://127.0.0.1:8000/homework_update1"
        response = requests.get(url)
        print(response.status_code)
        self.assertEquals(response.status_code, 404)

    def test_delete_user(self):
        url = "http://127.0.0.1:8000/delete/4"
        response = requests.delete(url)
        print(response.status_code)
        self.assertEquals(response.status_code, 403)
    def test_update_user(self):
        url = "http://127.0.0.1:8000/update/4"
        response = requests.get(url)
        print(response.status_code)
        self.assertEquals(response.status_code, 200)

    def test_update_study(self):
        url = "http://127.0.0.1:8000/studyform/4"
        response = requests.get(url)
        print(response.status_code)
        self.assertEquals(response.status_code, 200)
        '''
# -----------------------------tests for  Teacher user functionality --------------------

class TeacherMessageFormTests(TestCase):


    def test_Add_Message_Template(self):
        c = Client()
        response = c.get(reverse('create_teacher_message'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'login.html')





# -----------------------------tests for  homeworks  functionality --------------------

class homeworkTest(TestCase):

    def test_Add_homework_GET(self):
        c = Client()
        response = c.get(reverse('homework_form'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homework_templates/homework_form.html')




    def test_Add_homework_Template(self):
        c = Client()
        response = c.get(reverse('homework_form'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'login.html')

    def test_AddHomeWork_POST(self):
        c = Client()
        response = c.post(reverse('homework_form'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'teacher_base.html')


# ---------------------------------- test for Studies ---------------------------------------#
class studiesTest(TestCase):
    def test_Add_study_GET(self):
        c = Client()
        response = c.get(reverse('addstudy'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'studies_templates/study_form.html')


    def test_Add_study_Template(self):
        c = Client()
        response = c.get(reverse('addstudy'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'login.html')




# ================================ test for User ======================================#



    def test_login(self):
        login = self.client.login(username='test', password='test')
        self.assertFalse(login)

#=================================== test for Soltuions =========================================#
class SoltuionsTest(TestCase):
    def test_add_soltuion_GET(self):
        c = Client()
        response = c.get(reverse('Solution_form'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_solution.html')
