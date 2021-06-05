from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.test import TestCase,tag
from django.urls import reverse
from django.test import Client
from App.models import *
import requests


# Create your tests here.


# ------------tests for some admin functionality  ------     -- ------------------
@tag("unit_test")
class AdminMessageFormTests(TestCase):
    @tag('unit-test')
    def test_Add_Message_GET(self):
        c = Client()
        response = c.get(reverse('createmessage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_templates/admin_message_form.html')

    @tag('unit-test')
    def test_Add_Message_GET2(self):
        c = Client()
        response = c.get(reverse('createmessage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'teacher_templates/message_form.html')

    @tag('unit-test')
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

    @tag('unit-test')
    def test_Add_Message_Template(self):
        c = Client()
        response = c.get(reverse('create_teacher_message'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'login.html')





# -----------------------------tests for  homeworks  functionality --------------------

class homeworkTest(TestCase):

    '''def test_Add_homework_GET(self):
        c = Client()
        response = c.get(reverse('homework_form'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homework_templates/homework_form.html')'''




    '''def test_Add_homework_Template(self):
        c = Client()
        response = c.get(reverse('homework_form'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'login.html')'''

    '''def test_AddHomeWork_POST(self):
        c = Client()
        response = c.post(reverse('homework_form'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'teacher_base.html')'''


# ---------------------------------- test for Studies ---------------------------------------#
class studiesTest(TestCase):
    @tag('unit-test')
    def test_Add_study_GET(self):
        c = Client()
        response = c.get(reverse('addstudy'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'studies_templates/study_form.html')

    @tag('unit-test')
    def test_Add_study_Template(self):
        c = Client()
        response = c.get(reverse('addstudy'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'login.html')




# ================================ test for User ======================================#

    @tag('unit-test')
    def test_login(self):
        login = self.client.login(username='test', password='test')
        self.assertFalse(login)

#=================================== test for Soltuions =========================================#
class SoltuionsTest(TestCase):
    @tag('unit-test')
    def test_add_soltuion_GET(self):
        c = Client()
        response = c.get(reverse('Solution_form'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_solution.html')




#=================================== test  =========================================#


class loginTest(TestCase):

    @tag('unit-test')
    def test_login_access_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_login_access_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_login_access_url_negative(self):
        response = self.client.get('/login/')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_login_access_name_negative(self):
        response = self.client.get(reverse('login'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def testLoginUsedTemplate(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'login.html')

    @tag('unit-test')
    def testLogin_NOT_UsedTemplate(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response,'home.html')

    @tag('unit-test')
    def testUserLogin(self):

        User.objects.create(username='aa', password='aa')

        data = {'username': 'a12', 'password': '1234'}
        response=self.client.post(reverse('login'),data=data,follow=True)
        self.assertEqual(response.status_code,200)
        '''the reason why it redircets to login that's this user doesnt belong to any group'''
        self.assertRedirects(response, reverse('login'))

    @tag('integration-test')
    def testLoginAndLogout(self):
        User.objects.create(username='aa', password='aa')

        data = {'username': 'a12', 'password': '1234'}
        response = self.client.post(reverse('login'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        '''the reason why it redircets to login that's this user doesnt belong to any group'''
        self.assertRedirects(response, reverse('login'))
        self.assertTemplateUsed(response, 'login.html')




        response = self.client.get(reverse('logout'), follow=True)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)


class RegisterTest_Teacher(TestCase):
    @tag('unit-test')
    def test_register_access_url(self):
        response = self.client.get('/Teacher_Register/')
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_register_access_name(self):
        response = self.client.get(reverse('Teacher_Signup'))
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_register_access_url_negative(self):
        response = self.client.get('/Teacher_Register/')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_register_access_name_negative(self):
        response = self.client.get(reverse('Teacher_Signup'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def testRegisterUsedTemplate(self):
        response = self.client.get(reverse('Teacher_Signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_templates/teacher_register.html')

    @tag('unit-test')
    def testRegister_NOT_UsedTemplate(self):
        response = self.client.get(reverse('Teacher_Signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'home.html')

    @tag('unit-test')
    def testTeacherRegister(self):
        User.objects.create(username='aa', password='aa')


        data = {'first_name': 'a12', 'last_name': '1234','username':'username',
                'password1':'password1','password2':'password2','id':'id','email':'email'}
        response = self.client.post(reverse('Teacher_Signup'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.filter(username='aa')),1)



    @tag('integration-test')
    def testRegisterTeacherAndLogin(self):
        #User.objects.create(username='aa', password='aa')

        data_login = {'username': 'aa', 'password': '1234'}
        data_register = {'first_name': 'aa', 'last_name': '1234', 'username': 'username',
                'password1': 'password1', 'password2': 'password2', 'id': 'id', 'email': 'email'}

        response = self.client.post(reverse('Teacher_Signup'), data=data_register, follow=True)

        self.assertEqual(response.status_code, 200)


        response = self.client.post(reverse('login'), data=data_login, follow=True)


        self.assertTemplateUsed(response, 'login.html')
        self.assertRedirects(response, reverse('login'))


    @tag('integration-test')
    def testRegisterTeacherAndLoginAndLogout(self):
        #User.objects.create(username='aa', password='aa')

        data_login = {'username': 'aa', 'password': '1234'}
        data_register = {'first_name': 'aa', 'last_name': '1234', 'username': 'username',
                'password1': 'password1', 'password2': 'password2', 'id': 'id', 'email': 'email'}

        response = self.client.post(reverse('Teacher_Signup'), data=data_register, follow=True)

        self.assertEqual(response.status_code, 200)


        response = self.client.post(reverse('login'), data=data_login, follow=True)


        self.assertTemplateUsed(response, 'login.html')
        self.assertRedirects(response, reverse('login'))

        response = self.client.get(reverse('logout'), follow=True)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)

class RegisterTest_Student(TestCase):
    @tag('unit-test')
    def test_register_access_url(self):
        response = self.client.get('/Student_Register/')
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_register_access_name(self):
        response = self.client.get(reverse('Student_Signup'))
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_register_access_url_negative(self):
        response = self.client.get('/Student_Register/')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_register_access_name_negative(self):
        response = self.client.get(reverse('Student_Signup'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def testRegisterUsedTemplate(self):
        response = self.client.get(reverse('Student_Signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_templates/student_register.html')

    @tag('unit-test')
    def testRegister_NOT_UsedTemplate(self):
        response = self.client.get(reverse('Student_Signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'home.html')

    @tag('unit-test')
    def testStudentRegister(self):
        User.objects.create(username='aa', password='aa')


        data = {'first_name': 'a12', 'last_name': '1234','username':'username',
                'password1':'password1','password2':'password2','id':'id','email':'email'}
        response = self.client.post(reverse('Teacher_Signup'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.filter(username='aa')),1)



    @tag('integration-test')
    def testRegisterStudentAndLogin(self):
        #User.objects.create(username='aa', password='aa')

        data_login = {'username': 'aa', 'password': '1234'}
        data_register = {'first_name': 'aa', 'last_name': '1234', 'username': 'username',
                'password1': 'password1', 'password2': 'password2', 'id': 'id', 'email': 'email'}

        response = self.client.post(reverse('Teacher_Signup'), data=data_register, follow=True)

        self.assertEqual(response.status_code, 200)


        response = self.client.post(reverse('login'), data=data_login, follow=True)


        self.assertTemplateUsed(response, 'login.html')
        self.assertRedirects(response, reverse('login'))


    @tag('integration-test')
    def testRegisterTeacherAndLoginAndLogout(self):
        #User.objects.create(username='aa', password='aa')

        data_login = {'username': 'aa', 'password': '1234'}
        data_register = {'first_name': 'aa', 'last_name': '1234', 'username': 'username',
                'password1': 'password1', 'password2': 'password2', 'id': 'id', 'email': 'email'}

        response = self.client.post(reverse('Teacher_Signup'), data=data_register, follow=True)

        self.assertEqual(response.status_code, 200)


        response = self.client.post(reverse('login'), data=data_login, follow=True)


        self.assertTemplateUsed(response, 'login.html')
        self.assertRedirects(response, reverse('login'))

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)





class LogoutTest(TestCase):
   def testLogout(self):
       User.objects.create(username='username', password='username')
       self.client.login(username='username',password='password')

       response = self.client.get(reverse('logout'), follow=True)

       self.assertEqual(response.status_code, 200)
       self.assertFalse(response.context["user"].is_authenticated)

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', email='email',
                                        last_name='last_name',
                                        first_name='first_name')
        self.user.set_password('password')
        self.user.save()

    @tag('unit-test')
    def test_profile_access_url(self):
        # Arrange
        self.client.force_login(self.user)

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_profile_access_name(self):
        # Arrange
        self.client.force_login(self.user)

        response = self.client.get('/profile')

        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_profile_access_url_Negateve(self):
        # Arrange
        self.client.force_login(self.user)

        response = self.client.get(reverse('profile'))

        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_profile_access_name_Negateve(self):
        # Arrange
        self.client.force_login(self.user)

        response = self.client.get('/profile')

        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def testProfileUsedTemplate(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'profile.html')

    @tag('unit-test')
    def testProfile_NOT_UsedTemplate(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response,'home.html')

    @tag('integration-test')
    def testLoginAndAccsesViewAndLogout(self):

        #Login
        self.client.force_login(self.user)
        #accss view
        response = self.client.get(reverse('profile'))
        self.assertTrue(response.context['user'].is_authenticated)


        self.assertEqual(response.status_code, 200)

        #logout
        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)


class ManageUsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', email='email',
                                        last_name='last_name',
                                        first_name='first_name')
        self.user.set_password('password')
        self.user.save()

    '''@tag('unit-test')'''
    '''def test_editUser_access_url(self):
        # Arrange
        self.client.force_login(self.user)

        response = self.client.get(reverse('update_user_info'),follow=True,data={"id":self.user.id})

        self.assertEqual(response.status_code, 200)'''

    @tag('unit-test')
    def test_editUser_access_name(self):
        # Arrange
        self.client.force_login(self.user)

        response = self.client.get('/profile')

        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_editUser_access_url_Negateve(self):
        # Arrange
        self.client.force_login(self.user)

        response = self.client.get(reverse('profile'))

        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_editUser_access_name_Negateve(self):
        # Arrange
        self.client.force_login(self.user)

        response = self.client.get('/profile')

        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def testeditUserUsedTemplate(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'profile.html')

    @tag('unit-test')
    def testeditUser_NOT_UsedTemplate(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response,'home.html')



##############################################################


class HomeWorkTest_(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', email='email',
                                             last_name='last_name',
                                             first_name='first_name')

    @tag('unit-test')
    def test_add_homework_access_url(self):
        self.client.force_login(self.user)
        Teacher.objects.create(user=self.user)
        response = self.client.get('/homeworkform/')
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_add_homework__access_name(self):
        self.client.force_login(self.user)
        Teacher.objects.create(user=self.user)
        response = self.client.get(reverse('homework_form'))
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_add_homework_access_url_negative(self):
        self.client.force_login(self.user)
        Teacher.objects.create(user=self.user)
        response = self.client.get(reverse('homework_form'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_add_homework_access_name_negative(self):
        self.client.force_login(self.user)
        Teacher.objects.create(user=self.user)
        response = self.client.get(reverse('homework_form'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def testadd_homeworkUsedTemplate(self):
        self.client.force_login(self.user)
        Teacher.objects.create(user=self.user)
        response = self.client.get(reverse('homework_form'))
        #self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homework_templates/homework_form.html')

    @tag('unit-test')
    def testadd_homework_NOT_UsedTemplate(self):
        self.client.force_login(self.user)
        Teacher.objects.create(user=self.user)
        response = self.client.get(reverse('homework_form'))
        self.assertTemplateNotUsed(response, 'home.html')

    @tag('unit-test')
    def testadd_homework(self):
        self.client.force_login(self.user)
        teacher=Teacher.objects.create(user=self.user)
        data={'teacher':teacher,'homeWorkTitle':'homeWorkTitle','homeWorkContent':'homeWorkContent'}
        response = self.client.post(reverse('homework_form'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)



    @tag('integration-test')
    def test_add_homework_WithLogin(self):
        self.client.force_login(self.user)
        teacher = Teacher.objects.create(user=self.user)
        data = {'teacher': teacher, 'homeWorkTitle': 'homeWorkTitle', 'homeWorkContent': 'homeWorkContent'}
        response = self.client.post(reverse('homework_form'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)


        self.assertTemplateUsed(response, 'teacher_templates/teacher_dashboard.html')
        self.assertRedirects(response, reverse('teacher'))


#############################################################

class BugReportTest_(TestCase):

    @tag('unit-test')
    def test_bugreport_access_url(self):

        response = self.client.get('/bugreport',)
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_bugreport__access_name(self):
        response = self.client.get(reverse('bugreport'))
        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_bugreport_access_url_negative(self):

        response = self.client.get('/bugreport')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_register_access_name_negative(self):
        response = self.client.get(reverse('bugreport'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def testRegisterUsedTemplate(self):
        response = self.client.get(reverse('bugreport'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bugReport_templates/bugReport_form.html')

    @tag('unit-test')
    def testRegister_NOT_UsedTemplate(self):
        response = self.client.get(reverse('bugreport'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'home.html')

    @tag('unit-test')
    def test_view(self):
        data = {'bugContent': 'content',}
        response = self.client.post(reverse('bugreport'),data=data,follow=True)
        self.assertEqual(response.status_code, 200)

##########################################################



















