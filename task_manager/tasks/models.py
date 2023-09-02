from django.db import models
from django.db.models import DateTimeField
# from django.contrib.auth.models import User

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import Correctly_Displayed_User


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name='tasks'
    )
    author = models.ForeignKey(
        Correctly_Displayed_User, on_delete=models.PROTECT, related_name='tasks_authored'
    )
    executor = models.ForeignKey(
        Correctly_Displayed_User, on_delete=models.PROTECT, related_name='tasks_assigned',
        null=True
    )
    labels = models.ManyToManyField(Label)
    creation_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
