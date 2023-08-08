from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
            messages.success(request, ("Пользователь успешно зарегистрирован"))
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
    users = User.objects.all()
    print(users)
    return render(request, 'users.html', {
        'users': users,
    })


def edit_user(request, *args, **kwargs):
    if request.method == "POST":
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = RegisterUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Пользователь обновлен!')
            return redirect('articles')
    else:
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        print('user', user)
        form = RegisterUserForm(instance=user)
        print('form', form)
        return render(request, 'edit.html', {'form': form, 'user_id': user_id})


def delete_user(request, *args, **kwargs):
    user_id = kwargs.get('id')
    user = User.objects.get(id=user_id)
    if user:
        user.delete()
    return redirect('users')
