import django_filters
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(method='my_custom_filter')
    author = django_filters.BooleanFilter

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })
