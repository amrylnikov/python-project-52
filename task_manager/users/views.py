from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from task_manager.users.forms import RegisterUserForm


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Вы залогинены'))
            return redirect('index')
        else:
            messages.error(request, ('''Пожалуйста, введите правильные имя
                                       пользователя и пароль. Оба поля могут
                                       быть чувствительны к регистру.'''))
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('Вы разлогинены'))
    return redirect('index')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Registration Successful!"))
            return redirect('login')
        messages.error(request, (form.errors))
        return render(request, 'registration.html', {
            'form': form,
        })
    else:
        form = RegisterUserForm()
        return render(request, 'registration.html', {
            'form': form,
        })


def show_users(request):
    return render(request, 'users.html')
