from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.labels.forms import CreateLabelForm
from task_manager.labels.models import Label


class LabelCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    form_class = CreateLabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = "Метка успешно создана"

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class LabelShow(LoginRequiredMixin, View):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request, 'labels/labels.html', {
            'labels': labels,
        })


class LabelEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    model = Label
    template_name = 'edit.html'
    form_class = CreateLabelForm
    success_message = "Метка успешно обновлена!"

    def get_success_url(self):
        return reverse('labels')


class LabelDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    model = Label
    template_name = 'auth/label_confirm_delete.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Метка успешно удалёна!")
        return redirect(self.success_url)
