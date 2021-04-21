from django.shortcuts import render,redirect
from .forms import *

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect ,get_object_or_404

from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render


