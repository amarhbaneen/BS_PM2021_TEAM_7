from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
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
    homeWorkContent = models.TextField  # the content that include the questions of the homework


class StudentSolution(models.Model):
    id = models.IntegerField(primary_key=True)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    solutionContent = models.TextField


class Grade(models.Model):
    id = models.IntegerField(primary_key=True)
    homeWorkId = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.FloatField
    teacherComment = models.TextField


class Studies(models.Model):
    id = models.IntegerField(primary_key=True)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    contentLink = models.TextField


class StudiesStudent(models.Model):
    id = models.IntegerField(primary_key=True)
    studyId = models.ForeignKey(Studies, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    finishedFlag = models.BooleanField(default=False)


class AdminMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    adminId = models.ForeignKey(Admin, on_delete=models.CASCADE)
    messageContent = models.TextField


class TeacherMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    messageContent = models.TextField
