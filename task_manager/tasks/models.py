from django.db import models
from django.db.models import DateTimeField

from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='tasks')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_authored')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned', null=True)
    date_joined = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
