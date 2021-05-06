import django_filters
from App.models import *


class userFilter(django_filters.FilterSet):
    class Meta:
        model =User
        fields = ['username',]
