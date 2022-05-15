from asyncio import events

from ates.consumer import ConsumeCommand, Message

from accounting.services import (
    charge_user_for_task,
    get_or_create_task,
    topup_user_for_task_completion,
)
from billing import settings
from users.services import get_or_create_user
from users.views import PWD


def handle_task_added(msg: Message):
    task = get_or_create_task(public_id=msg.data["public_id"])
    if not task.title:
        task.title = msg.data["title"]
        task.save()


def handle_task_assigned(msg: Message):
    user = get_or_create_user(public_id=msg.data["user_public_id"])
    task = get_or_create_task(public_id=msg.data["public_id"], user=user)
    charge_user_for_task(user, task)


def handle_task_closed(msg: Message):
    user = get_or_create_user(public_id=msg.data["user_public_id"])
    task = get_or_create_task(public_id=msg.data["public_id"], user=user)
    topup_user_for_task_completion(user, task)


def handle_user_created(msg: Message):
    get_or_create_user(
        public_id=msg.data["public_id"],
        username=msg.data["username"],
        role=msg.data["role"],
    )


def handle_user_updated(msg: Message):
    user = get_or_create_user(
        public_id=msg.data["public_id"],
    )
    new_role = msg.data.get("role")
    if new_role and (not user.role or user.role != new_role):
        user.role = new_role
    new_username = msg.data.get("username")
    if new_username and (not user.username or user.username != new_username):
        user.role = new_username
    user.save()


HANDLERS = {
    "tasks.added": {
        1: handle_task_added,
    },
    "tasks.assigned": {
        1: handle_task_assigned,
    },
    "tasks.closed": {
        1: handle_task_closed,
    },
    "users.created": {
        1: handle_user_created,
    },
    "users.updated": {
        1: handle_user_updated,
    },
}


class Command(ConsumeCommand):
    SERVICE = "billing"
    TOPICS = ["task-lifecycle", "user-lifecycle"]
    KAFKA_SERVERS = settings.KAFKA_SERVERS

    def handle_message(self, msg: Message):
        handler = HANDLERS.get(msg.event_name, {}).get(msg.event_version)
        if handler:
            handler(msg)
