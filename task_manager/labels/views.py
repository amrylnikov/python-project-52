from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.translation import gettext as _
from django.views.generic.list import ListView

from task_manager.labels.forms import CreateLabelForm
from task_manager.labels.models import Label
from task_manager.mixins import SpecifiedLoginRequiredMixin


class LabelCreate(SpecifiedLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateLabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = _("Метка успешно создана")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class LabelShow(SpecifiedLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    paginate_by = 100


class LabelEdit(SpecifiedLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/update.html'
    form_class = CreateLabelForm
    success_url = reverse_lazy('labels')
    success_message = _("Метка успешно изменена")


class LabelDelete(SpecifiedLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'auth/label_confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _("Метка успешно удалена")
