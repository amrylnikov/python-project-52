from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.translation import gettext as _

from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from task_manager.mixins import SpecifiedLoginRequiredMixin


class TaskGetInfo(SpecifiedLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        form = CreateTaskForm(instance=task)
        return render(request, 'tasks/task.html', {'form': form, 'task': task})


class TaskCreate(SpecifiedLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = _("Задача успешно создана")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class TaskShow(SpecifiedLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
        tasks = task_filter.qs
        if request.GET.get('self_tasks'):
            tasks = task_filter.qs.filter(author=request.user)

        return render(request, 'tasks/tasks.html', {
            'form': task_filter.form,
            'tasks': tasks,
        })


class TaskEdit(SpecifiedLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks')
    success_message = _("Задача успешно изменена")


class TaskDelete(SpecifiedLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'auth/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _("Задача успешно удалена")


# TODO Удалять задачи может их создатель
