from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
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


class StatusShow(SpecifiedLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    paginate_by = 100


class StatusEdit(SpecifiedLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = CreateStatusForm
    success_url = reverse_lazy('statuses')
    success_message = _("Статус успешно изменен")


class StatusDelete(SpecifiedLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'auth/status_confirm_delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _("Статус успешно удален")
