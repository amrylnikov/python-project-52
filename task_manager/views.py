from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import VerboseLoginRequiredMixin


class UserLogin(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('index')
    success_message = _("Вы залогинены")

    def form_invalid(self, form):
        messages.error(self.request, _(
            'Пожалуйста, введите правильные имя пользователя и пароль. '
            'Оба поля могут быть чувствительны к регистру.'
        ))
        return super().form_invalid(form)


class UserLogout(VerboseLoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("Вы разлогинены"))
        return super().dispatch(request, *args, **kwargs)
