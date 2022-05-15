import random

from django.db import models

from users.models import User


def generate_task_cost() -> int:
    return round(random.uniform(10, 20), 2) * 100


class Task(models.Model):
    public_id = models.CharField(editable=False, max_length=64)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(default="", max_length=256)

    cost = models.IntegerField(default=generate_task_cost)


class Transaction(models.Model):
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=256, default="")
    is_debit = models.BooleanField(default=False)
    is_credit = models.BooleanField(default=False)

    related_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
