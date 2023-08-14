from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View

from task_manager.users.forms import RegisterUserForm


class RegisterUser(View):

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request, 'registration.html', {
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Пользователь успешно зарегистрирован"))
            return redirect('login')
        messages.error(request, (form.errors))
        return render(request, 'registration.html', {
            'form': form,
        })


class ShowUsers(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users.html', {
            'users': users,
        })


class EditUser(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        print('user', user)
        form = RegisterUserForm(instance=user)
        print('form', form)
        return render(request, 'edit.html', {'form': form, 'user_id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = RegisterUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Пользователь обновлен!')
            return redirect('articles')


class DeleteUser(View):
    # TODO реализовать страницу удаления пользователя?
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('users')
