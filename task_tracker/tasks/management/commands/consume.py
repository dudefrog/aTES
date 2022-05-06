from django.core.management.base import BaseCommand, CommandError

from kafka import KafkaConsumer

from task_tracker import settings

TOPICS = ["auth", "task_tracker"]


class Command(BaseCommand):
    def handle(self, *args, **options):

        print("Initializing consumer...")
        consumer = KafkaConsumer(
            *TOPICS,
            bootstrap_servers=settings.KAFKA_SERVERS,
        )

        print("Consumer started. Waiting for messages in", TOPICS)
        for message in consumer:
            print(message)
