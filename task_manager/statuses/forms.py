from django import forms

from task_manager.statuses.models import Status


class CreateStatusForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label='Имя')

    class Meta:
        model = Status
        fields = ['name']
