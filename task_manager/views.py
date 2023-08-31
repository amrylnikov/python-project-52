from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class UserLogin(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, _("Вы залогинены"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _(
            'Пожалуйста, введите правильные имя пользователя и пароль. '
            'Оба поля могут быть чувствительны к регистру.'
        ))
        return super().form_invalid(form)


class UserLogout(LoginRequiredMixin, View):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _(
                'Вы не авторизованы! Пожалуйста, выполните вход.'
            ))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _("Вы разлогинены"))
        return redirect('index')
