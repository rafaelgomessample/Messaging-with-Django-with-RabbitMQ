from django.core.management.base import BaseCommand

from core.messaging.consumer import EventConsumer
from core.messaging.exchanges import ExchangeEnum
from payments.handlers.payments_handlers import (
    payment_change_status_handler,
    payment_notification_handler,
)


DATA_EVENT_HANDLER_MAPPING_BY_EVENT = {
    "payment_change_status": dict(
        exchange=ExchangeEnum.PAYMENTS,
        queue_name="payments.payment_change_status",
        routing_key="payments.payment_change_status",
        handler=payment_change_status_handler,
    ),
    "payment_notification": dict(
        exchange=ExchangeEnum.PAYMENTS,
        queue_name="payments.payment_notification",
        routing_key="payments.payment_notification",
        handler=payment_notification_handler,
    )
}


class Command(BaseCommand):
    # This description shows up when running: python manage.py start_subscribers --help
    help = "Starts the consumer processes"

    def add_arguments(self, parser):
        parser.add_argument("event", type=str)

    def handle(self, *args, **options):
        event = options["event"]
        data_event = DATA_EVENT_HANDLER_MAPPING_BY_EVENT[event]
        exchange = data_event["exchange"]
        queue_name = data_event["queue_name"]
        routing_key = data_event["routing_key"]

        print(f"==================================")
        print(f"Start consumer event from {event}")
        print(f"Exchange: {exchange}")
        print(f"Queue: {queue_name}")
        print(f"Routing key: {routing_key}")
        print(f"==================================")

        EventConsumer(
            exchange=exchange,
            queue_name=queue_name,
            routing_key=routing_key,
        ).consume(data_event["handler"])
