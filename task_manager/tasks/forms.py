from django import forms
from django.db.models import DateTimeField
from django.contrib.auth.models import User

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class CreateTaskForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label='Имя')
    description = forms.CharField(
        label='Описание', required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'placeholder': 'Описание'
        })
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(), label='Статус'
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(), label='Исполнитель', required=False
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(), label='Метки', required=False
    )
    creation_date = DateTimeField(auto_now_add=True)

    User.__str__ = lambda self: f'{self.first_name} {self.last_name}'

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
