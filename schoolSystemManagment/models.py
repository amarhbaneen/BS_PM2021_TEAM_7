from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):

    id = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return  self.userId.username
    # teacher model that inherit his auth id from user Table


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # student model inherit his auth id from User Table and his
    # own teacher by Teacher Table


class Admin(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    # Admin model that inherit his auth id from user Table


class HomeWork(models.Model):
    id = models.IntegerField(primary_key=True)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # every Homework have the id of the teacher who submit it
    # so we can send it to the student page who have the same teacher id
    homeWorkContent = models.TextField(default="")  # the content that include the questions of the homework


class StudentSolution(models.Model):
    id = models.IntegerField(primary_key=True)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    solutionContent = models.TextField(default="")


class Grade(models.Model):
    id = models.IntegerField(primary_key=True)
    homeWorkId = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.FloatField(default=0)
    teacherComment = models.TextField(default="")


class Studies(models.Model):
    id = models.IntegerField(primary_key=True)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    contentLink = models.TextField(default="")


class StudiesStudent(models.Model):
    id = models.IntegerField(primary_key=True)
    studyId = models.ForeignKey(Studies, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    finishedFlag = models.BooleanField(default=False)


class AdminMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    adminId = models.ForeignKey(Admin, on_delete=models.CASCADE,default=1)
    messageContent = models.TextField(default="")


class TeacherMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    messageContent = models.TextField(default="")
