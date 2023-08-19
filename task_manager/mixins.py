from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):

    login_url = 'login'
    permission_denied_message = 'Вы не авторизованы! Пожалуйста, выполните вход.!'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.permission_denied_message)
        return super().dispatch(request, *args, **kwargs)
