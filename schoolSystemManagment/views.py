from django.shortcuts import render, redirect
from .forms import HomeworkForm
from .models import HomeWork


def homework_form(request,id=0):
    if request.method == "GET":
        if id == 0:
            form = HomeworkForm()

        else:
            homework = HomeWork.objects.get(pk=id)
            form = HomeworkForm(instance=homework)

        return render(request, "homework_form.html", {'form': form})
    else:
        if id ==0:
            form = HomeworkForm(request.POST)
        else:
            homework = HomeWork.objects.get(pk=id)
            form=HomeworkForm(request.POST,instance=homework)
        if form.is_valid():
            form.save()
        return redirect('/teacher')


def teacher_base(request):
    contex = {'homework_list': HomeWork.objects.all()}
    return render(request, "teacher_base.html", contex)


def homework_delete(request, id):
    homework = HomeWork.objects.get(pk=id)
    homework.delete()
    return redirect('/teacher')
