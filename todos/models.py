from django.contrib.auth import get_user_model
from django.db import models
import uuid
from typing import cast


class Todo(models.Model):
    id = cast(str, models.UUIDField(primary_key=True,
                                    default=uuid.uuid4, editable=False))
    text = cast(str, models.CharField(max_length=200))
    date_added = cast(str, models.DateTimeField(auto_now_add=True))
    # no_type_check
    date_updated = cast(str, models.DateTimeField(default=None, null=True))
    completed = cast(bool, models.BooleanField(default=False))
    deleted = cast(bool, models.BooleanField(default=False))
    created_by = cast(str, models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE))
