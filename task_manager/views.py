from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext as _
from django.views import View

from task_manager.mixins import SpecifiedLoginRequiredMixin


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


class UserLogout(SpecifiedLoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("Вы разлогинены"))
        return super().dispatch(request, *args, **kwargs)
