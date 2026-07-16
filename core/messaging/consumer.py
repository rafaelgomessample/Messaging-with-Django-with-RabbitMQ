import json
import logging
from typing import Callable
from pika.adapters.blocking_connection import BlockingChannel
from core.messaging.exchanges import ExchangeEnum
from core.messaging.connection import RabbitMQConnection



logger = logging.getLogger(__name__)


class EventConsumer:
    def __init__(self, exchange: ExchangeEnum, queue_name: str, routing_key: str):
        self.exchange = exchange
        self.queue_name = queue_name
        self.routing_key = routing_key

    def _setup_queue(self, channel: BlockingChannel):
        channel.queue_declare(
            queue=self.queue_name,
            durable=True,
        )
        channel.queue_bind(
            queue=self.queue_name,
            exchange=self.exchange,
            routing_key=self.routing_key,
        )

    def consume(self, handler: Callable[[dict], None]):
        channel = RabbitMQConnection.get_channel()

        self._setup_queue(channel)

        channel.basic_qos(prefetch_count=10)

        def _on_message(ch: BlockingChannel, method, properties, body):
            try:
                payload = json.loads(body)
                handler(payload)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception:
                logger.exception(f"Error send event in to {self.queue_name}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_consume(queue=self.queue_name, on_message_callback=_on_message)
        channel.start_consuming()
