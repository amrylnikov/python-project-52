from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from task_manager.mixins import CustomLoginRequiredMixin


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class TaskGetInfo(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        form = CreateTaskForm(instance=task)
        return render(request, 'tasks/task.html', {'form': form, 'task': task})


class TaskCreate(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class TaskShow(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
        tasks = task_filter.qs

        if request.GET.get('self_tasks'):
            tasks = task_filter.qs.filter(author=request.user)

        return render(request, 'tasks/tasks.html', {
            'form': task_filter.form,
            'tasks': tasks,
        })


class TaskEdit(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    form_class = CreateTaskForm
    success_message = "Задача успешно изменена"

    def get_success_url(self):
        return reverse('tasks')


class TaskDelete(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'auth/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Задача успешно удалена")
        return redirect(self.success_url)

# Удалять задачи может их создатель
# Добавить индивидуальную задачу