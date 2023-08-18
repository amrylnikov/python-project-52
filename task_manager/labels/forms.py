from django import forms

from task_manager.labels.models import Label


class CreateLabelForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Label
        fields = ['name']
