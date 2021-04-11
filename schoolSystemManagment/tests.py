from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
from djangoProject.views import addMessage
from .models import AdminMessage
from .forms import AdminMessageForm



class TestAddHomeWork(TestCase):
    def test_AddHomeWork(self):
        client = Client()
        response = client.get('homework_form')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "homework_form.html")



class AdminMessageFormTests(TestCase):
    def test_Add_Message_GET(self):
        c = Client()
        response = c.get(reverse('createMess'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'AddAmessages.html')

    def test_Add_Message_POST(self):
        c = Client()
        data = {'messageContent': 'this is a test for the post method'}

        responce = c.post(reverse('createMess'))
        self.assertEquals(responce.status_code, 302)
        self.assertTemplateNotUsed(responce, 'index.html')


class DeletingHomework(TestCase):
    def test_delete_homework_GET(self):
        c = Client()
        response = c.get(reverse('homework_delete', 0))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_base.html')
