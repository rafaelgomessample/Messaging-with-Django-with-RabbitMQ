import pika
import json
from core.messaging.exchanges import ExchangeEnum
from core.messaging.connection import RabbitMQConnection


class EventPublisher:

    def __init__(self, exchange: ExchangeEnum):
        self.exchange = exchange

    def publish(self, routing_key: str, payload: dict):
        channel = RabbitMQConnection.get_channel()

        try:
            channel.basic_publish(
                exchange=self.exchange.value,
                routing_key=routing_key,
                body=json.dumps(payload),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    content_type='application/json',
                    message_id=None #id message
                ),
            )
        except Exception as exc:
            print(f"Error publishing message: {exc}")
