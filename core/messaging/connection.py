import pika
from django.conf import settings
from pika.adapters.blocking_connection import BlockingChannel


class RabbitMQConnection:

    _connection : pika.BlockingConnection | None = None
    _channel : BlockingChannel | None = None

    @classmethod
    def get_channel(cls) -> BlockingChannel:
        if cls._connection is None or cls._connection.is_closed:
            cls._connect()
        return cls._channel

    @classmethod
    def _connect(cls):
        cls._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(
                    username=settings.RABBITMQ_USERNAME,
                    password=settings.RABBITMQ_PASSWORD,
                ),
                heartbeat=30,
                blocked_connection_timeout=10,
            )
        )
        cls._channel = cls._connection.channel()
