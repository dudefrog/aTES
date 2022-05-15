from uuid import uuid4

from django.db import models

from users.models import User


def generate_uuid():
    return str(uuid4())


class Task(models.Model):
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=None
    )
    public_id = models.CharField(max_length=128, default=generate_uuid)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    # Intentional simplification: task only has 2 states
    is_closed = models.BooleanField(default=False)
