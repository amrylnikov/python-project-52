import django_filters
# from django.contrib.auth.models import User

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.users.models import Correctly_Displayed_User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label='Статус'
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=Correctly_Displayed_User.objects.all(), label='Исполнитель'
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(), label='Метка'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_tasks(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })
