import json

from kafka import KafkaProducer

from . import settings


class Event:
    TOPIC = "auth"

    def __init__(self, data) -> None:
        self.data = data

    def get_msg(self):
        return self.data

    def send(self):
        message = {**self.get_msg(), "event_type": self.__class__.__name__}
        p = create_producer()
        print("Publishing message", self.TOPIC, message)
        p.send(self.TOPIC, value=message)


class UserEvent(Event):
    def get_msg(self):
        user = self.data
        return {
            "user_id": user.id,
            "username": user.username,
        }


class UserRegistered(UserEvent):
    pass


class UserLoggedIn(UserEvent):
    pass


class UsernameChanged(UserEvent):
    pass


def serializer(msg: dict):
    return json.dumps(msg).encode("utf-8")


def create_producer() -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVERS,
        value_serializer=serializer,
    )
    return producer
