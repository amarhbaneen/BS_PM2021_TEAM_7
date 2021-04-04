from django.shortcuts import render, redirect
from .forms import HomeworkForm


def homework_form(request):

    if request.method == "GET":
        form = HomeworkForm()
        return render(request, "homework_form.html", {'form': form})
    else:
        form = HomeworkForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/teacher')


def teacher_base(request):
    return render(request, "teacher_base.html")
