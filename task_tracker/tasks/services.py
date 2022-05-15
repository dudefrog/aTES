import random
from typing import List

from task_tracker import events
from task_tracker.events import validate_and_publish
from tasks.models import Task
from users.models import User


def get_assignable_users():
    return User.objects.exclude(username="admin").exclude(role="manager").all()


def pick_random_user() -> User:
    return random.choice(get_assignable_users())


def shuffle_tasks():
    tasks: List[Task] = Task.objects.filter(is_closed=False).all()
    user_ids = [user.id for user in get_assignable_users()]
    for task in tasks:
        task.assignee_id = random.choice(user_ids)
        task.save()
        validate_and_publish(events.TaskAssigned_v1, task)
