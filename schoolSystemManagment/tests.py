# Create your tests here.
from django.test import TestCase, Client


class TestAddHomeWork(TestCase):
    def AddHomeWork_test(self):
        client = Client()
        response = client.get('/homeworkform/')
        self.assertTemplateUsed(response,"homework_form.html")
        self.assertEquals(response.status_code,200)