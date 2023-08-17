from django.db import models
from django.db.models import DateTimeField


class Status(models.Model):
    name = models.CharField(max_length=255)
    date_joined = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
