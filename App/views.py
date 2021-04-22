from django.contrib import auth
from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.
def homepage(request):
    return render(request, 'dashboard.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.groups.filter(name='admins').exists():
            auth.login(request, user)
            return render(request, 'AdminPage.html')
        elif user is not None and user.groups.filter(name='students').exists():
            auth.login(request, user)
            return render(request, 'StudentPage.html')
        elif user is not None and user.groups.filter(name='teachers').exists():
            auth.login(request, user)
            return render(request, 'TeacherPage.html')
        else:
            messages.info(request, 'error')
            return redirect('login')
    else:
        return render(request, 'login.html')
