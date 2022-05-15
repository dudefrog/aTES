import json
from abc import abstractmethod
from datetime import datetime
from typing import Any, Dict

import pydantic
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer


class Message(pydantic.BaseModel):
    event_id: str
    event_version: int
    event_name: str
    event_time: datetime
    producer: str
    data: Dict[str, Any]


class ConsumeCommand(BaseCommand):
    SERVICE = ""
    TOPICS = []
    KAFKA_SERVERS = []

    def handle(self, *args, **options):

        print(f"Initializing consumer for {self.SERVICE} service..")
        consumer = KafkaConsumer(
            *self.TOPICS,
            bootstrap_servers=self.KAFKA_SERVERS,
        )

        print("Consumer started. Waiting for messages in", self.TOPICS)
        for message in consumer:
            record = json.loads(message.value.decode("utf8"))
            msg = Message(**record)
            print(f"Handling {msg.event_name}")
            self.handle_message(msg)

    @abstractmethod
    def handle_message(self, msg: Message):
        pass
