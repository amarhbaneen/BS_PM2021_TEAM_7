import django_filters
from App.models import *


class StudentSolutionsFilter(django_filters.FilterSet):
    class Meta:
        model = StudentSolution
        fields = ['student','homeWork']
class userFilter(django_filters.FilterSet):
    class Meta:
        model =User
        fields = ['username',]
