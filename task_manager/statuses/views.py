from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.translation import gettext as _

from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status
from task_manager.mixins import CustomLoginRequiredMixin


class StatusCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateStatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _("Статус успешно создан")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class StatusShow(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'statuses/statuses.html', {
            'statuses': statuses,
        })


class StatusEdit(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = CreateStatusForm
    success_message = _("Статус успешно изменен")

    def get_success_url(self):
        return reverse('statuses')


class StatusDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'auth/status_confirm_delete.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, _("Статус успешно удален"))
        return redirect(self.success_url)
