from django.db import models
from django.db.models import DateTimeField


class Label(models.Model):
    name = models.CharField(max_length=255)
    creation_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
