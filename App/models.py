from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import *


# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teachername = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    # teacher model that inherit his auth id from user Table
    def __str__(self):
        return self.user.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    # teacher model that inherit his auth id from user Table
    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class HomeWork(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # every Homework have the id of the teacher who submit it
    # so we can send it to the student page who have the same teacher id
    homeWorkContent = RichTextField(blank=True)  # the content that include the questions of the homework
    homeWorkTitle = models.TextField()

    def __str__(self):
        return self.homeWorkTitle


class StudentSolution(models.Model):
    homeWork = models.ForeignKey(HomeWork, on_delete=models.CASCADE, null=True)
    solutionContent = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "student:  " + self.student.__str__() + "     Solution: " + self.solutionContent + "    Home work: " + self.homeWork.__str__()


class Grade(models.Model):
    solution = models.ForeignKey(StudentSolution, on_delete=models.CASCADE, null=True)
    grade = models.FloatField()
    teacherComment = RichTextField()

    def __str__(self):
        return  self.solution.__str__()


class Studies(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    contentLink = RichTextField(blank=True)
    title = models.TextField()

    def __str__(self):
        return self.title


class StudiesStudent(models.Model):
    study = models.ForeignKey(Studies, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    finishedFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.study.__str__() + self.student.__str__()


class AdminMessage(models.Model):
    messageTitle = models.TextField(default="")
    messageContent = models.TextField(default="")

    def __str__(self):
        return self.messageTitle


class TeacherMessage(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    messageTitle = models.TextField(default="")
    messageContent = models.TextField()

    def __str__(self):
        return self.messageTitle + self.teacher.__str__()


class Bugreport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bugContent = models.TextField()

    def __str__(self):
        return self.bugContent


class TeacherId(models.Model):
    teacherId = models.IntegerField()


    def __str__(self):
        return self.teacherId