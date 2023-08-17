from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class UserLogin(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Вы залогинены"))
            return redirect('index')
        else:
            messages.error(request, ('''Пожалуйста, введите правильные имя
                                       пользователя и пароль. Оба поля могут
                                       быть чувствительны к регистру.'''))
            return redirect('login')


class UserLogout(LoginRequiredMixin, View):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, ("Вы разлогинены"))
        return redirect('index')
