import json
import uuid
from datetime import datetime

from kafka import KafkaProducer

from .schema import Schema


class Event:
    TOPIC = None
    PRODUCER = None
    NAME = None
    VERSION = 1

    def __init__(self, data) -> None:
        self.data = data
        self.msg = self.get_msg()

    def get_msg(self):
        return {
            "event_id": str(uuid.uuid4()),
            "event_version": self.VERSION,
            "event_name": self.NAME,
            "event_time": str(datetime.utcnow()),
            "producer": self.PRODUCER,
            "data": self.data,
        }


def serializer(msg: dict):
    return json.dumps(msg).encode("utf-8")


def create_producer(servers) -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=serializer,
    )
    return producer


def send_message(event: Event, producer: KafkaProducer):
    print("Publishing message", event.TOPIC, event.msg)
    producer.send(event.TOPIC, value=event.msg)


def validate_and_publish(event_class, data, producer):
    event = event_class(data)
    schema = Schema(f"{event_class.NAME}.{event_class.VERSION}")
    schema.validate(event.msg)

    print("Publishing message", event.TOPIC, event.msg)
    producer.send(event.TOPIC, value=event.msg)
