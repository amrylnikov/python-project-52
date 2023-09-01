from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django.views.generic.list import ListView

from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from task_manager.mixins import VerboseLoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class TaskGetInfo(VerboseLoginRequiredMixin, DetailView):
    template_name = 'tasks/task.html'
    model = Task
    context_object_name = 'task'


class TaskCreate(VerboseLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = _("Задача успешно создана")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class TaskShow(VerboseLoginRequiredMixin, FilterView, ListView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('self_tasks'):
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context


class TaskEdit(VerboseLoginRequiredMixin, UserPassesTestMixin,
               SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks')
    success_message = _("Задача успешно изменена")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author


class TaskDelete(VerboseLoginRequiredMixin, UserPassesTestMixin,
                 SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'auth/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _("Задача успешно удалена")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author
