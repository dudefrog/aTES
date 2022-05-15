import random

from .models import Task, Transaction
from users.models import User


def generate_task_completion_sum() -> int:
    return round(random.uniform(20, 40), 2) * 100


def charge_user_for_task(user: User, task: Task):
    Transaction.objects.create(
        amount=task.cost,
        user=user,
        is_debit=True,
        related_task=task,
    )
    user.balance -= task.cost
    user.save()


def topup_user_for_task_completion(user: User, task: Task):
    sum = generate_task_completion_sum()
    Transaction.objects.create(
        amount=sum,
        user=user,
        is_credit=True,
        related_task=task,
    )
    user.balance += sum
    user.save()


def get_or_create_task(public_id: str, title: str = "", user=None) -> Task:
    try:
        return Task.objects.get(public_id=public_id)
    except Task.DoesNotExist:
        return Task.objects.create(
            public_id=public_id,
            title=title,
            assignee=user,
        )
