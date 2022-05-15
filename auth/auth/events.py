from ates.async_messaging import Event, create_producer
from ates.async_messaging import validate_and_publish as _validate_and_publish

from . import settings
from users.models import User

PRODUCER = create_producer(settings.KAFKA_SERVERS)


def validate_and_publish(event_class, event_data):
    _validate_and_publish(event_class, event_data, PRODUCER)


class UserEvent(Event):
    PRODUCER = "auth"


class UserLifecycleEvent(UserEvent):
    TOPIC = "user-lifecycle"


class UserCreated_v1(UserLifecycleEvent):
    NAME = "users.created"

    def get_msg(self):
        user: User = self.data
        msg = super().get_msg()
        msg["data"] = {
            "public_id": user.public_id,
            "username": user.username,
            "role": user.role,
        }
        return msg


class UserUpdated_v1(UserLifecycleEvent):
    NAME = "users.updated"
