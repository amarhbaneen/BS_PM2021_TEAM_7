from django.test import TestCase,Client
from django.urls import reverse

# Create your tests here.
from djangoProject.views import addMessage
from .models import AdminMessage
from .forms import AdminMessageForm

class TestAddHomeWork(TestCase):
    def AddHomeWork_test(self):
        client = Client()
        response = client.get('/homeworkform/')
        self.assertTemplateUsed(response,"homework_form.html")
        self.assertEquals(response.status_code,200)



class AdminMessageFormTests(TestCase):
    def test_Add_Message_GET(self):
        c=Client()
        response=c.get(reverse('createMess'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'AddAmessages.html')

    def test_Add_Message_POST(self):
        c = Client()
        data = {'messageContent': 'this is a test for the post method'}

        responce = c.post(reverse('createMess'))
        self.assertEquals(responce.status_code, 302)
        self.assertTemplateNotUsed(responce,'index.html')







