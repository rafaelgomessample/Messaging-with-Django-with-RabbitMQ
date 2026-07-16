from enum import Enum
from core.messaging.connection import RabbitMQConnection


class ExchangeEnum(str, Enum):
    ORDERS = "orders_exchange"
    PAYMENTS = "payments_exchange"


def declare_exchanges():
    channel = RabbitMQConnection.get_channel()

    for exchange in ExchangeEnum:
        channel.exchange_declare(
            exchange=exchange.value,
            exchange_type="topic",
            durable=True
        )
