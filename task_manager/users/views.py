from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.users.forms import RegisterUserForm


class UserRegister(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован"

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    # Для ошибок пароля. Удалить при проверке
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class UsersShow(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users.html', {
            'users': users,
        })


class UserEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    model = User
    template_name = 'edit.html'
    form_class = RegisterUserForm
    success_message = "Пользователь успешно изменен!"

    def get_success_url(self):
        return reverse('users')


class UserDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    model = User
    template_name = 'auth/user_confirm_delete.html'
    success_url = reverse_lazy('users')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Пользователь успешно удалён!")
        return redirect(self.success_url)

# TODO В логине исправить сообщения в html, щас там только опасности.
# TODO Проверить в html что на нужных страницах проверяется, залогиген ли юзер
# (если ты в браузере ссылку на изменение вобьёшь например)
# А как? Надо ж редирект делать, но проверить я могу только в html i guess?
# Нельзя удалить пользователя если он связан с задачами. И метки тжс. Как?
