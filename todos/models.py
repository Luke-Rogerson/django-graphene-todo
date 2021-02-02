from django.db import models


class Todo(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, null=True)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)