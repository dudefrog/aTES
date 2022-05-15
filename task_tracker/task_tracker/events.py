from ates.async_messaging import Event, create_producer
from ates.async_messaging import validate_and_publish as _validate_and_publish

from . import settings
from tasks.models import Task

PRODUCER = create_producer(settings.KAFKA_SERVERS)


def validate_and_publish(event_class, event_data):
    _validate_and_publish(event_class, event_data, PRODUCER)


class TaskTrackerEvent(Event):
    PRODUCER = "task_tracker"

    def get_msg(self):
        task: Task = self.data
        msg = super().get_msg()
        msg["data"] = {
            "public_id": task.public_id,
            "title": task.title,
        }
        return msg


class TaskLifecycleEvent(TaskTrackerEvent):
    TOPIC = "task-lifecycle"


class TaskAdded_v1(TaskLifecycleEvent):
    NAME = "tasks.added"


class TaskClosed_v1(TaskLifecycleEvent):
    NAME = "tasks.closed"

    def get_msg(self):
        msg = super().get_msg()
        msg["data"]["user_public_id"] = self.data.assignee.public_id
        return msg


class TaskAssigned_v1(TaskLifecycleEvent):
    NAME = "tasks.assigned"

    def get_msg(self):
        msg = super().get_msg()
        msg["data"]["user_public_id"] = self.data.assignee.public_id
        return msg
