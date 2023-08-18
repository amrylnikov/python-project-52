from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class TaskGetInfo(LoginRequiredMixin, View):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        print('task_id', task_id)
        task = Task.objects.get(id=task_id)
        print('task', task)
        form = CreateTaskForm(instance=task)
        return render(request, 'tasks/task.html', {'form': form, 'task': task})


class TaskCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    form_class = CreateTaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = "Задачи успешно создана!"

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class TaskShow(LoginRequiredMixin, View):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
        # tasks = Task.objects.all()
        return render(request, 'tasks/tasks.html', {
            'form': task_filter.form,
            'tasks': task_filter.qs,
        })


class TaskEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    model = Task
    template_name = 'edit.html'
    form_class = CreateTaskForm
    success_message = "Задача успешно обновлена!"

    def get_success_url(self):
        return reverse('tasks')


class TaskDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().dispatch(request, *args, **kwargs)

    model = Task
    template_name = 'auth/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Задача успешно удалёна!")
        return redirect(self.success_url)

# Удалять задачи может их создатель
# Нельзя удалить юзера у которого есть задачи
# Добавить индивидуальную задачу