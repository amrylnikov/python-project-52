from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class StatusCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    form_class = CreateStatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно создан"

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class StatusShow(LoginRequiredMixin, View):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'statuses/statuses.html', {
            'statuses': statuses,
        })


# html форма кривая
class StatusEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    model = Status
    template_name = 'edit.html'
    form_class = CreateStatusForm
    success_message = "Статус успешно обновлен!"

    def get_success_url(self):
        return reverse('statuses')


# Не выводится сообщение
class StatusDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    model = Status
    template_name = 'auth/status_confirm_delete.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Статус успешно удалён!")
        return redirect(self.success_url)
