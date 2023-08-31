from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.translation import gettext as _

from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status
from task_manager.mixins import SpecifiedLoginRequiredMixin


class StatusCreate(SpecifiedLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateStatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _("Статус успешно создан")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class StatusShow(SpecifiedLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'statuses/statuses.html', {
            'statuses': statuses,
        })


class StatusEdit(SpecifiedLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = CreateStatusForm
    success_message = _("Статус успешно изменен")

    def get_success_url(self):
        return reverse('statuses')


class StatusDelete(SpecifiedLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'auth/status_confirm_delete.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, _("Статус успешно удален"))
        return redirect(self.success_url)
