from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.labels.forms import CreateLabelForm
from task_manager.labels.models import Label
from task_manager.mixins import CustomLoginRequiredMixin


class LabelCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateLabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = "Метка успешно создана"

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class LabelShow(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request, 'labels/labels.html', {
            'labels': labels,
        })


class LabelEdit(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'edit.html'
    form_class = CreateLabelForm
    success_message = "Метка успешно изменена"

    def get_success_url(self):
        return reverse('labels')


class LabelDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'auth/label_confirm_delete.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Метка успешно удалена")
        return redirect(self.success_url)
