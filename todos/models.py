from django.contrib.auth import get_user_model
from django.db import models
import uuid


class Todo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, null=True)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)
