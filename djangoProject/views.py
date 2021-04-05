from django.shortcuts import render

def Teacherbase(request):
    return render(request,"teacher_base.html")
from django.shortcuts import render, redirect

from schoolSystemManagment.forms import AdminMessageForm

def index(request):
    return render(request, "index.html", )

def addMessage(request):
    if request.method =="POST":
        form = AdminMessageForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/index')

    else:
        form = AdminMessageForm()
        return render(request, "AddAmessages.html", {'form': form})


