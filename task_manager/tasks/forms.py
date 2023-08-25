from django import forms
from django.db.models import DateTimeField
from django.contrib.auth.models import User

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class CreateTaskForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label="Имя")
    description = forms.CharField(max_length=255, label="Описание")
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    author = forms.ModelChoiceField(queryset=User.objects.all())
    worker = forms.ModelChoiceField(queryset=User.objects.all())
    labels = forms.ModelMultipleChoiceField(queryset=Label.objects.all())
    date_joined = DateTimeField(auto_now_add=True)

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'author', 'worker', 'labels']
