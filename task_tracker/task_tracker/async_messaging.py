import json

from kafka import KafkaProducer

from . import settings


class Event:
    TOPIC = "task_tracker"

    def __init__(self, data) -> None:
        self.data = data

    def get_msg(self):
        return self.data

    def send(self):
        message = {**self.get_msg(), "event_type": self.__class__.__name__}
        p = create_producer()
        print("Publishing message", self.TOPIC, message)
        p.send(self.TOPIC, value=message)


class BaseTaskEvent(Event):
    def get_msg(self):
        task = self.data
        return {
            "task_id": task.id,
            "task_uuid": task.uuid,
            "task_title": task.title,
        }


class TaskAdded(BaseTaskEvent):
    pass


class TaskClosed(BaseTaskEvent):
    pass


class TaskAssigned(Event):
    def get_msg(self):
        task = self.data
        return {
            "task_id": task.id,
            "task_uuid": task.uuid,
            "task_title": task.title,
            "task_assignee": task.assignee.external_user_id,
        }


def serializer(msg: dict):
    return json.dumps(msg).encode("utf-8")


def create_producer() -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVERS,
        value_serializer=serializer,
    )
    return producer
